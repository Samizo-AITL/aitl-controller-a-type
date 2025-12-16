# Reliability Control Demo Analysis  
## Friction Aging Scenario (1000 days)

---

## 1. Overview

This document summarizes and analyzes the **Reliability Control behavior** of  
the **AITL Controller A-Type** under long-term **friction aging (1000 days)**.

The objective of this demo is **not accuracy improvement**, but **preservation of timing reliability (Δt)** under plant degradation.

---

## 2. Demo Configuration

### Controllers Compared

- **Initial**
  - PID controller tuned at day = 0
  - Represents nominal (non-aged) design

- **PID_only (1000d)**
  - Same PID gains applied after friction aging
  - No adaptation or retuning

- **AITL (1000d)**
  - FSM-based gain retuning
  - Aging-aware adaptive logic (naïve AITL version)

### Aging Model

- Coulomb friction (Fc) increase
- Static friction (Fs) increase
- Other plant parameters unchanged

Aging level corresponds to **1000 days of operation**.

---

## 3. Result Visualization

The following figure compares the time-domain responses:

<p align="center">
  <img
    src="https://samizo-aitl.github.io/aitl-controller-a-type/data/pid_vs_aitl_friction_aging.png"
    alt="Timing degradation under friction aging"
    style="width:80%;"
  />
</p>

**Figure 1** — Timing degradation (Δt) under friction aging

---

## 4. Observed Results

### 4.1 Initial (Reference)

- Stable oscillatory response
- Nominal amplitude and phase
- Used as Δt reference

---

### 4.2 PID_only (1000d)

- Clear **phase delay accumulation**
- Peak timing shifts progressively
- Amplitude mostly preserved

**Interpretation**  
→ Friction aging manifests primarily as **timing degradation (Δt increase)**  
→ Conventional PID cannot maintain temporal reliability

---

### 4.3 AITL (1000d)

- **Peak timing remains close to Initial**
- Δt is effectively suppressed
- However:
  - Oscillation amplitude is reduced
  - Flat / saturated-like regions appear
  - Motion authority is partially lost

**Interpretation**  
→ Timing is preserved  
→ **Controllability is sacrificed**

---

## 5. Key Insight — Why This Happens

The current AITL implementation optimizes **timing (Δt)** as a *single objective*.

As a result:

- Gain retuning suppresses phase lag
- But ignores:
  - Amplitude preservation
  - Control authority
  - Energy usage
  - Stability margin

This leads to a critical outcome:

> **Timing-oriented retuning alone can collapse motion amplitude.**

This behavior is **not a bug**, but an **expected failure mode** of naïve Reliability Control.

---

## 6. Redefining Reliability Control

From this experiment, Reliability Control must be defined as:

> **A control framework that preserves system performance under degradation  
> using multi-objective, constraint-aware adaptation,  
> rather than single-metric optimization.**

### Δt is important — but **not sufficient**.

---

## 7. Design Lessons Learned

### Lesson 1  
Single-metric (Δt-only) optimization is **not Reliability Control**.

### Lesson 2  
Retuning is a **design action**, not a simple gain tweak.

### Lesson 3  
FSMs must detect **over-adaptation**, not only degradation.

---

## 8. Future Design Policy

### 8.1 Introduce Multi-Objective Reliability Metrics

Minimum required metrics:

- Timing deviation (Δt)
- Amplitude ratio (motion authority)
- Actuator saturation rate
- Retuning frequency / stability

---

### 8.2 Retuning Policy Upgrade

- Eliminate resets to base gains
- Use **incremental gain updates**
- Limit gain change rates
- Enforce amplitude and stability constraints

---

### 8.3 Reliability FSM Extension

Proposed states:

- NORMAL
- TIMING_DEGRADE
- UNDERACTUATED
- ACTUATOR_STRESS
- CRITICAL

FSM must decide **when to adapt** and **when to stop adapting**.

---

## 9. Position of This Result

This demo represents a **critical intermediate milestone**:

- Demonstrates PID limitation
- Demonstrates naïve AITL limitation
- Clarifies necessary conditions for true Reliability Control

> Failure to preserve amplitude while preserving timing  
> is an essential lesson toward mature Reliability Control.

---

## 10. Next Steps

1. Implement amplitude-constrained AITL
2. Formalize Reliability FSM design
3. Log Δt, amplitude, and saturation simultaneously
4. Extend aging scenarios beyond friction

---

## Conclusion

AITL has already surpassed conventional adaptive control.  
The remaining challenge lies not in algorithms, but in **how reliability itself is defined and constrained**.

This demo provides the foundation for that definition.
