import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ROOT)

from controllers.fsm import FSMController


def main():
    DATA = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(DATA, exist_ok=True)

    states = {
        "normal": lambda v, t: f"[normal] {v}",
        "high":   lambda v, t: f"[high] {v}",
        "low":    lambda v, t: f"[low] {v}",
    }

    transitions = {
        "normal": [
            (lambda v: v > 1.0, "high"),
            (lambda v: v < -1.0, "low"),
        ],
        "high": [(lambda v: v < 0.5, "normal")],
        "low":  [(lambda v: v > -0.5, "normal")],
    }

    fsm = FSMController(states, transitions, initial_state="normal")

    inputs = [0, 0.3, 1.5, 0.2, -1.5, -0.4, 0.1]

    out = os.path.join(DATA, "fsm_transition_log.txt")
    with open(out, "w") as f:
        for v in inputs:
            out_val = fsm.step(v)
            f.write(f"{v}, {fsm.current_state}, {out_val}\n")

    print("Saved", out)


if __name__ == "__main__":
    main()
