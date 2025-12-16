"""
07_reliability_metrics_dt_amp.py

Reliability metrics demo (self-contained):
- Δt   : timing deviation (peak-to-peak)
- Amp  : amplitude ratio (motion authority)

This script is intentionally independent from 06_ demos.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =========================================================
# Utility
# =========================================================

def sat(x, lo, hi):
    return np.minimum(np.maximum(x, lo), hi)

# =========================================================
# Plant (friction aging ONLY)
# =========================================================

def plant_params(day):
    Fc0, Fs0 = 0.25, 0.45
    b0 = 0.35
    Kt0 = 0.9

    Fc = Fc0 * (1 + 0.0040 * day)
    Fs = Fs0 * (1 + 0.0050 * day)

    return dict(
        m=1.0,
        Fc=Fc,
        Fs=Fs,
        vs=0.02,
        kv=0.04,
        b=b0,
        Kt=Kt0,
        R=2.0
    )

def friction(v, p):
    sgn = np.sign(v) if abs(v) > 1e-6 else 0.0
    return (p["Fc"] + (p["Fs"] - p["Fc"])
            * np.exp(-(abs(v)/p["vs"])**2)) * sgn + p["kv"] * v

# =========================================================
# PID Controller
# =========================================================

class PID:
    def __init__(self, kp, ki, kd, dt):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.dt = dt
        self.i = 0.0
        self.e_prev = 0.0

    def reset(self):
        self.i = 0.0
        self.e_prev = 0.0

    def step(self, e, u_sat, u_unsat):
        self.i += (e + (u_sat - u_unsat)) * self.dt
        de = (e - self.e_prev) / self.dt
        self.e_prev = e
        return self.kp * e + self.ki * self.i + self.kd * de

# =========================================================
# AITL : FSM + Retuning (minimal)
# =========================================================

def fsm_state(metrics):
    if metrics["isat_rate"] > 0.15:
        return "SATURATION"
    if metrics["low_speed_error"] > 0.03:
        return "FRICTION"
    return "NORMAL"

def retune_pid(base, state):
    kp, ki, kd = base
    if state == "FRICTION":
        kp *= 1.6
        ki *= 0.8
        kd *= 1.2
    elif state == "SATURATION":
        ki *= 0.6
        kd *= 1.3

    return (
        float(sat(kp, 10, 120)),
        float(sat(ki, 1, 120)),
        float(sat(kd, 0.0, 3.0))
    )

# =========================================================
# Simulation
# =========================================================

def simulate(day, controller_type,
             base_gains=(25.0, 50.0, 0.3),
             T=20.0, dt=0.001,
             Vmax=12.0, Imax=6.0):

    p = plant_params(day)
    pid = PID(*base_gains, dt)
    pid.reset()

    x, v = 0.0, 0.0
    x_ref = 1.0

    n = int(T / dt)
    slow_N = int(0.1 / dt)

    xs = np.zeros(n)
    Is = np.zeros(n)

    for k in range(n):
        e = x_ref - x

        u_unsat = pid.kp*e + pid.ki*pid.i \
                  + pid.kd*((e - pid.e_prev)/dt)

        V_pre = sat(u_unsat, -Vmax, Vmax)
        I_pre = sat(V_pre / p["R"], -Imax, Imax)

        if controller_type == "AITL" and k > 500 and k % slow_N == 0:
            win = Is[max(0, k-500):k]
            metrics = {
                "isat_rate": np.mean(np.abs(win) >= (Imax - 1e-6)),
                "low_speed_error": abs(e) if abs(v) < 0.01 else 0.0
            }
            state = fsm_state(metrics)
            pid.kp, pid.ki, pid.kd = retune_pid(base_gains, state)

        u = pid.step(e, V_pre, u_unsat)
        V = sat(u, -Vmax, Vmax)
        I = sat(V / p["R"], -Imax, Imax)

        a = (p["Kt"]*I - p["b"]*v - friction(v, p)) / p["m"]
        v += a * dt
        x += v * dt

        xs[k] = x
        Is[k] = I

    t = np.arange(n) * dt
    return t, xs

# =========================================================
# Δt metric (peak-based)
# =========================================================

def find_peaks_simple(t, x, min_dist_s=0.8):
    idx = np.where((x[1:-1] > x[:-2]) & (x[1:-1] > x[2:]))[0] + 1
    min_dist = int(min_dist_s / (t[1]-t[0]))
    peaks, last = [], -10**9
    for i in idx:
        if i - last >= min_dist:
            peaks.append(i)
            last = i
    return np.array(peaks, dtype=int)

def compute_dt(t, x_ref, x_cmp):
    pr = find_peaks_simple(t, x_ref)
    pc = find_peaks_simple(t, x_cmp)
    n = min(len(pr), len(pc))
    return t[pc[:n]] - t[pr[:n]]

# =========================================================
# Amplitude metric
# =========================================================

def amplitude(x):
    return np.max(x) - np.min(x)

# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    # --- simulate ---
    t, x_ref        = simulate(0,    "PID")
    _, x_pid_1000   = simulate(1000, "PID")
    _, x_aitl_1000  = simulate(1000, "AITL")

    # --- Δt ---
    dt_pid  = compute_dt(t, x_ref, x_pid_1000)
    dt_aitl = compute_dt(t, x_ref, x_aitl_1000)

    dt_pid_mean  = np.mean(dt_pid)
    dt_aitl_mean = np.mean(dt_aitl)

    # --- amplitude ratio ---
    A0     = amplitude(x_ref)
    A_pid  = amplitude(x_pid_1000)  / A0
    A_aitl = amplitude(x_aitl_1000) / A0

    # =====================================================
    # Print results
    # =====================================================

    print("\n=== Reliability Metrics (1000 days aging) ===")
    print("Controller    | Δt mean [s] | Amp ratio")
    print("------------------------------------------")
    print(f"PID_only      | {dt_pid_mean:+.4f}     | {A_pid:.3f}")
    print(f"AITL          | {dt_aitl_mean:+.4f}     | {A_aitl:.3f}")

    # =====================================================
    # Visualization
    # =====================================================

    labels = ["PID_only", "AITL"]

    # Δt plot
    plt.figure(figsize=(6,4))
    plt.bar(labels, [dt_pid_mean, dt_aitl_mean])
    plt.ylabel("Δt [s]")
    plt.title("Timing reliability (Δt)")
    plt.grid(True, axis="y")
    plt.tight_layout()

    data_dir = Path(__file__).resolve().parents[1] / "data"
    data_dir.mkdir(exist_ok=True)
    plt.savefig(data_dir / "metric_dt.png", dpi=150)
    plt.show()

    # Amplitude plot
    plt.figure(figsize=(6,4))
    plt.bar(labels, [A_pid, A_aitl])
    plt.ylabel("Amplitude ratio (A / A₀)")
    plt.ylim(0, 1.1)
    plt.title("Motion authority")
    plt.grid(True, axis="y")
    plt.tight_layout()

    plt.savefig(data_dir / "metric_amp_ratio.png", dpi=150)
    plt.show()
