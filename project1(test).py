import asyncio
import random
from datetime import datetime
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
 
 
ALERT_FILE = "fire_alert(project1).csv"
mission_done = False
 
 
def check_fire(chance):
    if random.random() < chance:
        return random.uniform(100, 350), random.uniform(0.55, 0.98)
    return random.uniform(25, 40), random.uniform(0.0, 0.45)
 
 
def save_alert(lat, lon, alt, temp, conf):
    f = open(ALERT_FILE, "a")
    f.write(f"{datetime.now()},{lat},{lon},{alt},{temp},{conf}\n")
    f.close()
    print(f"Fire at {lat}, {lon} saved to {ALERT_FILE}")
 
 
def make_item(lat, lon, alt):
    return MissionItem(lat, lon, alt, 12.0, True, float('nan'), float('nan'),
                       MissionItem.CameraAction.NONE, float('nan'), float('nan'),
                       1, float('nan'), float('nan'), MissionItem.VehicleAction.NONE)
 
 
async def check_armed(drone):
    async for arming_state in drone.telemetry.armed():
        if arming_state:
            print("Armed")
            break
 
 
async def check_in_air(drone):
    async for state in drone.telemetry.landed_state():
        if state == state.IN_AIR:
            print("In air")
            break
 
 
async def detection_loop(drone):
    chance = 0.001
    while not mission_done:
        position = await anext(drone.telemetry.position())
        temp, conf = check_fire(chance)
        if temp >= 80.0 and conf >= 0.55:
            save_alert(position.latitude_deg, position.longitude_deg, position.absolute_altitude_m, temp, conf)
            chance = 0.001
        else:
            chance += 0.001
        await asyncio.sleep(1)
 
 
async def run():
    global mission_done
 
    drone = System()
    print("Connecting to PX4...")
    await drone.connect(system_address="udp://:14540")
 
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected")
            break
 
    print("Arming...")
    await drone.action.arm()
    await check_armed(drone)
 
    await drone.action.set_takeoff_altitude(10)
    print("Taking off...")
    await drone.action.takeoff()
    await check_in_air(drone)
 
    home = await anext(drone.telemetry.home())
    lat = home.latitude_deg
    lon = home.longitude_deg
    alt = 10.0
    s = 100 * 1e-5
    step = s / 8
 
    mission_items = [
        make_item(lat,          lon,     alt),
        make_item(lat,          lon + s, alt),
        make_item(lat - step,   lon + s, alt),
        make_item(lat - step,   lon,     alt),
        make_item(lat - step*2, lon,     alt),
        make_item(lat - step*2, lon + s, alt),
        make_item(lat - step*3, lon + s, alt),
        make_item(lat - step*3, lon,     alt),
        make_item(lat - step*4, lon,     alt),
        make_item(lat - step*4, lon + s, alt),
        make_item(lat - step*5, lon + s, alt),
        make_item(lat - step*5, lon,     alt),
        make_item(lat - step*6, lon,     alt),
        make_item(lat - step*6, lon + s, alt),
        make_item(lat - step*7, lon + s, alt),
        make_item(lat - step*7, lon,     alt),
        make_item(lat - step*8, lon,     alt),
        make_item(lat - step*8, lon + s, alt),
    ]
 
    mission_plan = MissionPlan(mission_items)
 
    print("Uploading mission...")
    await drone.mission.upload_mission(mission_plan)
 
    print("Starting mission...")
    await drone.mission.start_mission()
 
    asyncio.create_task(detection_loop(drone))
 
    async for progress in drone.mission.mission_progress():
        print(f"Mission progress: {progress.current}/{progress.total}")
        if progress.current == progress.total:
            print("Mission complete")
            break
 
    mission_done = True
 
    print("Returning to launch...")
    await drone.action.return_to_launch()
 
    async for state in drone.telemetry.landed_state():
        if state == state.ON_GROUND:
            print("Drone landed")
            break
 
asyncio.run(run())