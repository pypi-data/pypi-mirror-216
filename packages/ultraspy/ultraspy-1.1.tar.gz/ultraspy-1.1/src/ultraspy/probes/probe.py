"""Probe class, to store the physical characteristics of a probe.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt


class Probe(object):
    """Probe class to handle the probe configuration.

    :ivar str name: The name of the probe
    :ivar str geometry_type: The type of the probe (either linear, convex or
        matricial). Is defined by child
    :ivar float central_freq: The central frequency of the probe (in Hz)
    :ivar float bandwidth: The bandwidth of the probe (should be between 0 and
        200%), in %
    :ivar numpy.ndarray geometry: The coordinates of the elements of the probe
    :ivar int nb_elements: The number elements
    """

    def __init__(self, config):
        """Initialization for the Probe.

        :param dict config: The dictionary with the parameters needed to build
            a probe, at the minimum the central_freq and the nb_elements
        """
        # General params
        self._name = config.get('name', None)
        self._geometry_type = None
        self._central_freq = config['central_freq']
        self._bandwidth = config.get('bandwidth', None)

        # Initializes the coordinates in a 3D map, all zeros for now
        self._nb_elements = np.prod(config['nb_elements'])
        self._geometry = np.zeros((3, self._nb_elements))

    def __str__(self):
        """String sentence to show the probe characteristics.

        :returns: The string sentence to print
        :return type: str
        """
        x, y, z = self.geometry
        return '\n'.join([
            '====== Probe: ======',
            f'name: {self.name}, with a central freq of {self.central_freq}Hz',
            f"Geometry type: {self.geometry_type}",
            f"Probe elements:",
            f"\tlateral (x): [{np.min(x)} ; {np.max(x)}]",
            f"\televational (y): [{np.min(y)} ; {np.max(y)}]",
            f"\taxial (z): [{np.min(z)} ; {np.max(z)}]",
        ])

    @property
    def name(self):
        return self._name

    @property
    def geometry_type(self):
        return self._geometry_type

    @property
    def central_freq(self):
        return self._central_freq

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def nb_elements(self):
        return self._nb_elements

    @property
    def geometry(self):
        return self._geometry

    def set_central_freq(self, central_freq):
        """Setter for the central freq.

        :param float central_freq: The new central frequency
        """
        self._central_freq = central_freq

    def set_bandwidth(self, bandwidth):
        """Setter for the bandwidth.

        :param float bandwidth: The new bandwidth
        """
        self._bandwidth = bandwidth

    def get_thetas(self):
        """This should return the thetas of each probe element if they exist.
        When it happens, this needs to be overwritten in the dedicated child
        class (see ConvexProbe for example).

        :returns: The list of thetas for the probe, if called here and not from
            child (convex), returns a list of 0 thetas
        :return type: numpy.ndarray
        """
        return np.zeros((self.nb_elements,))

    def show(self):
        """Shows the probe geometry.
        """
        x, y, z = self.geometry * 1e3
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(x, y, z)
        ax.set_xlabel('X Lateral (mm)')
        ax.set_ylabel('Y Elevational (mm)')
        ax.set_zlabel('Z Axial (mm)')
        plt.show()

    def show_delays(self, delays, sound_speed=1540):
        """Shows the delays per transmissions using this probe.

        :param numpy.ndarray delays: The delays of each sequence (nb_t, nb_e)
        :param float sound_speed: The speed of sound used for the delays
        """
        # Recover distances, in mm
        delays *= sound_speed * 1e3
        nb_t = delays.shape[0]
        x, y, z = self.geometry * 1e3
        x_lims = (np.min(x) - 1, np.max(x) + 1)
        y_lims = (np.min(y) - 1, np.max(y) + 1)
        z_lims = (np.min(z[None, :] + delays) - 1,
                  np.max(z[None, :] + delays) + 1)
        mutable = {
            'transmission': 0,
        }

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        def on_press(event):
            sys.stdout.flush()
            index = mutable['transmission']

            ax.clear()
            ax.set_xlabel('X Lateral (mm)')
            ax.set_ylabel('Y Elevational (mm)')
            ax.set_zlabel('Z Axial (mm)')

            # Left key
            if event.key == 'left':
                index = (index - 1) % nb_t
            elif event.key == 'right':
                index = (index + 1) % nb_t

            ax.scatter(x, y, z)
            ax.scatter(x, y, z + delays[index], c='red', s=5)
            ax.set_xlim(x_lims)
            ax.set_ylim(y_lims)
            ax.set_zlim(z_lims)
            ax.set_title(f'Delays for transmission {index+1} / {nb_t}')
            mutable['transmission'] = index
            fig.canvas.draw()

        fig.canvas.mpl_connect('key_press_event', on_press)

        ax.set_xlabel('X Lateral (mm)')
        ax.set_ylabel('Y Elevational (mm)')
        ax.set_zlabel('Z Axial (mm)')
        ax.scatter(x, y, z)
        ax.scatter(x, y, z + delays[0], c='red', s=5)
        ax.set_xlim(x_lims)
        ax.set_ylim(y_lims)
        ax.set_zlim(z_lims)
        ax.set_title(f'Delays for transmission 1 / {nb_t}')
        plt.show()

    def show_sequences(self, emission_sequences, reception_sequences):
        """Shows the emission / reception sequences for this probe, per
        transmission.

        :param numpy.ndarray emission_sequences: The indices, per transmission
            of the probe elements used for emission
        :param numpy.ndarray reception_sequences: The indices, per transmission
            of the probe elements used for reception
        """
        x, y, z = self.geometry * 1e3
        nb_t = emission_sequences.shape[0]
        seqs = [emission_sequences, reception_sequences]
        x_lims = (np.min(x) - 1, np.max(x) + 1)
        y_lims = (np.min(y) - 1, np.max(y) + 1)
        z_lims = (np.min(z) - 1, np.max(z) + 1)
        mutable = {
            'transmission': 0,
        }

        fig = plt.figure()
        ax1 = fig.add_subplot(211, projection='3d')
        ax2 = fig.add_subplot(212, projection='3d')
        axs = [ax1, ax2]

        def on_press(event):
            sys.stdout.flush()
            index = mutable['transmission']

            for i, ax in enumerate(axs):
                ax.clear()
                ax.set_xlabel('X Lateral (mm)')
                ax.set_ylabel('Y Elevational (mm)')
                ax.set_zlabel('Z Axial (mm)')

                # Left key
                if event.key == 'left':
                    index = (index - 1) % nb_t
                elif event.key == 'right':
                    index = (index + 1) % nb_t

                ax.scatter(x, y, z, facecolors='none', edgecolors='b',
                           alpha=0.1)
                ax.scatter(x[seqs[i][index]],
                           y[seqs[i][index]],
                           z[seqs[i][index]], c='red')
                ax.set_xlim(x_lims)
                ax.set_ylim(y_lims)
                ax.set_zlim(z_lims)
                fig.suptitle(f'Sequences for transmission {index+1} / {nb_t}')
                mutable['transmission'] = index
                fig.canvas.draw()

        fig.canvas.mpl_connect('key_press_event', on_press)

        for i, ax in enumerate(axs):
            ax.set_xlabel('X Lateral (mm)')
            ax.set_ylabel('Y Elevational (mm)')
            ax.set_zlabel('Z Axial (mm)')
            ax.scatter(x, y, z, facecolors='none', edgecolors='b', alpha=0.1)
            ax.scatter(x[seqs[i][0]], y[seqs[i][0]], z[seqs[i][0]], c='red')
            ax.set_xlim(x_lims)
            ax.set_ylim(y_lims)
            ax.set_zlim(z_lims)
        fig.suptitle(f'Sequences for transmission 1 / {nb_t}')
        plt.show()
