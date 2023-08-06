/* Methods to compute the distances to a probe, either in 2D or 3D.
*/


__device__ void get_distances(const float *probe,
                              const int nb_transmissions,
                              const int nb_elements,
                              const int idx_transmission,
                              const int idx_element,
                              const float x,
                              const float y,
                              const float z,
                              float *dist_to_x,
                              float *dist_to_y,
                              float *dist_to_pixel)
{
    /* Computes the distance of a probe element to a pixel, and also to the
       projection of this pixel in the meridional plane.

      Input parameters:
      =================

      probe:            The probe array with the three dimensions, all the
                        transmissions, then all the elements, of shape
                        (3, nb_t, nb_e).

      nb_transmissions: The number of transmissions of the sequence.

      nb_elements:      The number of transmissions of the probe.

      idx_transmission: The current index of the transmission.

      idx_element:      The current index of the probe element.

      x:                The x position of the pixel to observe.

      y:                The y position of the pixel to observe.

      z:                The z position of the pixel to observe.

      dist_to_x:        The distance to the x location to the probe element,
                        at a depth = 0.

      dist_to_y:        The distance to the y location to the probe element,
                        at a depth = 0.

      dist_to_pixel:    The distance to the pixel at (x, y, z).
    */
    int base_probe = nb_transmissions * nb_elements;
    int lat_base = 0 * base_probe + idx_transmission * nb_elements;
    int ele_base = 1 * base_probe + idx_transmission * nb_elements;
    int axi_base = 2 * base_probe + idx_transmission * nb_elements;
    float x_diff = x - probe[lat_base + idx_element];
    float y_diff = y - probe[ele_base + idx_element];
    float z_diff = z - probe[axi_base + idx_element];

    *dist_to_x = x_diff;
    *dist_to_y = y_diff;
    *dist_to_pixel = sqrt(x_diff * x_diff +
                          y_diff * y_diff +
                          z_diff * z_diff);
}
