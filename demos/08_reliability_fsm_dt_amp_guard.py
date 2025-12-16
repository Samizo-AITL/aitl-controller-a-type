"""
08_reliability_fsm_dt_amp_guard.py

- Uses demo 06 via runpy (avoid importing module names starting with digits)
- Computes:
    Δt mean (using demo06.compute_dt)
    Amp ratio (A/A0)
- FSM decision:
    OK / LAG / LEAD based on signed Δt
- Guard:
    Amp ratio < AMP_MIN => block gain boost
    LEAD => block gain boost (and recommend revert/relax)
- Saves plots under data/
"""

from __future__ import annotations

import os
import runpy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Config
# -----------------------------
AGING_DAYS = 1000

DT_MAX = 0.8        # [s] classification threshold
AMP_MIN = 0.90      # motion authority lower bound

OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True)


# -----------------------------
# Metrics
# -----------------------------
def amplitude_ratio(ref_x: np.ndarray, cmp_x: np.ndarray) -> float:
    a0 = float(np.max(ref_x) - np.min(ref_x))
    a1 = float(np.max(cmp_x) - np.min(cmp_x))
    if a0 <= 1e-12:
        return float("nan")
    return a1 / a0


def dt_mean_from_demo06(demo06_env: Dict, t: np.ndarray, x_ref: np.ndarray, x_cmp: np.ndarray) -> float:
    """
    Use demo06.compute_dt(t, x_ref, x_cmp) and take mean.
    """
    if "compute_dt" not in demo06_env:
        raise RuntimeError("demo 06 does not define compute_dt()")

    compute_dt = demo06_env["compute_dt"]
    dts = compute_dt(t, x_ref, x_cmp)  # array of Δt for corresponding peaks
    if len(dts) == 0:
        return float("nan")
    return float(np.mean(dts))


# -----------------------------
# FSM
# -----------------------------
@dataclass
class FsmDecision:
    state: str
    dt: float
    dt_abs: float
    amp_ratio: float
    allow_gain_boost: bool
    action: str


def classify_state(dt: float, dt_max: float) -> str:
    if dt > dt_max:
        return "LAG"
    if dt < -dt_max:
        return "LEAD"
    return "OK"


def decide(dt: float, amp: float, dt_max: float, amp_min: float) -> FsmDecision:
    state = classify_state(dt, dt_max)
    dt_abs = abs(dt)

    allow = (state == "LAG") and (amp >= amp_min)

    if state == "OK":
        action = "NO ACTION (within timing band)"
    elif state == "LAG":
        if amp >= amp_min:
            action = "GAIN BOOST ALLOWED (lag detected, authority OK)"
        else:
            action = "GAIN BOOST BLOCKED (lag detected, but authority too low)"
    else:  # LEAD
        action = "GAIN BOOST BLOCKED + REVERT/RELAX (lead detected)"

    return FsmDecision(
        state=state,
        dt=dt,
        dt_abs=dt_abs,
        amp_ratio=amp,
        allow_gain_boost=allow,
        action=action,
    )


# -----------------------------
# Load demo 06 via runpy
# -----------------------------
def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_demo06(repo_root: Path) -> Dict:
    demo06_path = repo_root / "demos" / "06_pid_initial_vs_aitl_friction_aging_demo.py"
    if not demo06_path.exists():
        raise FileNotFoundError(f"demo 06 not found: {demo06_path}")

    env = runpy.run_path(str(demo06_path))

    # must have simulate_response
    if "simulate_response" not in env:
        raise RuntimeError(
            "demo 06 loaded, but simulate_response() was not found.\n"
            "Please add simulate_response() to demo 06 (see provided patch)."
        )
    return env

def simulate(env: Dict, controller: str, aging_days: int, variant: str) -> Tuple[np.ndarray, np.ndarray]:
    fn = env["simulate_response"]
    t, x = fn(controller=controller, aging_days=aging_days, variant=variant)
    t = np.asarray(t, dtype=float)
    x = np.asarray(x, dtype=float)
    return t, x

# -----------------------------
# Plot helpers
# -----------------------------
def plot_dt_bar(dt_pid: float, dt_aitl: float, dt_max: float, outpath: Path) -> None:
    labels = ["PID", "AITL"]
    vals = [dt_pid, dt_aitl]
    plt.figure()
    plt.title("Timing deviation (Δt mean)")
    plt.bar(labels, vals)
    plt.ylabel("Δt mean [s]")
    plt.grid(True, axis="y")
    plt.axhline(+dt_max, linestyle="--")
    plt.axhline(-dt_max, linestyle="--")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def plot_amp_bar(amp_pid: float, amp_aitl: float, amp_min: float, outpath: Path) -> None:
    labels = ["PID", "AITL"]
    vals = [amp_pid, amp_aitl]
    plt.figure()
    plt.title("Motion authority")
    plt.bar(labels, vals)
    plt.ylabel("Amplitude ratio (A / A₀)")
    plt.ylim(0.0, 1.1)
    plt.grid(True, axis="y")
    plt.axhline(amp_min, linestyle="--")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    repo_root = get_repo_root()
    os.chdir(repo_root)  # ensure relative data/ path

    env06 = load_demo06(repo_root)

    # Reference: Initial (day=0, PID)
    t_ref, x_ref = simulate(env06, controller="PID", aging_days=0, variant="initial")

    # Compare: aging
    t_pid, x_pid = simulate(env06, controller="PID", aging_days=AGING_DAYS, variant="aging")
    t_aitl, x_aitl = simulate(env06, controller="AITL", aging_days=AGING_DAYS, variant="aging")

    # Metrics (Δt uses demo06.compute_dt, so t must match)
    # In your sim, t grids should match; still, we compute dt using t_ref.
    dt_pid = dt_mean_from_demo06(env06, t_ref, x_ref, x_pid)
    dt_aitl = dt_mean_from_demo06(env06, t_ref, x_ref, x_aitl)

    amp_pid = amplitude_ratio(x_ref, x_pid)
    amp_aitl = amplitude_ratio(x_ref, x_aitl)

    dec_pid = decide(dt_pid, amp_pid, DT_MAX, AMP_MIN)
    dec_aitl = decide(dt_aitl, amp_aitl, DT_MAX, AMP_MIN)

    print("=== Reliability FSM (Δt mean + Amp guard) ===")
    print(f"Config: DT_MAX={DT_MAX:.3f} [s], AMP_MIN={AMP_MIN:.3f}, AGING_DAYS={AGING_DAYS}")
    print("")
    print("Controller | Δt mean [s] | |Δt| [s] | Amp ratio | State | GainBoost | Action")
    print("-" * 94)
    for name, dec in [("PID", dec_pid), ("AITL", dec_aitl)]:
        gb = "ALLOW" if dec.allow_gain_boost else "BLOCK"
        print(f"{name:9s} | {dec.dt:11.4f} | {dec.dt_abs:8.4f} | {dec.amp_ratio:9.3f} | "
              f"{dec.state:4s} | {gb:8s} | {dec.action}")

    # Save plots
    plot_dt_bar(dt_pid, dt_aitl, DT_MAX, OUT_DIR / "metric_dt_mean_fsm.png")
    plot_amp_bar(amp_pid, amp_aitl, AMP_MIN, OUT_DIR / "metric_amp_ratio_guard.png")

    print("\nSaved:")
    print(f" - {OUT_DIR / 'metric_dt_mean_fsm.png'}")
    print(f" - {OUT_DIR / 'metric_amp_ratio_guard.png'}")


if __name__ == "__main__":
    main()
