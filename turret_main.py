# turret_main.py
import math
import time
import json
import multiprocessing

from Stepper_Lab8_3 import Stepper
from shifter import Shifter  # your lab shifter

MY_TEAM_ID = 1  # change later

def polar_to_cart(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def compute_aim_angles(my_r, my_theta, target_r, target_theta, target_z):
    my_x, my_y = polar_to_cart(my_r, my_theta)
    my_z = 0.0

    tx, ty = polar_to_cart(target_r, target_theta)
    tz = target_z

    dx = tx - my_x
    dy = ty - my_y
    dz = tz - my_z

    az_rad = math.atan2(dy, dx)
    horiz_dist = math.hypot(dx, dy)
    el_rad = math.atan2(dz, horiz_dist)

    return math.degrees(az_rad), math.degrees(el_rad)

def main():
    Stepper.shifter_outputs = multiprocessing.Value('i', 0)

    s = Shifter(data=16, latch=20, clock=21)

    lock_az = multiprocessing.Lock()
    lock_el = multiprocessing.Lock()

    m_az = Stepper(s, lock_az)
    m_el = Stepper(s, lock_el)

    # for now, assume you’ve already manually aligned and called zero from somewhere
    m_az.zero()
    m_el.zero()

    # fake JSON for now
    with open("field_coords.json", "r") as f:
        data = json.load(f)

    my_r = data["turrets"][str(MY_TEAM_ID)]["r"]
    my_theta = data["turrets"][str(MY_TEAM_ID)]["theta"]

    for globe in data["globes"]:
        g_r = globe["r"]
        g_theta = globe["theta"]
        g_z = globe["z"]

        az_deg, el_deg = compute_aim_angles(my_r, my_theta, g_r, g_theta, g_z)
        print(f"Aiming at globe: az={az_deg:.1f}, el={el_deg:.1f}")

        m_az.goAngle(az_deg)
        m_el.goAngle(el_deg)
        time.sleep(5)  # wait for motors

        # TODO: laser on 3s then off using GPIO

if __name__ == "__main__":
    main()
