# demos/15_fsm_explainability_demo.py
# ------------------------------------------------------------
# FSM Explainability Demo
# Purpose:
#  - Show WHY FSM switched modes
#  - Provide time-stamped, human-readable reasons
#
# Output:
#  - console log (reasoned transitions)
#  - PNG figure for portal / sales material
# ------------------------------------------------------------
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import os


# ============================
# Minimal plant (V -> I)
# ============================
class RLPlant:
    def __init__(self, L, R, v_max):
        self.L = L
        self.R = R
        self.v_max = v_max
        self.I = 0.0

    def reset(self):
        self.I = 0.0

    def step(self, V, dt):
        V = float(np.clip(V, -self.v_max, self.v_max))
        self.I += ((V - self.R * self.I) / self.L) * dt
        return self.I


# ============================
# PID
# ============================
class PID:
    def __init__(self, kp, ki, dt, u_lim):
        self.kp = kp
        self.ki = ki
        self.dt = dt
        self.u_lim = u_lim
        self.ei = 0.0

    def update(self, e):
        self.ei += e * self.dt
        u = self.kp * e + self.ki * self.ei
        return float(np.clip(u, -self.u_lim, self.u_lim))


# ============================
# Explainable FSM
# ============================
class ExplainableFSM:
    def __init__(self, e_hi, e_lo):
        self.e_hi = e_hi
        self.e_lo = e_lo
        self.mode = "normal"
        self.logs = []

    def reset(self):
        self.mode = "normal"
        self.logs = []

    def update(self, e, t):
        ae = abs(e)

        if self.mode == "normal" and ae >= self.e_hi:
            self.mode = "high"
            self.logs.append(
                f"[t={t:.3f}s] normal → high : |e|={ae:.3f} ≥ e_hi={self.e_hi:.3f}"
            )

        elif self.mode == "high" and ae <= self.e_lo:
            self.mode = "normal"
            self.logs.append(
                f"[t={t:.3f}s] high → normal : |e|={ae:.3f} ≤ e_lo={self.e_lo:.3f}"
            )

        return self.mode


# ============================
# Scenario
# ============================
def Iref(t):
    if t < 0.5:
        return 0.0
    elif t < 2.0:
        return 1.0
    else:
        return 1.4


def disturbance(t):
    if 1.2 <= t < 1.35:
        return -0.06
    return 0.0


# ============================
# Main demo
# ============================
def main():
    T = 4.0
    dt = 0.001
    n = int(T / dt)
    t = np.linspace(0, T, n)

    plant = RLPlant(L=0.08, R=1.3, v_max=6.0)
    pid_n = PID(kp=2.2, ki=10.0, dt=dt, u_lim=6.0)
    pid_h = PID(kp=3.8, ki=12.0, dt=dt, u_lim=6.0)

    fsm = ExplainableFSM(e_hi=0.18, e_lo=0.08)

    I = np.zeros(n)
    e = np.zeros(n)
    mode = np.zeros(n)

    plant.reset()
    fsm.reset()

    for k in range(n):
        ref = Iref(t[k])
        e[k] = ref - plant.I

        m = fsm.update(e[k], t[k])
        if m == "high":
            V = pid_h.update(e[k])
            mode[k] = 1.0
        else:
            V = pid_n.update(e[k])
            mode[k] = 0.0

        plant.step(V, dt)
        plant.I += disturbance(t[k])
        I[k] = plant.I

    # ============================
    # Explainability log
    # ============================
    print("=== FSM Transition Log (Explainability Evidence) ===")
    if not fsm.logs:
        print("No FSM transitions occurred.")
    else:
        for line in fsm.logs:
            print(line)

    # ============================
    # Plot
    # ============================
    fig, ax = plt.subplots(3, 1, figsize=(9, 7), sharex=True)

    ax[0].plot(t, [Iref(x) for x in t], "--", label="Iref")
    ax[0].plot(t, I, label="I")
    ax[0].set_ylabel("I [A]")
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    ax[1].plot(t, e)
    ax[1].set_ylabel("e = Iref − I [A]")
    ax[1].grid(True, alpha=0.3)

    ax[2].plot(t, mode)
    ax[2].set_ylabel("FSM (high=1)")
    ax[2].set_xlabel("t [s]")
    ax[2].grid(True, alpha=0.3)

    fig.suptitle("FSM Explainability Demo: Why the mode switched", fontsize=13)

    plt.tight_layout()

    # ============================
    # Save PNG (portal-ready)
    # ============================
    os.makedirs("data", exist_ok=True)
    out_png = "data/15_fsm_explainability_demo.png"
    plt.savefig(out_png, dpi=160, bbox_inches="tight")
    print(f"[saved] {out_png}")

    plt.show()


if __name__ == "__main__":
    main()
