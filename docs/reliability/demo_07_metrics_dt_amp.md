---
title: "[Reliability Analysis] Δt and Amplitude Evaluation under Friction Aging"
layout: default
lang: en
author: AITL Controller A-Type
tags:
  - Reliability
  - Adaptive Control
  - AITL
  - Friction Aging
  - PID
description: >
  Quantitative reliability analysis of PID and AITL controllers under
  friction aging (1000 days), using timing deviation (Δt) and amplitude
  ratio metrics.
---

# [Reliability Analysis] Δt and Amplitude Evaluation under Friction Aging  
**AITL Controller A-Type**

---

## 1. Purpose (Why this analysis exists)

The purpose of this analysis is to clarify, under **friction aging equivalent to 1000 days**,  
what is **preserved** and what is **sacrificed** by:

- Conventional PID control  
- AITL (PID × FSM-based re-tuning)

using **quantitative reliability metrics (Δt and amplitude ratio)**.

Issues that are often overlooked in waveform-based evaluations (demo 06), such as  
**over-compensation** and **loss of motion authority**, are explicitly visualized using numerical indicators.

---

## 2. Definition of Evaluation Metrics

### 2.1 Δt (Timing Deviation)

- Definition  
  Difference between the peak time of the reference response (Initial)  
  and the peak time of the compared response.

$$
\Delta t = t_{\text{cmp, peak}} - t_{\text{ref, peak}}
$$

- Interpretation  
  - Δt > 0 : lag  
  - Δt < 0 : lead  

*In this analysis, the **mean value** of Δt is used.*

---

### 2.2 Amplitude Ratio

- Definition  

$$
A / A_0 = \frac{\max(x) - \min(x)}{\max(x_{\text{ref}}) - \min(x_{\text{ref}})}
$$

- Interpretation  
  - 1.0 : Equivalent control authority to the reference  
  - < 0.9 : Degraded control authority  
  - < 0.7 : Practically unsafe region  

---

## 3. Evaluation Conditions

- Aging model: Increase in friction terms only (Fc, Fs)  
- Aging level: Equivalent to 1000 days  
- Evaluation script:  
  `demos/07_reliability_metrics_dt_amp.py` (self-contained)

---

## 4. Numerical Results

```
=== Reliability Metrics (1000 days aging) ===
Controller | Δt mean [s] | Amp ratio
------------------------------------
PID_only   | -0.4730     | 0.902
AITL       | -1.3807     | 0.888
```

---

## 5. Interpretation of Results (Key Findings)

### 5.1 Discussion on Δt

- **PID_only**  
  - Friction aging introduces response delay  
  - Compensation is limited, resulting in only slight lead behavior  

- **AITL**  
  - Delay is detected and gains are reinforced by FSM logic  
  - This results in a **significant peak advance (lead)**  
  - The absolute value |Δt| actually increases  

👉 **AITL succeeds in delay compensation but fails to preserve the timing reference.**

---

### 5.2 Discussion on Amplitude

- **PID_only**: 0.902  
  → Control authority is largely preserved  

- **AITL**: 0.888  
  → **Amplitude is reduced** as the cost of Δt improvement  

👉 **Motion authority is sacrificed in order to preserve timing behavior.**

---

## 6. Design-Relevant Conclusions

### 6.1 Limitation of Single-Metric Optimization

- Re-tuning focused solely on minimizing Δt leads to:
  - Excessive lead (over-compensation)  
  - Reduction in amplitude (loss of authority)  

👉 **Reliability is not equivalent to minimizing Δt alone.**

---

### 6.2 Interpretation of the Current AITL State

The current AITL behavior can be summarized as:

- “If delay is detected, always move forward”  
- No constraints applied  
- No distinction between lead and lag  

This behavior **correctly exposes a design failure mode**  
and should be regarded as a design outcome, not a bug.

---

## 7. Improvement Guidelines (Next Steps)

### 7.1 Redefinition of Δt

- Use absolute timing deviation instead of signed Δt:

$$
|\Delta t|
$$

as the reliability metric.

---

### 7.2 FSM State Expansion

| State | Condition |
|---|---|
| LAG  | Δt > +Δt\_max |
| LEAD | Δt < -Δt\_max |
| OK   | $$|\Delta t| \le \Delta t_{\max}$$ |

👉 **“Too fast” is also defined as degradation.**

---

### 7.3 Introduction of Amplitude Lower Bound

- If A / A₀ < 0.9 → Gain reinforcement is prohibited  
- This suppresses the trade-off between timing compensation and control authority.

---

## 8. Summary (Value of This Analysis)

- Quantitatively identifies **AITL over-compensation issues** that are not visible in waveforms  
- Demonstrates that **delay compensation and reliability are distinct concepts**  
- Clearly defines the **design challenges of AITL-based reliability control**

👉 This analysis is **not a failure report**,  
but a result that **advances design decision-making**.

---

## Related Demos

- `demos/06_pid_initial_vs_aitl_friction_aging_demo.py`  
- `demos/07_reliability_metrics_dt_amp.py`  

---

**[END]**
