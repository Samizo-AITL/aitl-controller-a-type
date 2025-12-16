"""
09_reliability_cost_tradeoff.py

- Uses demo 06 via runpy
- Computes:
    Δt mean
    Amplitude ratio
    Reliability cost J_rel
- Compares:
    PID vs AITL under friction aging
- Shows that "Δt improvement" does NOT always mean "Reliability improvement"
"""

from __future__ import annotations

import os
import runpy
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# Config
# =========================================================
AGING_DAYS = 1000

DT_MAX = 0.8        # [s] reference (for interpretation only)
AMP_MIN = 0.90      # amplitude guard reference

# Reliability cost weights
W_DT  = 1.0
W_AMP = 4.0         # penalize authority loss strongly

OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True)


# =========================================================
# Metrics
# =========================================================
def amplitude_ratio(ref_x: np.ndarray, cmp_x: np.ndarray) -> float:
    a0 = float(np.max(ref_x) - np.min(ref_x))
    a1 = float(np.max(cmp_x) - np.min(cmp_x))
    return a1 / a0 if a0 > 1e-12 else float("nan")


def dt_mean_from_demo06(env: Dict, t: np.ndarray, x_ref: np.ndarray, x_cmp: np.ndarray) -> float:
    compute_dt = env["compute_dt"]
    dts = compute_dt(t, x_ref, x_cmp)
    return float(np.mean(dts)) if len(dts) > 0 else float("nan")


def reliability_cost(dt: float, amp: float,
                     w_dt: float, w_amp: float,
                     amp_min: float) -> float:
    """
    J_rel = w_dt * |Δt| + w_amp * max(0, amp_min - amp)
    """
    return w_dt * abs(dt) + w_amp * max(0.0, amp_min - amp)


# =========================================================
# Load demo 06
# =========================================================
def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_demo06(repo_root: Path) -> Dict:
    demo06_path = repo_root / "demos" / "06_pid_initial_vs_aitl_friction_aging_demo.py"
    env = runpy.run_path(str(demo06_path))
    if "simulate_response" not in env:
        raise RuntimeError("simulate_response() not found in demo 06")
    return env


def simulate(env: Dict, controller: str, aging_days: int, variant: str) -> Tuple[np.ndarray, np.ndarray]:
    t, x = env["simulate_response"](
        controller=controller,
        aging_days=aging_days,
        variant=variant
    )
    return np.asarray(t), np.asarray(x)


# =========================================================
# Plot
# =========================================================
def plot_cost(costs: Dict[str, float], outpath: Path):
    labels = list(costs.keys())
    values = list(costs.values())

    plt.figure()
    plt.title("Reliability cost comparison")
    plt.bar(labels, values)
    plt.ylabel("J_rel (lower is better)")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


# =========================================================
# Main
# =========================================================
def main():
    repo_root = get_repo_root()
    os.chdir(repo_root)

    env06 = load_demo06(repo_root)

    # Reference
    t_ref, x_ref = simulate(env06, "PID", 0, "initial")

    # Aging cases
    t_pid,  x_pid  = simulate(env06, "PID",  AGING_DAYS, "aging")
    t_aitl, x_aitl = simulate(env06, "AITL", AGING_DAYS, "aging")

    # Metrics
    dt_pid  = dt_mean_from_demo06(env06, t_ref, x_ref, x_pid)
    dt_aitl = dt_mean_from_demo06(env06, t_ref, x_ref, x_aitl)

    amp_pid  = amplitude_ratio(x_ref, x_pid)
    amp_aitl = amplitude_ratio(x_ref, x_aitl)

    # Reliability cost
    J_pid  = reliability_cost(dt_pid,  amp_pid,  W_DT, W_AMP, AMP_MIN)
    J_aitl = reliability_cost(dt_aitl, amp_aitl, W_DT, W_AMP, AMP_MIN)

    # Print
    print("=== Reliability Cost Evaluation ===")
    print(f"W_DT={W_DT}, W_AMP={W_AMP}, AMP_MIN={AMP_MIN}")
    print("")
    print("Controller | Δt mean [s] | Amp ratio | J_rel")
    print("------------------------------------------------")
    print(f"PID  | {dt_pid:10.4f} | {amp_pid:9.3f} | {J_pid:6.3f}")
    print(f"AITL | {dt_aitl:10.4f} | {amp_aitl:9.3f} | {J_aitl:6.3f}")

    better = "PID" if J_pid < J_aitl else "AITL"
    print(f"\n→ Lower reliability cost : {better}")

    # Plot
    plot_cost(
        {"PID": J_pid, "AITL": J_aitl},
        OUT_DIR / "metric_reliability_cost.png"
    )

    print("\nSaved:")
    print(f" - {OUT_DIR / 'metric_reliability_cost.png'}")


if __name__ == "__main__":
    main()
