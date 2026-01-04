from __future__ import annotations
import math
import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Plant: RL current dynamics (V -> I)
# ============================================================
class RLPlant:
    def __init__(self, L_h: float, R0_ohm: float, v_max: float):
        self.L = L_h
        self.R0 = R0_ohm
        self.v_max = v_max
        self.I = 0.0

    def reset(self, I0: float = 0.0):
        self.I = I0

    def R_of_t(self, t, R_step_time, R_step_ratio, R_ramp):
        R = self.R0
        if t >= R_step_time:
            R = self.R0 * (1.0 + R_step_ratio)
        R *= (1.0 + R_ramp * t)
        return R

    def step(self, V_cmd, t, dt, R_step_time, R_step_ratio, R_ramp, I_dist):
        V = float(np.clip(V_cmd, -self.v_max, self.v_max))
        R = self.R_of_t(t, R_step_time, R_step_ratio, R_ramp)
        self.I += ((V - R * self.I) / self.L) * dt
        self.I += I_dist
        return self.I, V, R


# ============================================================
# PID
# ============================================================
class PID:
    def __init__(self, kp, ki, kd, dt, u_min, u_max):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.dt = dt
        self.u_min, self.u_max = u_min, u_max
        self.ei = 0.0
        self.ep = 0.0

    def set_gains(self, kp=None, ki=None, kd=None):
        if kp is not None: self.kp = kp
        if ki is not None: self.ki = ki
        if kd is not None: self.kd = kd

    def update(self, e):
        self.ei += e * self.dt
        de = (e - self.ep) / self.dt
        self.ep = e
        u = self.kp * e + self.ki * self.ei + self.kd * de
        return float(np.clip(u, self.u_min, self.u_max))


# ============================================================
# FSM
# ============================================================
class ErrorFSM:
    def __init__(self, e_hi, e_lo, hold_s, dt):
        self.e_hi, self.e_lo = e_hi, e_lo
        self.hold = int(hold_s / dt)
        self.mode = "normal"
        self.cnt = 0

    def update(self, e):
        if self.cnt > 0:
            self.cnt -= 1
            return self.mode
        ae = abs(e)
        if self.mode == "normal" and ae >= self.e_hi:
            self.mode = "high"
            self.cnt = self.hold
        elif self.mode == "high" and ae <= self.e_lo:
            self.mode = "normal"
            self.cnt = self.hold
        return self.mode


# ============================================================
# LLM-like tuner (deterministic)
# ============================================================
class KpTuner:
    def __init__(self, kp_min, kp_max, step):
        self.kp_min, self.kp_max, self.step = kp_min, kp_max, step

    def update(self, kp, mode):
        if mode == "high":
            return min(self.kp_max, kp + self.step)
        return max(self.kp_min, kp - 0.5 * self.step)


# ============================================================
# Profiles
# ============================================================
def Iref(t):
    if t < 0.6: return 0.0
    if t < 3.0: return 1.2
    return 1.6


def disturb(t):
    if 2.0 <= t < 2.12:
        return -0.05
    if 3.6 <= t < 4.4:
        return 0.006 * math.sin(2 * math.pi * 18 * t)
    return 0.0


# ============================================================
# Simulation
# ============================================================
def run_case(name, T, dt, plant_p, pid_n, pid_h, fsm_p, tuner_p):
    n = int(T / dt)
    t = np.linspace(0, T, n)

    plant = RLPlant(plant_p["L_h"], plant_p["R0_ohm"], plant_p["v_max"])
    pid = PID(*pid_n, dt, -plant_p["v_max"], plant_p["v_max"])
    fsm = ErrorFSM(dt=dt, **fsm_p)
    tuner = KpTuner(**tuner_p) if tuner_p else None

    I = np.zeros(n)
    e = np.zeros(n)
    kp = np.zeros(n)
    mode = np.zeros(n)

    for k in range(n):
        e[k] = Iref(t[k]) - plant.I
        m = "normal" if name == "Fixed PID" else fsm.update(e[k])

        if m == "high":
            pid.set_gains(*pid_h)
        else:
            pid.set_gains(*pid_n)

        if tuner:
            pid.set_gains(kp=tuner.update(pid.kp, m))

        V = pid.update(e[k])
        plant.step(V, t[k], dt,
                   plant_p["R_step_time"],
                   plant_p["R_step_ratio"],
                   plant_p["R_ramp_per_s"],
                   disturb(t[k]))

        I[k] = plant.I
        kp[k] = pid.kp
        mode[k] = 1 if m == "high" else 0

    return t, I, e, kp, mode


# ============================================================
# MAIN
# ============================================================
def main():
    T, dt = 6.0, 0.001

    plant_p = dict(
        L_h=0.08, R0_ohm=1.2, v_max=6.0,
        R_step_time=2.4, R_step_ratio=0.75, R_ramp_per_s=0.03
    )

    pid_n = (2.2, 12.0, 0.0)
    pid_h = (3.6, 16.0, 0.0)

    fsm_p = dict(e_hi=0.18, e_lo=0.08, hold_s=0.18)
    tuner_p = dict(kp_min=1.6, kp_max=7.0, step=0.25)

    cases = [
        ("Fixed PID", None),
        ("PID×FSM", None),
        ("AITL", tuner_p),
    ]

    results = [run_case(n, T, dt, plant_p, pid_n, pid_h, fsm_p, t) for n, t in cases]

    # ---------- plot ----------
    fig, axes = plt.subplots(4, 3, figsize=(14, 9), sharex=True)

    for c, (name, _) in enumerate(cases):
        t, I, e, kp, mode = results[c]
        axes[0, c].plot(t, [Iref(x) for x in t], "--")
        axes[0, c].plot(t, I)
        axes[0, c].set_title(name)

        axes[1, c].plot(t, e)
        axes[2, c].plot(t, mode)
        axes[3, c].plot(t, kp)

        for r in range(4):
            axes[r, c].grid(True, alpha=0.3)
            axes[r, c].axvline(2.0, ls="--")
            axes[r, c].axvline(plant_p["R_step_time"], ls="--")

    axes[0, 0].set_ylabel("I [A]")
    axes[1, 0].set_ylabel("e [A]")
    axes[2, 0].set_ylabel("FSM")
    axes[3, 0].set_ylabel("Kp")
    axes[3, 0].set_xlabel("t [s]")

    fig.suptitle("V–I Current Control Sales Demo (aging + disturbance)")

    os.makedirs("data", exist_ok=True)
    out = "data/12_vi_current_control_sales_demo.png"
    fig.savefig(out, dpi=160, bbox_inches="tight")
    print(f"[saved] {out}")

    plt.show()


if __name__ == "__main__":
    main()
