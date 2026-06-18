# Fire Detection Drone

A Gazebo + PX4 SITL simulation of an autonomous quadcopter that surveys an area, scans for fire using a simulated thermal camera, and logs GPS-tagged fire alerts.

## World and drone design

**World** (`gazebo_worlds/testworldo2.sdf`): a flat grass terrain (`gazebo_models/world1`) with six animated flame meshes (`gazebo_models/fire_ani`) placed in a tight cluster at varying heights. Each flame is tagged with a thermal emission plugin set to 1200 K, so it reads as a strong heat source to a thermal sensor even though it's visually just a small flame mesh.

**Drone** (`gazebo_models/x500_TC`): a standard PX4 X500 quadcopter frame with a small thermal camera module (`gazebo_models/thermal_camera`) rigidly bolted underneath it via a fixed joint. The camera publishes 320x240 8-bit thermal images at 30 Hz, clamped to a 253.15-673.15 K range, so it can pick up the fire's heat signature against the cooler background terrain.

## Installation and setup

1. Install [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) and run its `Tools/setup/ubuntu.sh` script to get the full SITL toolchain.
2. Install Gazebo Harmonic (gz-sim 8.x) — required because the thermal camera sensor only renders on the ogre2 backend that ships with Harmonic.
3. Install Python 3 and the MAVSDK client:
```bash
   pip install mavsdk
```
4. Clone this repository and point Gazebo at its model and world folders:
```bash
   git clone https://github.com/saleh777-777/fire-detection-drone.git
   cd fire-detection-drone
   export GZ_SIM_RESOURCE_PATH=$PWD/gazebo_models:$PWD/gazebo_worlds:$GZ_SIM_RESOURCE_PATH
```

## Launch commands

Start PX4 SITL with the drone model and custom world:
```bash
PX4_GZ_WORLD=testworldo2 PX4_SYS_AUTOSTART=4001 PX4_SIM_MODEL=gz_x500_TC PX4_GZ_MODEL_POSE="0,0,2,0,0,0"~ ./build/px4_sitl_default/bin/px4
```
