"""Helpers needed for computing transmitted delays if not provided.
"""
import numpy as np


def compute_pw_delays_3d(angles, probe, speed_of_sound=1540.,
                         transmission_mode='positives', smallest=True):
    """Converting the lateral and elevational angles to positive focuses for
    plane wave imaging.

    :param numpy.ndarray angles: The list of the angles to send, in radians
    :param Probe probe: The probe class with the information relative to the
        elements geometry and coordinates
    :param float speed_of_sound: The estimated speed of sound of the medium to
        compute the transmission delays (default is 1540)
    :param str transmission_mode: The mode of transmission depending on the
        used convention. Can either be 'positives', setting all the delays to
        positive values, 'negatives', the opposite, or 'centered', where the
        maximum delay is equal to minus the minimum delay (only used in Picmus
        to my knowledge)
    :param bool smallest: If set to True, will make the minimum delay for each
        cycle equal to 0

    :returns: The delays for all the angles and probes elements, of shape
        (nb_angles, nb_probe_elements)
    :return type: numpy.ndarray
    """
    if transmission_mode not in ['positives', 'centered', 'negatives']:
        raise AttributeError(
           "Transmission mode needs to be either 'positives', 'centered' or "
           "'negatives'.")

    assert all(abs(angles.ravel()) < np.pi / 2), \
           "Angles must be in radians (|angle| < pi / 2)"

    assert angles.ndim == 2, \
           "In 3D, expects the lateral and elevational components."

    angles_lateral, angles_elevational = angles[0, :], angles[1, :]

    # Plane wave
    x_coords = probe.geometry[0, :]
    y_coords = probe.geometry[1, :]
    z_coords = probe.geometry[2, :]
    distances = x_coords[None, :] * np.sin(angles_lateral[:, None])
    distances += y_coords[None, :] * np.sin(angles_elevational[:, None])
    distances += z_coords[None, :]

    # Convert to delays
    delays = distances / speed_of_sound

    # Make all of them positives
    min_ref = np.min(delays, axis=1)[:, None] if smallest else np.min(delays)
    delays -= min_ref

    # Distinct transmission modes
    if transmission_mode == 'centered':
        delays -= (np.max(delays) / 2)
    elif transmission_mode == 'negatives':
        delays -= np.max(delays)

    return delays


def compute_pw_delays(angles, probe, speed_of_sound=1540.,
                      transmission_mode='positives', smallest=True):
    """Computes the transmission delays to send the plane waves with the given
    angles based on the probes used and the transmission mode.

    :param numpy.ndarray angles: The list of the angles to send, in radians
    :param Probe probe: The probe class with the information relative to the
        elements geometry and coordinates
    :param float speed_of_sound: The estimated speed of sound of the medium to
        compute the transmission delays (default is 1540)
    :param str transmission_mode: The mode of transmission depending on the
        used convention. Can either be 'positives', setting all the delays to
        positive values, 'negatives', the opposite, or 'centered', where the
        maximum delay is equal to minus the minimum delay (only used in Picmus
        to my knowledge)
    :param bool smallest: If set to True, will make the minimum delay for each
        cycle equal to 0

    :returns: The delays for all the angles and probes elements, of shape
        (nb_angles, nb_probe_elements)
    :return type: numpy.ndarray
    """
    if transmission_mode not in ['positives', 'centered', 'negatives']:
        raise AttributeError(
           "Transmission mode needs to be either 'positives', 'centered' or "
           "'negatives'.")

    assert all(abs(angles.ravel()) < np.pi / 2), \
           "Angles must be in radians (|angle| < pi / 2)"

    # If any angles in the elevational axis are given, compute 2D delays (got
    # a matricial probe)
    if angles.ndim == 2:
        assert probe.geometry_type == 'matricial', \
            "3D delays will be computed, the probe must be matricial."
        return compute_pw_delays_3d(angles, probe, speed_of_sound,
                                    transmission_mode, smallest)

    # Plane wave along the lateral axis
    x_coords = probe.geometry[0, :]
    z_coords = probe.geometry[2, :]
    distances = x_coords[None, :] * np.sin(angles[:, None])
    distances += z_coords[None, :]

    # Convert to delays
    delays = distances / speed_of_sound

    # Make all of them positives
    min_ref = np.min(delays, axis=1)[:, None] if smallest else np.min(delays)
    delays -= min_ref

    # Distinct transmission modes
    if transmission_mode == 'centered':
        delays -= (np.max(delays) / 2)
    elif transmission_mode == 'negatives':
        delays -= np.max(delays)

    return delays


def compute_dw_delays_3d(angles, probe, radius, speed_of_sound=1540.,
                         transmission_mode='positives', smallest=True,
                         center=None):
    """Converting the lateral and elevational angles to positive focuses for
    plane wave imaging.

    :param numpy.ndarray angles: The list of the angles to send, in radians
    :param Probe probe: The probe class with the information relative to the
        elements geometry and coordinates
    :param float radius: Sets the radius along the angle axis
    :param float speed_of_sound: The estimated speed of sound of the medium to
        compute the transmission delays (default is 1540)
    :param str transmission_mode: The mode of transmission depending on the
        used convention. Can either be 'positives', setting all the delays to
        positive values, 'negatives', the opposite, or 'centered', where the
        maximum delay is equal to minus the minimum delay (only used in Picmus
        to my knowledge)
    :param bool smallest: If set to True, will make the minimum delay for each
        cycle equal to 0
    :param list center: If set, defines the center of the probe. It is useful
        when the whole probe is not used

    :returns: The delays for all the angles and probes elements, of shape
        (nb_angles, nb_probe_elements)
    :return type: numpy.ndarray
    """
    if transmission_mode not in ['positives', 'centered', 'negatives']:
        raise AttributeError(
           "Transmission mode needs to be either 'positives', 'centered' or "
           "'negatives'.")

    assert all(abs(angles.ravel()) < np.pi / 2), \
           "Angles must be in radians (|angle| < pi / 2)"

    assert angles.ndim == 2, \
           "In 3D, expects the lateral and elevational components."

    assert center is None or len(center) == 3, \
           "The center of the probe should be 3D (x, y, z)"

    angles_lateral, angles_elevational = angles[0, :], angles[1, :]

    # Get the center of the probe
    x_coords = probe.geometry[0, :]
    y_coords = probe.geometry[1, :]
    z_coords = probe.geometry[2, :]
    z_min, z_max = np.min(z_coords), np.max(z_coords)
    if center is not None:
        xc, yc, zc = center
    else:
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        xc = x_min + ((x_max - x_min) / 2)
        yc = y_min + ((y_max - y_min) / 2)

    # Get the virtual sources
    x0 = xc - (np.sin(angles_lateral) * radius)
    y0 = yc - (np.sin(angles_elevational) * radius)
    z0 = z_max - (radius * (np.cos(angles_lateral) +
                            np.cos(angles_elevational)))

    # Diverging distances
    distances = np.sqrt((x_coords[None, :] - x0[:, None]) ** 2 +
                        (y_coords[None, :] - y0[:, None]) ** 2 +
                        (z_coords[None, :] - z0[:, None]) ** 2)

    # Convert to delays
    delays = distances / speed_of_sound

    # Make all of them positives
    min_ref = np.min(delays, axis=1)[:, None] if smallest else np.min(delays)
    delays -= min_ref

    # Distinct transmission modes
    if transmission_mode == 'centered':
        delays -= (np.max(delays) / 2)
    elif transmission_mode == 'negatives':
        delays -= np.max(delays)

    return delays


def compute_dw_delays(angles, probe, radius, speed_of_sound=1540.,
                      transmission_mode='positives', smallest=True,
                      center=None):
    """Computes the transmission delays to send the diverging waves with the
    given angles based on the probes used and the transmission mode.

    :param numpy.ndarray angles: The list of the angles to send, in radians
    :param Probe probe: The probe class with the information relative to the
        elements geometry and coordinates
    :param float radius: Sets the radius along the angle axis
    :param float speed_of_sound: The estimated speed of sound of the medium to
        compute the transmission delays (default is 1540)
    :param str transmission_mode: The mode of transmission depending on the
        used convention. Can either be 'positives', setting all the delays to
        positive values, 'negatives', the opposite, or 'centered', where the
        maximum delay is equal to minus the minimum delay (only used in Picmus
        to my knowledge)
    :param bool smallest: If set to True, will make the minimum delay for each
        cycle equal to 0
    :param list center: If set, defines the center of the probe. It is useful
        when the whole probe is not used

    :returns: The delays for all the angles and probes elements, of shape
        (nb_angles, nb_probe_elements)
    :return type: numpy.ndarray
    """
    if transmission_mode not in ['positives', 'centered', 'negatives']:
        raise AttributeError(
           "Transmission mode needs to be either 'positives', 'centered' or "
           "'negatives'.")

    assert all(abs(angles.ravel()) < np.pi / 2), \
           "Angles must be in radians (|angle| < pi / 2)"

    # If any angles in the elevational axis are given, compute 2D delays (got
    # a matricial probe)
    if angles.ndim == 2:
        assert probe.geometry_type == 'matricial', \
            "3D delays will be computed, the probe must be matricial."
        return compute_dw_delays_3d(angles, probe, radius, speed_of_sound,
                                    transmission_mode, smallest, center)

    assert center is None or len(center) == 3, \
           "The center of the probe should be 3D (x, y, z)"

    # Get the center of the probe
    x_coords = probe.geometry[0, :]
    z_coords = probe.geometry[2, :]
    z_min, z_max = np.min(z_coords), np.max(z_coords)
    if center is not None:
        xc, yc, zc = center
    else:
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        xc = x_min + ((x_max - x_min) / 2)

    # Get the virtual sources
    x0 = xc - (np.sin(angles) * radius)
    z0 = z_max - (np.cos(angles) * radius)

    # Diverging distances
    distances = np.hypot(x_coords[None, :] - x0[:, None],
                         z_coords[None, :] - z0[:, None])

    # Convert to delays
    delays = distances / speed_of_sound

    # Make all of them positives
    min_ref = np.min(delays, axis=1)[:, None] if smallest else np.min(delays)
    delays -= min_ref

    # Distinct transmission modes
    if transmission_mode == 'centered':
        delays -= (np.max(delays) / 2)
    elif transmission_mode == 'negatives':
        delays -= np.max(delays)

    return delays
