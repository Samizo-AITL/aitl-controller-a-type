import os, sys, time
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# PATH SETTINGS
# -------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ROOT)

from controllers.fsm import FSMController
from controllers.pid import PIDController
from controllers.hybrid import HybridController
from models.llm import AITLLLM


def main():
    print("Running AITL Full Demo (IDEAL)…")

    DATA = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(DATA, exist_ok=True)

    dt = 0.01
    sim_time = 20
    steps = int(sim_time / dt)
    INIT_FREEZE = 2.0

    # -------------------------------------------------
    # PID Gains
    # -------------------------------------------------
    pid_map = {
        "normal": PIDController(1.0, 0.4, 0.01, dt),
        "high":   PIDController(3.2, 0.4, 0.08, dt),
    }

    # -------------------------------------------------
    # FSM (hysteresis)
    # -------------------------------------------------
    transitions = {
        "normal": [(lambda e: abs(e) > 0.40, "high")],
        "high":   [(lambda e: abs(e) < 0.18, "normal")],
    }

    states = {k: None for k in pid_map}
    fsm = FSMController(states, transitions, "normal")
    hybrid = HybridController(fsm, pid_map)

    # LLM
    llm = AITLLLM()

    # -------------------------------------------------
    # Simulation variables
    # -------------------------------------------------
    setpoint = 1.0
    x = 0.0

    xs, ts, fsm_hist = [], [], []
    kp_log = {s: [] for s in pid_map}

    disturbance = {
        500: +0.8,
        1500: -1.0,
    }

    # -------------------------------------------------
    # Simulation loop
    # -------------------------------------------------
    for i in range(steps):
        t = i * dt
        error = setpoint - x

        if t > INIT_FREEZE:
            hybrid.fsm.update_state(error, t)
        state = hybrid.fsm.current_state

        u = pid_map[state].step(error)

        if i in disturbance:
            x += disturbance[i]

        tau = 0.18
        x += (u - x) * dt / tau

        pid_map[state].kp = llm.adjust(state, pid_map[state].kp, error)

        xs.append(x)
        ts.append(t)
        fsm_hist.append(1 if state == "high" else 0)
        for s in pid_map:
            kp_log[s].append(pid_map[s].kp)

    # -------------------------------------------------
    # Plot (教材仕上げ版)
    # -------------------------------------------------
    fig, ax = plt.subplots(3, 1, figsize=(11, 12), sharex=True)

    # ==========================
    # 1. System Response
    # ==========================
    ax[0].plot(ts, xs, label="x(t)", color="#0060C0", linewidth=2.0)
    ax[0].axhline(1.0, ls="--", color="#888888", label="reference r")

    for k in disturbance:
        td = k * dt
        ax[0].axvline(td, color="red", ls="--", alpha=0.8)
        ax[0].text(td, 1.45, "disturb", color="red")

    ax[0].grid(alpha=0.4)
    ax[0].set_title("System Response + A-type LLM", fontsize=13)
    ax[0].legend()

    # ==========================
    # 2. FSM States
    # ==========================
    ax[1].step(ts, fsm_hist, where="post", color="#2040FF", linewidth=2.5)
    ax[1].set_yticks([0, 1])
    ax[1].set_yticklabels(["normal", "high"])
    ax[1].grid(alpha=0.4)
    ax[1].set_title("FSM States", fontsize=13)

    # FSM 判別用の境界線
    fsm_arr = np.array(fsm_hist)
    for i in range(1, len(fsm_arr)):
        if fsm_arr[i] != fsm_arr[i - 1]:
            ax[1].axvline(ts[i], color="gray", ls="--", alpha=0.5)

    # ==========================
    # 3. Kp (state-dependent)
    # ==========================
    kp_normal_plot = np.where(fsm_arr == 0, kp_log["normal"], np.nan)
    kp_high_plot   = np.where(fsm_arr == 1, kp_log["high"],   np.nan)

    ax[2].step(ts, kp_normal_plot, where="mid",
               label="kp[normal]", color="#0070FF", linewidth=3)
    ax[2].step(ts, kp_high_plot, where="mid",
               label="kp[high]", color="#FF8000", linewidth=3)

    # FSM境界線（Kpプロットにも重ねる）
    for i in range(1, len(fsm_arr)):
        if fsm_arr[i] != fsm_arr[i - 1]:
            ax[2].axvline(ts[i], color="gray", ls="--", alpha=0.5)

    ax[2].grid(alpha=0.4)
    ax[2].legend(loc="lower right")
    ax[2].set_title("LLM Adjusted kp (state-dependent)", fontsize=13)

    # Save
    out = os.path.join(DATA, f"aitl_full_demo_ideal_{int(time.time())}.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print("Saved to:", out)


if __name__ == "__main__":
    main()
