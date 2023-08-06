"""Scan class, to store the information about the scan we want to beamform. Two
kinds of scans are supported for now, the Grid ones (regular grid of pixels),
and the Polar ones (polar coordinates).
"""
import logging
import numpy as np

from .utils import scan as scan_utils

from .config import cfg
if cfg.GPU_AVAILABLE:
    from .gpu import gpu_utils


logger = logging.getLogger(__name__)


class Scan(object):
    """The parent class, whatever the format of scan you're willing to beamform,
    it must inherit from this class to guarantee that its main methods will
    exist. See the GridScan and PolarScan below for examples.

    :ivar bool on_gpu: If set to False, the points will be stored in numpy
        arrays. Else case, cupy.array
    :ivar bool is_3d: Defines if the scan is in 3 dimensions or not
    :ivar tuple pixels: The coordinates of the pixels to beamform, either a 2D
        tuple with the coordinates (xx, zz), or 3D (xx, yy, zz)
    :ivar int nb_x: The resolution in the lateral axis
    :ivar int nb_y: The resolution in the elevational axis
    :ivar int nb_z: The resolution in the axial axis
    :ivar float, numpy.ndarray axial_step: The step of the axial dimension, it
        is either a float if the resolution is the same through the whole grid,
        or an array if it changes based on the lateral / elevational position.
        In this case, the output has the shape (nb_x,) for 2D, or (nb_x, nb_y)
        for 3D scans
    :ivar tuple shape: The shape of the scan: (nb_x, nb_z) in 2D, or
        (nb_x, nb_y, nb_y) in 3D
    """

    def __init__(self, on_gpu):
        """Initialization for the Scan, should not be called from here. Use a
        child class instead.

        :param bool on_gpu: If set to False, the points will be stored in numpy
            arrays. Else case, cupy.array
        """
        self._on_gpu = on_gpu
        self._is_3d = False
        self._pixels = None
        self._bounds = ()
        self._axis_to_fix = None
        self._fixed_axis = None

    @property
    def on_gpu(self):
        return self._on_gpu

    @property
    def is_3d(self):
        return self._is_3d

    @property
    def pixels(self):
        return self._pixels

    @property
    def bounds(self):
        return self._bounds

    @property
    def nb_x(self):
        """Returns the lateral resolution, should be implemented in child
        classes.
        """
        raise NotImplementedError

    @property
    def nb_y(self):
        """Returns the elevational resolution, should be implemented in child
        classes.
        """
        raise NotImplementedError

    @property
    def nb_z(self):
        """Returns the axial resolution, should be implemented in child
        classes.
        """
        raise NotImplementedError

    @property
    def axial_step(self):
        """Returns the axial step, should be implemented in child classes.
        """
        raise NotImplementedError

    @property
    def shape(self):
        """Returns the shape of the scan, in 2D or 3D based on the scan
        characteristics.

        :returns: The shape of the scan: (nb_x, nb_z) in 2D, or
            (nb_x, nb_y, nb_y) in 3D
        :return type: tuple
        """
        if self.is_3d:
            shp = [self.nb_x, self.nb_y, self.nb_z]
            if self._axis_to_fix is not None:
                shp[self._axis_to_fix] = 1
            return tuple(shp)
        else:
            return self.nb_x, self.nb_z

    def set_on_gpu(self, on_gpu):
        """Updates the on_gpu attribute if requested, will change the format
        of the pixels coordinates.

        :param bool on_gpu: True if is on GPU
        """
        if not cfg.GPU_AVAILABLE and on_gpu:
            logger.error("GPU mode is not available on this system.")
            return

        if self.on_gpu != on_gpu:
            self._on_gpu = on_gpu
            self._pixels = self._chose_type(self.pixels)

    def ravel_pixels(self):
        """Ravels the pixels of the scan, to make them usable for beamforming.
        The returned pixels are always a 3D tuple, with the elevational
        coordinates of the pixels set to zero if we are in 2D.

        :returns: The ravelled pixels coordinates (coords_x, coords_y, coords_z)
        :return type: tuple
        """
        # Maybe this should raise an error?
        if self.pixels is None:
            return ()

        if self.is_3d:
            return (self.pixels[0].ravel(),
                    self.pixels[1].ravel(),
                    self.pixels[2].ravel())

        else:
            # In 2D, we create 0 y-coordinates
            xx, zz = self.pixels[0].ravel(), self.pixels[1].ravel()
            yy = np.zeros_like(xx)
            return xx, yy, zz

    def remove_fixed_axis(self):
        """Remove the fixed axis information, if any.
        """
        self._axis_to_fix = None
        self._fixed_axis = None
        self._pixels = self.build_pixels()

    def build_pixels(self):
        """Builds the pixels coordinates, based on the scan characteristics,
         this should be implemented in child classes.
        """
        raise NotImplementedError

    def oversample_axial(self, *args, **kwargs):
        """Over-samples the scan in the axial direction, this should be
        implemented in child classes.
        """
        raise NotImplementedError

    def downsample_axial(self, *args, **kwargs):
        """Down-samples the scan in the axial direction, this should be
        implemented in child classes.
        """
        raise NotImplementedError

    def _chose_type(self, array):
        """Returns the array in the good format: numpy array if on CPU, cupy
        array else case.

        :param np.ndarray, cp.array array: The array to convert
        """
        if self.on_gpu:
            return gpu_utils.send_to_gpu(np.array(array), np.float32)
        else:
            try:
                array = array.get().astype(float)
            except AttributeError:
                pass
            return array

    def _fix_an_axis(self, axis, index):
        """If on 3D, defines a fixed axis for slice beamforming (especially for
        tri-plan or 2D visualization). This should be called by children.

        :param int axis: The axis to fix, either 0, 1 or 2, for the x, y or z
            axes
        :param int, float index: The index of the vector to fix
        """
        if not self.is_3d:
            logger.error("Can't fix an axis in 2D, ignored.")
            return 0

        if not (0 <= axis <= 2):
            raise NotImplementedError(
                "The axis must be either 0 (x), 1 (y) or 2 (z).")

        nb_max = {
            0: self.nb_x,
            1: self.nb_y,
            2: self.nb_z,
        }[axis]

        if not (0 <= index < nb_max):
            raise NotImplementedError(
                f"The index is out of bound for axis {axis}.")

        self._axis_to_fix = axis
        return 1

    def _update_bounds(self, pixels):
        """Updates the boundaries of the coordinates for each dimension.

        :param numpy.ndarray pixels: The pixels (of shape (3, nb_x, nb_z), or
            (3, nb_x, nb_y, nb_z) if is_3d)
        """
        self._bounds = tuple((np.min(p), np.max(p)) for p in pixels)


class GridScan(Scan):
    """GridScan class to handle a regular grid of pixels. It expects either two
    or three vectors (for 3D), with respectively the x, y, and z coordinates.

    :ivar bool on_gpu: If set to False, the points will be stored in numpy
        arrays. Else case, cupy.array
    :ivar bool is_3d: Defines if the scan is in 3 dimensions or not
    :ivar tuple pixels: The coordinates of the pixels to beamform, either a 2D
        tuple with the coordinates (xx, zz), or 3D (xx, yy, zz)
    :ivar int nb_x: The resolution in the lateral axis
    :ivar int nb_y: The resolution in the elevational axis
    :ivar int nb_z: The resolution in the axial axis
    :ivar float axial_step: The step of the axial dimension
    :ivar tuple shape: The shape of the scan: (nb_x, nb_z) in 2D, or
        (nb_x, nb_y, nb_y) in 3D
    """

    def __init__(self, axis_1, axis_2, axis_3=None, on_gpu=cfg.GPU_AVAILABLE):
        """Initialization for the Grid scan, it expects either two or three
        vectors (for 3D). If two are given, the grid will be 2D (lateral /
        axial). Else case, the grid will also include the y coordinates (
        lateral / elevational / axial).

        :param np.ndarray axis_1: The first axis for the grid, always the
            lateral axis
        :param np.ndarray axis_2: The second axis for the grid, if axis_3 is
            provided, this will be the elevational axis, else case, it will be
            used as the axial axis
        :param np.ndarray axis_3: Optional, if provided, the axis_2 is used as
            the elevational and this one as the axial, for 3D grids
        :param bool on_gpu: If set to False, the points will be stored in numpy
            arrays. Else case, cupy.array
        """
        # General params
        super().__init__(on_gpu)
        self._is_3d = axis_3 is not None
        self.x_axis = axis_1
        if self.is_3d:
            self.y_axis = axis_2
            self.z_axis = axis_3
        else:
            self.y_axis = None
            self.z_axis = axis_2

        # Builds the pixels
        self._pixels = self.build_pixels()

    @property
    def nb_x(self):
        """Returns the lateral resolution.
        """
        return self.x_axis.size

    @property
    def nb_y(self):
        """Returns the elevational resolution (None if 2D).
        """
        return self.y_axis.size if self.is_3d else None

    @property
    def nb_z(self):
        """Returns the axial resolution.
        """
        return self.z_axis.size

    @property
    def axial_step(self):
        """Returns the axial step.
        """
        axial_step = (self.z_axis[-1] - self.z_axis[0]) / self.nb_z
        if self.on_gpu:
            return axial_step.item()
        return axial_step

    def build_pixels(self):
        """Builds the pixels coordinates, this is simply a meshgrid with the two
        or three vectors provided at initialization, based on if the grid is 2D
        or 3D.

        :returns: The pixels coordinates (xx, zz) in 2D or (xx, yy, zz) in 3D
        :return type: tuple
        """
        if self.is_3d:
            axes = [self.x_axis, self.y_axis, self.z_axis]
            if self._axis_to_fix is not None:
                axes[self._axis_to_fix] = self._fixed_axis
            pixels = np.meshgrid(*axes, indexing='ij')
        else:
            pixels = np.meshgrid(self.x_axis, self.z_axis, indexing='ij')
        self._update_bounds(pixels)
        return self._chose_type(pixels)

    def fix_an_axis(self, axis, index):
        """If on 3D, defines a fixed axis for slice beamforming (especially for
        tri-plan or 2D visualization).

        :param int axis: The axis to fix, either 0, 1 or 2, for the x, y or z
            axes
        :param int, float index: The index of the vector to fix
        """
        if self._fix_an_axis(axis, index):
            self._fixed_axis = {
                0: self.x_axis,
                1: self.y_axis,
                2: self.z_axis,
            }[axis][index]
            self._pixels = self.build_pixels()

    def oversample_axial(self, factor):
        """Over-samples the scan in the axial direction by a factor.

        :param int factor: The factor for the oversampling, will be rounded if
            not an integer
        """
        res_z = self.nb_z * round(factor)
        self.z_axis = np.linspace(self.z_axis[0], self.z_axis[-1], res_z)
        self._pixels = self.build_pixels()

    def downsample_axial(self, factor):
        """Down-samples the scan in the axial direction by a factor.

        :param int factor: The factor for the down-sampling, will be rounded if
            not an integer
        """
        res_z = self.nb_z // round(factor)
        self.z_axis = np.linspace(self.z_axis[0], self.z_axis[-1], res_z)
        self._pixels = self.build_pixels()


class PolarScan(Scan):
    """PolarScan class to handle a regular grid of pixels. It is computing the
    grid using the spherical coordinates, as defined in mathematics, with the
    rhos (radial distances to the origin), the phis (polar angles to the axial
    axis) and, if 3D, the thetas (the azimuthal angles in the initial meridian
    plane).

    :ivar bool on_gpu: If set to False, the points will be stored in numpy
        arrays. Else case, cupy.array
    :ivar bool is_3d: Defines if the scan is in 3 dimensions or not
    :ivar tuple pixels: The coordinates of the pixels to beamform, either a 2D
        tuple with the coordinates (xx, zz), or 3D (xx, yy, zz)
    :ivar int nb_x: The resolution in the lateral axis
    :ivar int nb_y: The resolution in the elevational axis
    :ivar int nb_z: The resolution in the axial axis
    :ivar float axial_step: The step of the axial dimension
    :ivar tuple shape: The shape of the scan: (nb_x, nb_z) in 2D, or
        (nb_x, nb_y, nb_y) in 3D

    .. image:: ../images/polar_system.png
       :width: 300
       :align: center
    """

    def __init__(self, rhos, phis, thetas=None, on_gpu=cfg.GPU_AVAILABLE):
        """Initialization for the Polar scan, it expects either two or three
        vectors (for 3D). If two are given, the grid will be 2D (lateral /
        axial). Else case, the grid will also include the y coordinates
        (lateral / elevational / axial).

        :param np.ndarray rhos: The radial distances to the origin
        :param np.ndarray phis: The polar angles (to the axial axis)
        :param np.ndarray thetas: Optional, if provided, the azimuthal angles
            in the initial meridian plane
        :param bool on_gpu: If set to False, the points will be stored in numpy
            arrays. Else case, cupy.array
        """
        # General params
        super().__init__(on_gpu)
        self._is_3d = thetas is not None
        self.z_rhos = rhos
        self.x_phis = phis
        self.y_thetas = thetas

        # Builds the pixels
        self._pixels = self.build_pixels()

    @property
    def nb_x(self):
        """Returns the lateral resolution (number of phis).
        """
        return self.x_phis.size

    @property
    def nb_y(self):
        """Returns the elevational resolution (number of thetas) (None if 2D).
        """
        return self.y_thetas.size if self.is_3d else None

    @property
    def nb_z(self):
        """Returns the axial resolution (number of rhos).
        """
        return self.z_rhos.size

    @property
    def axial_step(self):
        """Returns the axial steps.
        """
        axial_step = (self.z_rhos[-1] - self.z_rhos[0]) / self.nb_z
        if self.on_gpu:
            return axial_step.item()
        return axial_step

    def build_pixels(self):
        """Builds the pixels coordinates. As we are working in a polar system,
        it first does the meshgrid of the rhos, phis and, if provided, thetas,
        then it is converting them to cartesian coordinates using a basic
        pol2cart method.

        :returns: The pixels coordinates (xx, zz) in 2D or (xx, yy, zz) in 3D
        :return type: tuple
        """
        if self.is_3d:
            axes = [self.x_phis, self.y_thetas, self.z_rhos]
            if self._axis_to_fix is not None:
                axes[self._axis_to_fix] = self._fixed_axis
            pv, tv, rv = np.meshgrid(*axes, indexing='ij')
            pixels = scan_utils.pol2cart_3d(rv, pv, tv)
        else:
            pv, rv = np.meshgrid(self.x_phis, self.z_rhos, indexing='ij')
            pixels = scan_utils.pol2cart(rv, pv)
        self._update_bounds(pixels)
        return self._chose_type(pixels)

    def fix_an_axis(self, axis, index):
        """If on 3D, defines a fixed axis for slice beamforming (especially for
        tri-plan or 2D visualization).

        :param int axis: The axis to fix, either 0, 1 or 2, for the x, y or z
            axes
        :param int, float index: The index of the vector to fix
        """
        if self._fix_an_axis(axis, index):
            self._fixed_axis = {
                0: self.x_phis,
                1: self.y_thetas,
                2: self.z_rhos,
            }[axis][index]
            self._pixels = self.build_pixels()

    def oversample_axial(self, factor):
        """Over-samples the scan in the axial direction by a factor.

        :param int factor: The factor for the oversampling, will be rounded if
            not an integer
        """
        res_z = self.nb_z * round(factor)
        self.z_rhos = np.linspace(self.z_rhos[0], self.z_rhos[-1], res_z)
        self._pixels = self.build_pixels()

    def downsample_axial(self, factor):
        """Down-samples the scan in the axial direction by a factor.

        :param int factor: The factor for the down-sampling, will be rounded if
            not an integer
        """
        res_z = self.nb_z // round(factor)
        self.z_rhos = np.linspace(self.z_rhos[0], self.z_rhos[-1], res_z)
        self._pixels = self.build_pixels()
