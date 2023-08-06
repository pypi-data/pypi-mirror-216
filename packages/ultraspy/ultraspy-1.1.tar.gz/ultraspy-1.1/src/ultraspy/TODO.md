- [ ]: flip_old should be removed in filtfilt_routine   
- [ ]: GPU matched filter doesn't work properly on tests for chirps
       duration (few consecutive tests, works fine on one only)  
- [ ]: Could check out the computation time for FDMAS with empty arrays
       for delays  
- [ ]: Add the compute_delays to the init.py  
- [ ]: Maybe more in cpu tho, but should add the generate wsw / chirp signal
       methods  
- [ ]: The FWHM and PSL metrics should always return details  
- [ ]: Test the delays on convex probes, only using delays from data so far,
       never computed them using angles, should be the same as MUST  
- [ ]: Compute 3D delays if only angles are provided (will probably never
       be used tho, but shouldn't be too long)  
- [ ]: Add a wrapper in Reader to handle the exception if the file can't be
       loaded, then set it within the GUI  
