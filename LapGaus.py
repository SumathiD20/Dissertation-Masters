import numpy as np

# Reproducible run
np.random.seed(42)

# Generate 100 synthetic temperature readings between 22°C and 30°C
original = np.random.uniform(22, 30, 100)

# Gaussian noise parameters
sigma = 0.5
gauss_noise = np.random.normal(0, sigma, 100)
gauss_noisy = original + gauss_noise

# Laplace noise parameters
laplace_scale = sigma
lap_noise = np.random.laplace(0, laplace_scale, 100)
lap_noisy = original + lap_noise

# Compute mean absolute errors
gauss_mae = np.mean(np.abs(gauss_noisy - original))
lap_mae = np.mean(np.abs(lap_noisy - original))

print(f"Mean Absolute Error (Gaussian): {gauss_mae:.3f} °C")
print(f"Mean Absolute Error (Laplace):  {lap_mae:.3f} °C")
