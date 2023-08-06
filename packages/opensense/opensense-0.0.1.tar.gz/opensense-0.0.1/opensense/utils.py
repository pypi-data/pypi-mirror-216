import numpy as np
import tsmoothie
from scipy.interpolate import interp1d

denoise_dict={
    'kalman': tsmoothie.KalmanSmoother(component='level_trend', component_noise={'level':0.1, 'trend':0.1}),
    'exponential': tsmoothie.ExponentialSmoother(window_len=20, alpha=3), # recommended
    'spectral': tsmoothie.SpectralSmoother(smooth_fraction=0.2, pad_len=20), # recommended
    'convolution': tsmoothie.ConvolutionSmoother(window_len=20, window_type='ones'),
    'polynomial': tsmoothie.PolynomialSmoother(degree=5),
    'spline': tsmoothie.SplineSmoother(n_knots=6, spline_type='natural_cubic_spline'),
    'gaussian': tsmoothie.GaussianSmoother(n_knots=6, sigma=0.1),
    'binner': tsmoothie.BinnerSmoother(n_knots=6),
    'lowess': tsmoothie.LowessSmoother(smooth_fraction=0.2, iterations=1)
}

def log_info(*args):
    print ('[LOG]', ' '.join(map(str, args)))

def log_split():
    print ('===============================')

def interpolate_nan_inf(arr):
    # Get the shape of the array
    shape = arr.shape

    # Iterate over each element in the array
    for i in range(shape[0]):
        for j in range(shape[1]):
            col = arr[i, j, :]

            # Find indices of NaN and inf values
            nan_indices = np.isnan(col)
            inf_indices = np.isinf(col)

            # Create a mask to identify non-NaN and non-inf values
            mask = ~(nan_indices | inf_indices)

            # Create interpolation function using non-NaN and non-inf values
            t = np.arange(shape[2])
            interp_func = interp1d(t[mask], col[mask], kind='linear', fill_value='extrapolate')

            # Replace NaN and inf values with interpolated values
            col[nan_indices] = interp_func(t[nan_indices])
            col[inf_indices] = interp_func(t[inf_indices])

            # Update the column in the array
            arr[i, j, :] = col

    return arr