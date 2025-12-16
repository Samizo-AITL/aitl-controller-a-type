---
title: "[Reliability Analysis] Δt, Amplitude, and FSM Evaluation under Friction Aging"
layout: default
lang: en
author: AITL Controller A-Type
tags:
  - Reliability
  - Adaptive Control
  - FSM
  - AITL
  - Friction Aging
  - PID
description: >
  Reliability analysis of PID and AITL controllers under friction aging
  (equivalent to 1000 days), using timing deviation (Δt), amplitude ratio,
  and FSM-based decision logic.
---

# [Reliability Analysis] Δt, Amplitude, and FSM Evaluation under Friction Aging  
**AITL Controller A-Type**

---

## 1. Purpose (Why this analysis exists)

The purpose of this analysis is to clarify, under **friction aging equivalent to 1000 days**,  
what is **preserved** and what is **sacrificed** by:

- Conventional PID control  
- AITL (PID × FSM-based re-tuning)

by explicitly evaluating **quantitative metrics (Δt, amplitude)** and **FSM-based decisions**.

Phenomena that are often overlooked in waveform-based evaluations (demo 06), such as  
**over-compensation, loss of motion authority, and when to stop adaptation**,  
are visualized through numerical indicators and control logic.

---

## 2. Definition of Evaluation Metrics

### 2.1 Δt (Timing Deviation)

- Definition  
  Difference between the peak time of the reference response (Initial)  
  and the peak time of the compared response.

$$
\Delta t = t_{\text{cmp, peak}} - t_{\text{ref, peak}}
$$

- In this analysis, the **mean of peak timing differences (Δt mean)** is used.

- Interpretation
  - Δt > 0 : lag  
  - Δt < 0 : lead  

---

### 2.2 Amplitude Ratio

- Definition  

$$
A / A_0 = \frac{\max(x) - \min(x)}{\max(x_{\text{ref}}) - \min(x_{\text{ref}})}
$$

- Interpretation
  - 1.0 : Control authority equivalent to the reference  
  - < 0.9 : Degraded control authority  
  - < 0.7 : Practically unsafe region  

---

## 3. Evaluation Conditions

- Aging model: Increase in friction terms only (Fc, Fs)  
- Aging level: Equivalent to 1000 days  

- Controller configurations:
  - PID_only  
  - AITL (with FSM-based gain re-tuning)

- Used demos:
  - `demos/06_pid_initial_vs_aitl_friction_aging_demo.py`  
  - `demos/07_reliability_metrics_dt_amp.py`  
  - `demos/08_reliability_fsm_dt_amp_guard.py`  

---

## 4. Numerical Results (Measured in demo 08)

```
=== Reliability FSM (Δt mean + Amp guard) ===

Controller | Δt mean [s] | |Δt| [s] | Amp ratio | State | GainBoost | Action
----------------------------------------------------------------------------------------------
PID       |     -0.4730 |   0.4730 |     0.902 | OK   | BLOCK    | NO ACTION
AITL      |     -1.3807 |   1.3807 |     0.888 | LEAD | BLOCK    | GAIN BOOST BLOCKED + REVERT/RELAX
```

---

## 5. Interpretation of Results

### 5.1 Discussion on Δt

- **PID_only**
  - Phase delay occurs due to friction aging  
  - Compensation capability is limited, but |Δt| remains within an acceptable range  

- **AITL**
  - Friction degradation is detected and FSM intervenes  
  - Gain reinforcement excessively compensates the delay  
  - As a result, the response peak shifts significantly forward (**LEAD**)  

👉 **AITL succeeds in delay compensation but fails to preserve the timing reference.**

---

### 5.2 Discussion on Amplitude

- **PID_only**: A/A₀ = 0.902  
  - Control authority is largely preserved  

- **AITL**: A/A₀ = 0.888  
  - Amplitude is reduced as the cost of phase improvement  
  - Actuator limits and stability margins dominate the behavior  

👉 **Motion authority is sacrificed in order to preserve timing behavior.**

---

## 6. Reliability Decision by FSM (demo 08)

### 6.1 FSM State Definition

| State | Condition |
|---|---|
| OK   | $$|\Delta t| \le \Delta t_{\max}$$ |
| LAG  | $$\Delta t > +\Delta t_{\max}$$ |
| LEAD | $$\Delta t < -\Delta t_{\max}$$ |

($$\Delta t_{\max} = 0.8 \ \mathrm{s}$$)

---

### 6.2 Guard Conditions

- Amplitude lower bound:
  - If $$A / A_0 < 0.9$$ → Gain reinforcement is prohibited  

- LEAD state:
  - “Too fast” is also defined as degradation  
  - Gain reinforcement is blocked; rollback or relaxation is recommended  

---

### 6.3 FSM Decision Results

- **PID_only**
  - State = OK  
  - No re-tuning required  

- **AITL**
  - State = LEAD  
  - Amplitude lower bound violated  
  - **Adaptation is BLOCKED because it degrades reliability**  

👉 **The controller can explicitly decide when to stop adaptive behavior.**

---

## 7. Design-Relevant Conclusions

### 7.1 Limitation of Single-Metric Optimization

- Optimization focused solely on minimizing Δt leads to:
  - Excessive lead (over-compensation)  
  - Amplitude reduction (loss of control authority)  

👉 **Reliability is not equivalent to minimizing Δt.**

---

### 7.2 Current Position of AITL Controller A-Type

- Delay detection capability: available  
- Gain re-tuning capability: available  
- Adaptation stop decision: implemented for the first time in demo 08  

👉 **A transition point from “Adaptive” to “Reliable Adaptive”.**

---

## 8. Next Steps (Design Guidelines)

1. Use absolute timing deviation as the reliability metric:

$$
|\Delta t|
$$

2. Introduce a unified Reliability cost:

$$
J_{rel} = w_t |\Delta t| + w_a \max(0, 0.9 - A/A_0)
$$

3. Extend FSM logic from state classification  
   to **cost-based improvement / degradation decisions**.

---

## 9. Summary

- demo 06: Phenomenon visualization (waveforms)  
- demo 07: Quantitative evaluation (Δt, amplitude)  
- demo 08: Decision layer (FSM guard)  

This analysis quantitatively identifies **AITL over-compensation issues**  
and demonstrates that **adaptive control can and should be stopped**  
when reliability degrades.

This result is **not a failure report**,  
but an outcome that **advances reliability-oriented control design**.

---

**[END]**
