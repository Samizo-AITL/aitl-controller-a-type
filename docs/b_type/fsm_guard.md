---
title: "FSM Reliability Guard"
description: "Formal definition of reliability metrics and guard conditions for B-Type adaptive control"
layout: default
nav_order: 3
parent: "B-Type Architecture"
---

# FSM Reliability Guard  
## Metric Definitions and Decision Logic

---

## Purpose of the FSM Reliability Guard

The FSM Reliability Guard is the **core mechanism** that distinguishes  
AITL Controller **B-Type** from A-Type.

Its purpose is not to improve performance, but to **prevent adaptation from degrading reliability**.

> The FSM answers a single critical question:  
> **“Is adaptation allowed under the current reliability condition?”**

---

## Reliability Metrics Overview

The FSM evaluates system health using **dimensionless, normalized metrics**.  
This ensures robustness across operating points and plant variations.

The primary metrics are:

1. Response delay ratio (Δt / Δt₀)  
2. Gain compensation ratio (K / K₀)  
3. Amplitude ratio and saturation indicators  
4. Adaptation frequency (optional, for chattering detection)

---

## Metric 1: Response Delay Ratio (Δt / Δt₀)

### Definition

Let:
- Δt₀ : Nominal response delay under healthy plant conditions  
- Δt  : Measured response delay under current conditions  

The normalized delay ratio is defined as:

\[
R_{\Delta t} = \frac{\Delta t}{\Delta t_0}
\]

### Interpretation

- \( R_{\Delta t} \approx 1 \) : Nominal behavior  
- \( R_{\Delta t} > 1 \) : Degradation-induced delay  
- Large values indicate loss of responsiveness and control authority

### Guard Threshold

\[
R_{\Delta t} \le R_{\Delta t}^{\max}
\]

If this condition is violated, **adaptation must be blocked**.

---

## Metric 2: Gain Compensation Ratio (K / K₀)

### Definition

Let:
- \( K_0 \) : Nominal PID gain set  
- \( K \)   : Current (adapted) gain set  

The gain compensation ratio is defined as:

\[
R_{K} = \frac{K}{K_0}
\]

For multi-gain controllers, this ratio may be evaluated per component  
(e.g., \(K_P, K_I, K_D\)) or using a weighted norm.

### Interpretation

- \( R_K \approx 1 \) : Nominal control effort  
- \( R_K \gg 1 \) : Over-compensation risk  
- Excessive gain increase often precedes instability or saturation

### Guard Threshold

\[
R_K \le R_{K}^{\max}
\]

Violation indicates **unsafe compensation**, triggering adaptation blocking.

---

## Metric 3: Amplitude Ratio and Saturation

### Definition

Let:
- \( A_{\text{out}} \) : Output response amplitude  
- \( A_{\text{ref}} \) : Reference amplitude  

The amplitude ratio is:

\[
R_A = \frac{A_{\text{out}}}{A_{\text{ref}}}
\]

In addition, actuator saturation flags may be monitored.

### Interpretation

- Excessive amplitude indicates loss of damping
- Frequent saturation implies erosion of motion authority

### Guard Usage

Amplitude-related metrics are typically used as **secondary guards**  
or combined into a reliability cost function.

---

## Optional Metric: Adaptation Frequency (Chattering Detection)

### Definition

Let:
- \( N_{\text{adapt}} \) : Number of adaptation events per unit time  

Excessive adaptation frequency is a sign of instability in the supervisory logic.

### Guard Rule

If:
\[
N_{\text{adapt}} > N_{\text{adapt}}^{\max}
\]

then adaptation is blocked to prevent oscillatory redesign behavior.

---

## FSM Decision Logic

### Composite Guard Condition

Adaptation is permitted **only if all guard conditions are satisfied**:

\[
\begin{aligned}
R_{\Delta t} &\le R_{\Delta t}^{\max} \\
R_{K}        &\le R_{K}^{\max} \\
R_A          &\le R_{A}^{\max}
\end{aligned}
\]

If any condition is violated, the FSM transitions to **ADAPT_BLOCKED**.

---

## FSM State Transitions

```mermaid
stateDiagram-v2
    [*] --> NORMAL

    NORMAL --> DEGRADED : R_Δt > 1
    DEGRADED --> ADAPT_ALLOWED : All guards satisfied
    DEGRADED --> ADAPT_BLOCKED : Any guard violated

    ADAPT_ALLOWED --> DEGRADED : Metrics drift
    ADAPT_BLOCKED --> SAFE_MODE : Persistent violation

    SAFE_MODE --> NORMAL : Manual reset / maintenance
```

---

## Design Implications

- Adaptation is **explicitly constrained**, not implicitly discouraged
- Performance improvement never overrides reliability limits
- Long-term degradation naturally leads to conservative control behavior

> In B-Type, *blocking adaptation is a correct and expected outcome*.

---

## Summary

The FSM Reliability Guard provides:

- Formal, quantitative reliability definitions  
- Clear and deterministic adaptation permission rules  
- A structural safeguard against over-compensation  

By enforcing these guard conditions,  
B-Type transforms adaptive control into a **reliability-aware control architecture**.

---

The next sections may include:
- Reliability cost function formulation  
- Parameter selection guidelines for guard thresholds  
- Mapping from simulation metrics to real sensor data
