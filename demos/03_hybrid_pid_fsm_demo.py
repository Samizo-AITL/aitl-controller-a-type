import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

from controllers.fsm import FSMController
from controllers.pid import PIDController
from controllers.hybrid import HybridController


def main():
    DATA = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(DATA, exist_ok=True)

    dt = 0.01

    pid_map = {
        "normal": PIDController(1.0, 0.5, 0.01, dt=dt),
        "high":   PIDController(2.0, 0.3, 0.05, dt=dt),
        "low":    PIDController(0.5, 0.2, 0.00, dt=dt),
    }

    transitions = {
        "normal": [
            (lambda e: e > 1.0, "high"),
            (lambda e: e < -1.0, "low"),
        ],
        "high": [(lambda e: e < 0.5, "normal")],
        "low":  [(lambda e: e > -0.5, "normal")],
    }

    states = {k: None for k in pid_map.keys()}
    fsm = FSMController(states, transitions, "normal")
    hybrid = HybridController(fsm, pid_map)

    setpoint = 1.0
    x = 0.0
    xs, us, states_hist, ts = [], [], [], []

    for i in range(1000):
        t = i * dt
        error = setpoint - x
        u, state = hybrid.step(error)
        x += (u - x) * dt

        xs.append(x)
        us.append(u)
        states_hist.append(state)
        ts.append(t)

    fig = plt.figure(figsize=(9, 4))
    plt.plot(ts, xs)
    plt.axhline(setpoint, linestyle="--", color="gray")
    plt.title("Hybrid PID × FSM Response")

    out_graph = os.path.join(DATA, "hybrid_response.png")
    fig.savefig(out_graph)

    out_csv = os.path.join(DATA, "hybrid_states.csv")
    with open(out_csv, "w") as f:
        for t, s in zip(ts, states_hist):
            f.write(f"{t:.4f},{s}\n")

    print("Saved", out_graph)
    print("Saved", out_csv)


if __name__ == "__main__":
    main()
