/* The interpolation methods, can be used to convert the hyperbolic delays into
their related data using some interpolation method. Two ways are implemented
here:
- 0: no interpolation (we're taking the closest value)
- 1: linear interpolation, using the two closest values to determine an in
between appropriated value
*/


template <class T>
__device__ T no_interpolation(const T *data,
                              const int base_idx,
                              const float data_idx,
                              const int nb_t)
{
    /* No interpolation method. Finds the closest value.

      Input parameters:
      =================

      data:     The RFs or IQs data.

      base_idx: The base index for the time samples vector. The data we are
                looking for is theoretically data[base_idx + data_idx].

      data_idx: The 'real' index of the time sample, might not exist, need to
                be interpolated.

      nb_t:     The number of time samples.

      Return value:
      =============
      The interpolated value we've extracted from the data.
    */
    int closest = round(data_idx);
    if (0 <= closest && closest < nb_t) {
        return data[base_idx + closest];
    } else {
        return 0.;
    }
}


template <class T>
__device__ T linear_interpolation(const T *data,
                                  const int base_idx,
                                  const float data_idx,
                                  const int nb_t)
{
    /* Linear interpolation method. Finds the two bound values, and return an
       in-between interpolation.

      Input parameters:
      =================

      data:     The RFs or IQs data.

      base_idx: The base index for the time samples vector. The data we are
                looking for is theoretically data[base_idx + data_idx].

      data_idx: The 'real' index of the time sample, might not exist, need to
                be interpolated.

      nb_t:     The number of time samples.

      Return value:
      =============
      The interpolated value we've extracted from the data.
    */
    int idx = int(data_idx);
    if (idx >= 0 && idx < (nb_t - 1)) {
        T dl = data[base_idx + idx];
        T du = data[base_idx + idx + 1];
        T t = data_idx - idx;
        return dl * (T(1) - t) + du * t;
    } else {
        return 0.;
    }
}


template <class T>
__device__ T interpolate(const T *data,
                         const int base_idx,
                         const float data_idx,
                         const int nb_t,
                         const int interpolation_method)
{
    /* The factory for the interpolation method. It is expected
       interpolation_method to be either 0 (no interpolation) or 1 (linear).
       Additional interpolations could be implemented (and have in CPU), but
       ended up to be a bit too much time-consuming for the observed gain of
       resolution.

      Input parameters:
      =================

      data:                 The RFs or IQs data.

      base_idx:             The base index for the time samples vector. The
                            data we are looking for is theoretically
                            data[base_idx + data_idx].

      data_idx:             The 'real' index of the time sample, might not
                            exist, need to be interpolated.

      nb_t:                 The number of time samples.

      interpolation_method: The interpolation method to use (can be 0 (no
                            interpolation) or 1 (linear)).

      Return value:
      =============
      The interpolated value we've extracted from the data.
    */
     switch(interpolation_method) {
     case 0:
         return no_interpolation(data, base_idx, data_idx, nb_t);
         break;
     case 1:
         return linear_interpolation(data, base_idx, data_idx, nb_t);
         break;
     }
     return 0.;
}
