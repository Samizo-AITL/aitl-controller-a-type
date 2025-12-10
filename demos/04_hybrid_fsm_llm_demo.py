import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

from controllers.fsm import FSMController
from controllers.pid import PIDController
from controllers.hybrid import HybridController
from models.llm import AITLLLM


def main():
    DATA = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(DATA, exist_ok=True)

    dt = 0.01

    # -----------------------
    # PID controllers for each state
    # -----------------------
    pid_map = {
        "normal": PIDController(1.0, 0.4, 0.01, dt=dt),
        "high":   PIDController(2.0, 0.3, 0.05, dt=dt),
        "low":    PIDController(0.5, 0.2, 0.00, dt=dt),
    }

    # -----------------------
    # FSM definition
    # -----------------------
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
    llm = AITLLLM()

    # -----------------------
    # Simulation variables
    # -----------------------
    setpoint = 1.0
    x = 0.0

    xs, us, states_hist, ts = [], [], [], []
    kp_log = {s: [] for s in pid_map}
    llm_trigger_interval = 100  # every 100 steps, LLM modifies gains

    # -----------------------
    # Simulation loop
    # -----------------------
    for i in range(1500):
        t = i * dt
        error = setpoint - x

        # Hybrid control (PID × FSM)
        u, state = hybrid.step(error)

        # Plant update (simple first-order model)
        x += (u - x) * dt

        # Log
        xs.append(x)
        us.append(u)
        states_hist.append(state)
        ts.append(t)

        # Log PID gains
        for s in pid_map:
            kp_log[s].append(pid_map[s].kp)

        # -----------------------
        # 🔥 LLMによるゲイン調整（適応制御）
        # -----------------------
        if i % llm_trigger_interval == 0 and i > 0:
            print("\n--- LLM adjusting PID gains ---")
            original = {s: {"kp": pid_map[s].kp, "ki": pid_map[s].ki, "kd": pid_map[s].kd}
                        for s in pid_map}

            new_params = llm.analyze_and_adjust(original)

            for s in pid_map:
                pid_map[s].kp = new_params[s]["kp"]

            print("LLM updated gains:", new_params)

    # -----------------------
    # Plotting
    # -----------------------
    fig, ax = plt.subplots(3, 1, figsize=(10, 10))

    # 1. Output response
    ax[0].plot(ts, xs)
    ax[0].axhline(setpoint, ls="--", color="gray")
    ax[0].set_title("System Response")

    # 2. State transitions
    ax[1].plot(ts, states_hist)
    ax[1].set_title("FSM State")

    # 3. LLM-adjusted kp changes
    for s, log in kp_log.items():
        ax[2].plot(ts, log, label=f"kp[{s}]")
    ax[2].legend()
    ax[2].set_title("LLM Adjusted kp Values")

    out = os.path.join(DATA, "fsm_llm_demo.png")
    fig.savefig(out)
    print("Saved:", out)


if __name__ == "__main__":
    main()
