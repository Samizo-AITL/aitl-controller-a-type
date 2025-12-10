import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt
from controllers.pid import PIDController


def main():
    DATA = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(DATA, exist_ok=True)

    dt = 0.01
    pid = PIDController(1.2, 0.8, 0.05, dt=dt)

    setpoint = 1.0
    x = 0.0
    xs, ts = [], []

    for i in range(1000):
        t = i * dt
        error = setpoint - x
        u = pid.step(error)
        x += (u - x) * dt
        xs.append(x)
        ts.append(t)

    fig = plt.figure()
    plt.plot(ts, xs)
    plt.axhline(setpoint, linestyle="--", color="gray")
    plt.title("PID Step Response")

    out = os.path.join(DATA, "pid_step_response.png")
    fig.savefig(out)
    print("Saved", out)


if __name__ == "__main__":
    main()
