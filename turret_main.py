# turret_main.py
import math
import time
import json
import multiprocessing

from Stepper_Lab8_3 import Stepper
from shifter import Shifter

MY_TEAM_ID = 1   # change later when you know your team number


# -------------------------
#  COORDINATE MATH
# -------------------------
def polar_to_cart(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def compute_aim_angles(my_r, my_theta, t_r, t_theta, t_z):
    my_x, my_y = polar_to_cart(my_r, my_theta)
    my_z = 0.0

    tx, ty = polar_to_cart(t_r, t_theta)
    tz = t_z

    dx = tx - my_x
    dy = ty - my_y
    dz = tz - my_z

    az = math.atan2(dy, dx)
    horiz_dist = math.hypot(dx, dy)
    el = math.atan2(dz, horiz_dist)

    return math.degrees(az), math.degrees(el)


# -------------------------
#  MAIN TURRET PROGRAM
# -------------------------
def main():
    # Required for your Stepper class
    Stepper.shifter_outputs = multiprocessing.Value('i', 0)

    # Shift register on Pi
    s = Shifter(data=16, latch=20, clock=21)

    # each motor needs its own lock so they can run simultaneously
    lock_az = multiprocessing.Lock()
    lock_el = multiprocessing.Lock()

    # Create 2 motors: azimuth + elevation
    m_az = Stepper(s, lock_az)
    m_el = Stepper(s, lock_el)

    # During calibration you will manually aim and press zero()
    m_az.zero()
    m_el.zero()

    # Load FAKE JSON for now
    with open("field_coords.json", "r") as f:
        data = json.load(f)

    # Your turret's position
    me = data["turrets"][str(MY_TEAM_ID)]
    my_r = me["r"]
    my_theta = me["theta"]

    # Aim at all globes
    for globe in data["globes"]:
        t_r = globe["r"]
        t_theta = globe["theta"]
        t_z = globe["z"]

        az_deg, el_deg = compute_aim_angles(my_r, my_theta, t_r, t_theta, t_z)

        print(f"Aiming at globe: AZ={az_deg:.2f}, EL={el_deg:.2f}")

        # Move both motors at once
        m_az.goAngle(az_deg)
        m_el.goAngle(el_deg)

        # crude wait for now
        time.sleep(5)

        # Later: add laser on for 3 seconds here

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting turret.")


if __name__ == "__main__":
    main()

