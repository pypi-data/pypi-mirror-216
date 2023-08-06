/* The estimation of the transmission delays of the signals depends on the
delays set while emitting the plane waves. Those can be perform in three ways:
- 0: The plane waves are tilted around the centered element (picmus simulation)
- 1: The plane waves are titled so all the delays are negatives (unused..?)
- 2: The plane waves are titled so all the delays are positives (db-sas / vera)
*/


__device__ float positive_tilt(const float *pos_elements,
                               const int nb_e,
                               const float angle)
{
    /* If the delays have been computed to all be negatives, which means they
       start at either one extremity or the other of the probe, depending on
       the angle of the plane wave.

      Input parameters:
      =================

      pos_elements:    The positions of the probe elements.

      nb_e:            The number of probe elements.

      angle:           The angle for this plane wave (in radians).

      Return value:
      =============
      The relative x to use, here one side or the other of the probe based on
      the sign of the angle.
    */
    if (angle >= 0) {
        return pos_elements[0];
    } else {
        return pos_elements[nb_e - 1];
    }
}


__device__ float negative_tilt(const float *pos_elements,
                               const int nb_e,
                               const float angle)
{
    /* If the delays have been computed to all be positives, which means they
       start at either one extremity or the other of the probe, depending on
       the angle of the plane wave.

      Input parameters:
      =================

      pos_elements:    The positions of the probe elements.

      nb_e:            The number of probe elements.

      angle:           The angle for this plane wave (in radians).

      Return value:
      =============
      The relative x to use, here one side or the other of the probe based on
      the sign of the angle.
    */
    if (angle >= 0) {
        return pos_elements[nb_e - 1];
    } else {
        return pos_elements[0];
    }
}


__device__ float centered_tilt(const float *pos_elements,
                               const int nb_e)
{
    /* If the delays have been centered (half of them are positives, second
       half are negatives), the relative x should be computed based on the
       medium element in the probe.

      Input parameters:
      =================

      pos_elements:    The positions of the probe elements.

      nb_e:            The number of probe elements.

      Return value:
      =============
      The relative x to use, here the half of the probe.
    */
    float probe_width = pos_elements[nb_e - 1] - pos_elements[0];
    return pos_elements[nb_e - 1] - probe_width / 2;
}


__device__ float get_transmit_delays(const float x,
                                     const float z,
                                     const float *pos_elements,
                                     const int nb_e,
                                     const float angle,
                                     const int transmit_method)
{
    /* The factory for the plane-waves transmission method. It is expected
       transmit_method to be either 0 (delays centers at 0), 1 (all delays are
       negatives), or 2 (all delays are positives). Note that Picmus data is of
       the first option (transmit_method = 0), and Vera / PA2 of the latter
       (transmit_method = 2).

      Input parameters:
      =================

      x:               The x position of the pixel in the scan.

      z:               The z position of the pixel in the scan.

      pos_elements:    The positions of the probe elements.

      nb_e:            The number of probe elements.

      angle:           The angle for this plane wave (in radians).

      transmit_method: The transmission method to use (can be 0 (picmus), 1
                       (negative delays) or 2 (Vera / PA2)).

      Return value:
      =============
      The transmitting distance (/!\ distance, not delays, still need to be
      divided by sound_speed later to get delays).
    */
    float ref_x = 0;
    switch(transmit_method) {
    case 0:
        ref_x = centered_tilt(pos_elements, nb_e);
        break;
    case 1:
        ref_x = negative_tilt(pos_elements, nb_e, angle);
        break;
    case 2:
        ref_x = positive_tilt(pos_elements, nb_e, angle);
        break;
    }
    return sin(angle) * (x - ref_x) + cos(angle) * z;
}
