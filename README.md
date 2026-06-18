Fire Detection Drone

A Gazebo + PX4 SITL simulation of an autonomous quadcopter that surveys an area, scans for fire using a simulated thermal camera, and logs GPS-tagged fire alerts.

How it works

Drone: a PX4 X500 quadcopter (x500_TC) with an 8-bit thermal camera rigidly mounted underneath it.

World: a custom Gazebo world (testworldo2.sdf) containing a ground terrain (world1) and six animated flame meshes (fire_ani) placed in a cluster,
each tagged with a thermal emission temperature of 1200 K so they show up "hot" to the thermal sensor.

Mission script (projectfire.py): connects to PX4 over MAVSDK, arms and takes off the drone to 12 m,
then uploads and flies an outward spiral search pattern centered on the home position
(2 loops, 16 points per loop, expanding out to roughly a 0.0002-degree radius) while
running a detection loop in parallel that checks for fire readings at each telemetry tick.

Alerts: whenever a reading crosses the temperature/confidence threshold, the drone's current latitude, longitude,
altitude, temperature, and confidence are appended to fire_alert(project1).csv. Once the survey mission completes,
the drone automatically returns to launch and lands.
