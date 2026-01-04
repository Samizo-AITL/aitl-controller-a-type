# demos/13_aging_sweep_delta_t.py
# ------------------------------------------------------------
# Sales Evidence: Aging sweep -> Δt (settle time) & max|e| curves
# Plant: L dI/dt + R(t) I = V
# Compare: Fixed PID / PID×FSM / AITL
#
# Outputs:
#  - data/13_aging_sweep_delta_t.png
#  - prints summary table
# ------------------------------------------------------------
from __future__ import annotations

import math
import os
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# Plant: RL current dynamics (V -> I)
# ----------------------------
class RLPlant:
    def __init__(self, L_h: float, R0_ohm: float, v_max: float):
        self.L = float(L_h)
        self.R0 = float(R0_ohm)
        self.v_max = float(v_max)
        self.I = 0.0

    def reset(self, I0: float = 0.0):
        self.I = float(I0)

    def R_of_t(self, t: float, R_step_time: float, R_step_ratio: float, R_ramp_per_s: float) -> float:
        R = self.R0
        if t >= R_step_time:
            R = self.R0 * (1.0 + R_step_ratio)
        R *= (1.0 + R_ramp_per_s * t)
        return max(1e-6, R)

    def step(
        self,
        V_cmd: float,
        t: float,
        dt: float,
        R_step_time: float,
        R_step_ratio: float,
        R_ramp_per_s: float,
        I_disturb: float,
    ) -> tuple[float, float, float]:
        V = float(np.clip(V_cmd, -self.v_max, self.v_max))
        R = self.R_of_t(t, R_step_time, R_step_ratio, R_ramp_per_s)
        dIdt = (V - R * self.I) / self.L
        self.I += dIdt * dt
        self.I += I_disturb
        return self.I, V, R


# ----------------------------
# PID
# ----------------------------
class PID:
    def __init__(self, kp: float, ki: float, kd: float, dt: float, u_min: float, u_max: float):
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.dt = float(dt)
        self.u_min = float(u_min)
        self.u_max = float(u_max)
        self.e_int = 0.0
        self.e_prev = 0.0

    def reset(self):
        self.e_int = 0.0
        self.e_prev = 0.0

    def set_gains(self, kp: float | None = None, ki: float | None = None, kd: float | None = None):
        if kp is not None:
            self.kp = float(kp)
        if ki is not None:
            self.ki = float(ki)
        if kd is not None:
            self.kd = float(kd)

    def update(self, e: float) -> float:
        self.e_int += e * self.dt
        de = (e - self.e_prev) / self.dt
        self.e_prev = e

        u = self.kp * e + self.ki * self.e_int + self.kd * de
        u_sat = float(np.clip(u, self.u_min, self.u_max))

        # simple anti-windup
        if u != u_sat and abs(self.ki) > 1e-12:
            self.e_int *= 0.98

        return u_sat


# ----------------------------
# FSM
# ----------------------------
class ErrorFSM:
    def __init__(self, e_hi: float, e_lo: float, hold_s: float, dt: float):
        self.e_hi = float(e_hi)
        self.e_lo = float(e_lo)
        self.hold_steps = int(max(0, round(hold_s / dt)))
        self.mode = "normal"
        self.hold_counter = 0

    def reset(self):
        self.mode = "normal"
        self.hold_counter = 0

    def update(self, e: float) -> str:
        ae = abs(e)

        if self.hold_counter > 0:
            self.hold_counter -= 1
            return self.mode

        if self.mode == "normal":
            if ae >= self.e_hi:
                self.mode = "high"
                self.hold_counter = self.hold_steps
        else:  # high
            if ae <= self.e_lo:
                self.mode = "normal"
                self.hold_counter = self.hold_steps

        return self.mode


# ----------------------------
# "LLM" tuner (deterministic heuristic)
# ----------------------------
class KpTuner:
    def __init__(self, kp_min: float, kp_max: float, step: float,
                 improve_window_s: float, min_improve_ratio: float, dt: float):
        self.kp_min = float(kp_min)
        self.kp_max = float(kp_max)
        self.step = float(step)
        self.win = int(max(3, round(improve_window_s / dt)))
        self.min_improve_ratio = float(min_improve_ratio)
        self.e_hist: list[float] = []

    def reset(self):
        self.e_hist = []

    def propose_kp(self, kp_now: float, e: float, mode: str) -> float:
        self.e_hist.append(abs(e))
        if len(self.e_hist) > self.win:
            self.e_hist.pop(0)

        # act only in HIGH mode with enough history
        if mode != "high" or len(self.e_hist) < self.win:
            return kp_now

        e0 = self.e_hist[0]
        e1 = self.e_hist[-1]
        ratio = (e1 / (e0 + 1e-9))

        kp_new = kp_now
        if ratio > self.min_improve_ratio:
            kp_new = min(self.kp_max, kp_now + self.step)
        elif ratio < 0.35:
            kp_new = max(self.kp_min, kp_now - 0.5 * self.step)

        return float(kp_new)


# ----------------------------
# Reference + disturbance
# ----------------------------
def Iref_profile(t: float) -> float:
    if t < 0.6:
        return 0.0
    elif t < 3.0:
        return 1.2
    else:
        return 1.6


def disturbance_profile(t: float) -> float:
    if 2.0 <= t < 2.12:
        return -0.05
    if 3.6 <= t < 4.4:
        return 0.006 * math.sin(2 * math.pi * 18 * t) + 0.004 * math.sin(2 * math.pi * 7 * t)
    return 0.0


# ----------------------------
# Core sim: return Δt and max|e|
# ----------------------------
def simulate_metrics(
    case: str,
    T: float,
    dt: float,
    plant_params: dict,
    pid_normal: tuple[float, float, float],
    pid_high: tuple[float, float, float],
    fsm_params: dict,
    tuner_params: dict | None,
    settle_band_A: float = 0.02,
    settle_hold_s: float = 0.2,
    disturb_t0: float = 2.0,
) -> tuple[float, float]:
    n = int(round(T / dt))
    t_arr = np.linspace(0.0, T, n, endpoint=False)

    plant = RLPlant(plant_params["L_h"], plant_params["R0_ohm"], plant_params["v_max"])
    plant.reset(0.0)

    pid = PID(*pid_normal, dt=dt, u_min=-plant_params["v_max"], u_max=plant_params["v_max"])
    fsm = ErrorFSM(dt=dt, **fsm_params)

    tuner = KpTuner(dt=dt, **tuner_params) if tuner_params is not None else None
    if tuner is not None:
        tuner.reset()

    e_log = np.zeros(n)
    max_abs_e = 0.0

    for k, t in enumerate(t_arr):
        Iref = Iref_profile(t)
        e = Iref - plant.I
        e_log[k] = e
        max_abs_e = max(max_abs_e, abs(e))

        if case == "Fixed PID":
            mode = "normal"
        else:
            mode = fsm.update(e)

        if mode == "high":
            pid.set_gains(*pid_high)
        else:
            pid.set_gains(*pid_normal)

        if tuner is not None:
            pid.set_gains(kp=tuner.propose_kp(pid.kp, e, mode))

        V_cmd = pid.update(e)
        plant.step(
            V_cmd, t, dt,
            R_step_time=plant_params["R_step_time"],
            R_step_ratio=plant_params["R_step_ratio"],
            R_ramp_per_s=plant_params["R_ramp_per_s"],
            I_disturb=disturbance_profile(t),
        )

    # Δt: after disturb_t0, first time |e|<band for hold duration
    idx0 = int(round(disturb_t0 / dt))
    hold_steps = int(max(1, round(settle_hold_s / dt)))
    settle_idx = None
    for i in range(idx0, n - hold_steps):
        if np.all(np.abs(e_log[i:i + hold_steps]) < settle_band_A):
            settle_idx = i
            break

    delta_t = float("nan") if settle_idx is None else (settle_idx * dt) - disturb_t0
    return delta_t, max_abs_e


def main():
    # --- base scenario (align with 12) ---
    T = 6.0
    dt = 0.001

    base_plant = dict(
        L_h=0.08,
        R0_ohm=1.2,
        v_max=6.0,
        R_step_time=2.4,
        R_step_ratio=0.0,   # swept
        R_ramp_per_s=0.03,
    )

    pid_normal = (2.2, 12.0, 0.0)
    pid_high   = (3.6, 16.0, 0.0)

    fsm_params = dict(
        e_hi=0.18,
        e_lo=0.08,
        hold_s=0.18,
    )

    tuner_params = dict(
        kp_min=1.6,
        kp_max=7.0,
        step=0.25,
        improve_window_s=0.18,
        min_improve_ratio=0.82,
    )

    sweep = np.linspace(0.0, 1.2, 13)

    cases = [
        ("Fixed PID", None),
        ("PID×FSM", None),
        ("AITL", tuner_params),
    ]

    delta_t = np.zeros((len(sweep), len(cases)))
    max_e = np.zeros_like(delta_t)

    print("=== Aging sweep: R_step_ratio -> Δt, max|e| ===")
    print("R_step_ratio  |  FixedPID Δt[s]  PID×FSM Δt[s]  AITL Δt[s]  ||  FixedPID max|e|  PID×FSM max|e|  AITL max|e|")
    print("-" * 110)

    for i, ratio in enumerate(sweep):
        plant_params = dict(base_plant)
        plant_params["R_step_ratio"] = float(ratio)

        row_dt = []
        row_me = []
        for j, (name, tuner) in enumerate(cases):
            dt_s, me = simulate_metrics(
                case=name,
                T=T, dt=dt,
                plant_params=plant_params,
                pid_normal=pid_normal,
                pid_high=pid_high,
                fsm_params=fsm_params,
                tuner_params=tuner,
            )
            delta_t[i, j] = dt_s
            max_e[i, j] = me
            row_dt.append(dt_s)
            row_me.append(me)

        print(
            f"{ratio:10.2f}  |  {row_dt[0]:12.3f}  {row_dt[1]:12.3f}  {row_dt[2]:10.3f}  ||  "
            f"{row_me[0]:13.3f}  {row_me[1]:13.3f}  {row_me[2]:10.3f}"
        )

    # --- plot (use fig object, and save to data/ before show) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(sweep, delta_t[:, 0], label="Fixed PID")
    ax1.plot(sweep, delta_t[:, 1], label="PID×FSM")
    ax1.plot(sweep, delta_t[:, 2], label="AITL")
    ax1.set_xlabel("R aging step ratio (ΔR/R0) [-]")
    ax1.set_ylabel("Δt (settle time) [s]")
    ax1.grid(True, alpha=0.25)
    ax1.legend(loc="best", fontsize=9)
    ax1.set_title("Reliability: timing recovery Δt vs aging")

    ax2.plot(sweep, max_e[:, 0], label="Fixed PID")
    ax2.plot(sweep, max_e[:, 1], label="PID×FSM")
    ax2.plot(sweep, max_e[:, 2], label="AITL")
    ax2.set_xlabel("R aging step ratio (ΔR/R0) [-]")
    ax2.set_ylabel("max|e| [A]")
    ax2.grid(True, alpha=0.25)
    ax2.legend(loc="best", fontsize=9)
    ax2.set_title("Safety: worst deviation max|e| vs aging")

    fig.tight_layout()

    # ✅ save to data/ (portal-friendly)
    os.makedirs("data", exist_ok=True)
    out_png = "data/13_aging_sweep_delta_t.png"
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    print(f"\n[saved] {out_png}")

    plt.show()


if __name__ == "__main__":
    main()
