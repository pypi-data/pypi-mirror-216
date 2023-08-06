/* The apodization methods for the data we've got, before the reduction step
- 0: No apodization
- 1: A tukey apodization
*/


__device__ float tukey(const float normed_distance,
                       const float alpha)
{
    /* The tukey apodization window, as defined in
       https://en.wikipedia.org/wiki/Window_function.

      Input parameters:
      =================

      normed_distance: The point on which to apply the apodization, normed
                       between -1 and 1 (borders of the window).

      alpha:           The Tukey factor to apply.

      Return value:
      =============
      The weight to apply according to the Tukey formula.
    */
    float dist_to_0 = abs(normed_distance);
    if (dist_to_0 > 1) {
        return 0;
    } else if (dist_to_0 < 1 - alpha) {
        return 1;
    } else {
        return 0.5 * (1 + cos((M_PI / alpha) * (dist_to_0 - 1 + alpha)));
    }
}


__device__ float no_apodization(const float normed_distance)
{
    /* No apodization here, it's a boxcar window, weight is always 1.

      Input parameters:
      =================

      normed_distance: The point on which to apply the apodization, normed
                       between -1 and 1 (borders of the window).

      Return value:
      =============
      1, all weights are equal.
    */
    if (abs(normed_distance) > 1) {
        return 0;
    } else {
        return 1;
    }
}


__device__ float get_apodization_weight(const float normed_distance,
                                        const float factor,
                                        const int apodization_method)
{
    /* The factory for the apodization method. It is expected
       apodization_method to be either 0 (no apodization) or 1 (tukey window).
       The factor argument is the coefficient provided for the apodization
       window.

      Input parameters:
      =================

      normed_distance:      The point on which to apply the apodization,
                            normed between -1 and 1 (borders of the window).

      factor:               The factor for our apodization window.

      apodization_method:   The apodization method to use (can be 0 (no
                            apodization) or 1 (tukey)).

      Return value:
      =============
      The weight to apply according to the given apodization window.
    */
    switch(apodization_method) {
    case 0:
        return no_apodization(normed_distance);
        break;
    case 1:
        return tukey(normed_distance, factor);
        break;
    }
    return 0;
}
