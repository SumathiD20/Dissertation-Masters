import numpy as np
import pandas as pd
from pydp.algorithms.laplacian import LaplaceMechanism

def obfuscate_temperature_data(raw_data, epsilon=0.5, window_size=5):
    """
    Obfuscates temperature data using differential privacy (Laplace noise)
    and temporal aggregation to hide door events while preserving trends.
    
    Args:
        raw_data: 2D numpy array of shape (18, N) - 18 probes over N time steps
        epsilon: Privacy parameter (lower = stronger privacy)
        window_size: Rolling window size for temporal aggregation
        
    Returns:
        obfuscated_data: 2D numpy array of shape (18, N) with protected data
    """
    num_probes, num_timesteps = raw_data.shape
    obfuscated_data = np.zeros((num_probes, num_timesteps))
    
    # Initialize Laplace Mechanism with privacy budget
    lm = LaplaceMechanism(epsilon=epsilon)
    
    for i in range(num_probes):
        probe_data = raw_data[i, :]
        
        # Step 1: Apply Laplace noise to each reading
        noisy_data = np.array([lm.quick_result(val) for val in probe_data])
        
        # Step 2: Temporal aggregation using rolling mean
        series = pd.Series(noisy_data)
        aggregated = series.rolling(window=window_size, min_periods=1).mean().values
        
        obfuscated_data[i, :] = aggregated
        
    return obfuscated_data

# Example usage
if __name__ == "__main__":
    # Simulated data: 18 probes, 100 time steps (20-25°C baseline)
    np.random.seed(42)
    base_temps = np.random.uniform(20, 25, (18, 100))
    
    # Add door event (sudden drop at t=50)
    door_event = base_temps.copy()
    door_event[:, 50:55] = door_event[:, 50:55] - 3.0  # 3°C drop
    
    # Obfuscate data
    protected_data = obfuscate_temperature_data(door_event, epsilon=0.5, window_size=5)
    
    # Compare results
    print("Raw data with door event:", door_event[0, 48:53])
    print("Obfuscated data:", protected_data[0, 48:53])