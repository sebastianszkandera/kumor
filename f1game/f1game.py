import fastf1
from fastf1 import plotting
import os

# Enable caching to speed up data loading
cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
fastf1.Cache.enable_cache(cache_dir) 

# Load the session (e.g., 2024 Canadian GP Qualifying)
session = fastf1.get_session(2024, 'Canada', 'Q')
session.load()

# Get fastest lap for a driver
lap = session.laps.pick_driver('RUS').pick_fastest()

# Get telemetry for this lap
telemetry = lap.get_car_data().add_distance()

# Plot speed
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(telemetry['Distance'], telemetry['Speed'])
ax.set_title('George Russell 2024 Canada Pole Lap')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Speed (km/h)')
plt.show()
