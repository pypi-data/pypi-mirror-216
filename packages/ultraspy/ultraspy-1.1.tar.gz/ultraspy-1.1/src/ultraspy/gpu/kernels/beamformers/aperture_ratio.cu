/* The methods to compute the apertures ratio based on probe geometry.
*/


__device__ float get_aperture_ratio(const float z,
                                    const float x_diff,
                                    const float y_diff,
                                    const float dist,
                                    const float theta,
                                    const float *f_number)
{
    /* Returns the ratio telling if the element is within the aperture of the
       probe element. This is normalized, everything between [-1, 1] is within
       aperture, outside else case.

      Input parameters:
      =================

      z:         The axial distance of the point

      x_diff:    The lateral difference between the point and the probe elements

      y_diff:    The elevational difference between the point and the probe
                 elements

      dist:      The cartesian distance between the point and the probe elements

      theta:     The theta of the probe element (0 if linear)

      f_number:  The f number, full aperture if = 0. Two-dimensional, for both
                 the lateral and elevational axes

      Return value:
      =============
      The ratio of the aperture, within if [-1, 1], outside else case
    */
    if (f_number[0] <= 0 || f_number[1] <= 0) {
        return 0.;
    }

    else if (theta != 0) {
        float aperture = atan(1. / (2. * f_number[0]));
        return (asin(x_diff / dist) - theta) / aperture;
    }

    else {
        float aperture1 = abs(x_diff) / (z / (2 * f_number[0]));
        float aperture2 = abs(y_diff) / (z / (2 * f_number[1]));
        return max(aperture1, aperture2);
    }
}
