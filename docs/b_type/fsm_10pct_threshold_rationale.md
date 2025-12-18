---
title: "FSM Trigger Threshold Rationale: 10% Deviation Rule"
author: "Samizo-AITL"
date: 2025-12-18
category: "B-Type Control Design"
tags:
  - PID Control
  - FSM
  - Reliability Guard
  - Aging Model
  - Threshold Design
---

# FSM Trigger Threshold Rationale (10% Deviation Rule)

## 1. Purpose of This Document

This document clarifies the **design rationale** for adopting  
a **10% deviation from the initial PID response** as the trigger threshold
for FSM (Finite State Machine) activation in **B-Type control architecture**.

The goal is to establish a **technically sound, explainable, and commercially acceptable**
basis for FSM intervention.

---

## 2. Baseline Concept: PID as the Primary Controller

The fundamental design principle is:

> **PID control is always the primary control method.**  
> FSM is used only as an *exception handler*.

FSM is **not** intended to continuously optimize performance,
but to protect the system from **unexpected degradation** beyond normal aging.

---

## 3. Typical Aging Model and Observed Deviation

### 3.1 Assumed Typical Model

The reference aging model assumes:

- Gradual increase in friction parameters
- No structural change in the plant
- Fixed PID gains
- No external disturbances beyond modeled degradation

This represents a **typical and expected aging scenario**.

---

### 3.2 Simulation Observation

Under this typical model:

- After approximately **5 years equivalent aging**
  (day ≈ 2000–4000 in simulation),
- The PID-controlled response deviates from the initial response by roughly **10%**,
  measured in:
  - response amplitude
  - timing / phase characteristics
  - control effort

This deviation is **not a failure**, but a **natural long-term drift**.

---

## 4. Meaning of the 10% Threshold

### 4.1 10% Is the Upper Bound of Normal Aging

The **10% deviation** represents:

- The **upper bound of expected degradation** over long-term operation
- A level where performance change becomes *measurable and noticeable*
- A typical threshold used in industrial tolerance and maintenance criteria

Therefore:

- **Deviation < 10%** → expected aging (no FSM intervention)
- **Deviation ≥ 10%** → potentially *unexpected or accelerated degradation*

---

## 5. FSM Trigger Definition

### 5.1 Reference for Comparison

All FSM decisions are based on comparison with the **initial PID baseline**:

- Initial PID response at day = 0 is stored as reference
- Current response is compared against this baseline
- Absolute error alone is **not** used

---

### 5.2 Deviation Metrics

FSM evaluates deviation using normalized metrics such as:

#### Amplitude Deviation

$$
\Delta A = \frac{|A_{\text{current}} - A_0|}{A_0}
$$

#### Timing / Period Deviation

$$
\Delta t = \frac{|t_{\text{current}} - t_0|}{t_0}
$$

---

### 5.3 FSM Activation Logic (OR Condition)

FSM is triggered when **either** of the following conditions is met:

$$
\Delta A \ge 0.10 \;\; \textbf{OR} \;\; \Delta t \ge 0.10
$$

**AND logic is intentionally not used**, because it would delay protection
in fast or asymmetric degradation scenarios.

---

## 6. Role of Reliability Guard in B-Type Control

### 6.1 Risk of FSM Overreaction

FSM-based gain or mode changes can:

- Increase control effort
- Increase saturation rate
- Degrade stability if misapplied

Therefore, FSM alone is insufficient.

---

### 6.2 Reliability Guard as a Safety Supervisor

In B-Type architecture, **Reliability Guard** acts as a supervisory layer:

- FSM proposals are evaluated before application
- Corrections are limited or rejected if reliability metrics worsen

Typical guarded metrics include:

- Saturation rate (isat_rate)
- Integrated control effort
- Long-term cost accumulation

---

## 7. Commercial and Customer Perspective

This design allows a clear and defensible explanation to customers:

> “Under normal aging, the controller behaves exactly as designed.
> Only when performance deviates significantly—beyond about 10% from the original behavior—
> does the system activate corrective logic to protect reliability.”

This approach provides:

- Predictable behavior
- Avoidance of unnecessary intervention
- Robust handling of unexpected field conditions

---

## 8. Design Summary

- PID remains the default controller
- FSM is activated only for **unexpected degradation**
- 10% deviation represents **5-year-equivalent typical aging**
- FSM trigger uses **OR logic**
- Reliability Guard ensures safety and prevents overcompensation

This framework balances **control performance, reliability, and commercial acceptability**.

---

*End of document*
