---
title: "Uncertainty as State"
layout: default
---

# Uncertainty as State

## Why Δ Must Be a State

Treating uncertainty Δ as a single fixed bound hides critical information:
**where** and **how** degradation manifests.

True Robust Control treats Δ as a **state variable**.

---

## Decomposition of Δ

Δ is monitored in three domains:

### Low-Frequency Component
- Tracking degradation
- Gain reduction
- Increased friction

Risk:
- Loss of performance
- Steady-state error

---

### High-Frequency Component
- Unmodeled dynamics
- Delay increase
- Resonance amplification

Risk:
- Loss of stability margin
- Oscillation

---

### Input-Side Component
- Increased control effort
- Saturation
- Mechanical stress

Risk:
- Hardware damage
- Actuator failure

---

## Operational Threshold: 0.8

- ∥Δ∥∞ = 1.0 → theoretical guarantee failure
- Waiting until 1.0 is reactive and unsafe

**0.8 is chosen as a proactive operational threshold**:
- Still within guaranteed region
- Close enough to anticipate worst-case behavior

---

## FSM Interpretation

When any component reaches 0.8:
- FSM transitions to a degraded state
- Design adaptation is triggered

---
