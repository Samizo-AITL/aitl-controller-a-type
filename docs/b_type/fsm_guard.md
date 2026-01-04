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

Primary monitored quantities:

1. **Response delay ratio** \( R_{\Delta t} = \Delta t / \Delta t_0 \)  
2. **Gain compensation ratio(s)** \( R_{K_P}, R_{K_I}, R_{K_D} \) (or a norm)  
3. **Amplitude / authority ratio** \( R_A \) and **saturation indicators**  
4. **Adaptation frequency** \( N_{\text{adapt}} \) (optional; anti-chattering)

> **Note:** In the current A-Type demos, adaptation mainly adjusts **\(K_P\)**.  
> Therefore, B-Type may start with \(R_{K_P}\) as the primary gain guard,
> and later extend to \(K_I, K_D\) if needed.

---

## Metric 1: Response Delay Ratio (Δt / Δt₀)

### Definition

Let:
- \( \Delta t_0 \) : nominal response delay under healthy plant conditions  
- \( \Delta t \)   : measured response delay under current conditions  

The normalized delay ratio is:

\[
R_{\Delta t} = \frac{\Delta t}{\Delta t_0}
\]

### How to Measure Δt (Operational Definition)

To avoid ambiguity, B-Type defines Δt using **event-to-event timing**.

A practical and reproducible definition (used in the A-Type sweep) is:

- Choose a reference event time \( t_{\text{event}} \)  
  (e.g., **disturbance start**, **reference step**, or **command change**)
- Define Δt as the **settling recovery time** after \( t_{\text{event}} \)

Example definition:

- Let \( e(t) = I_{\text{ref}}(t) - I(t) \)
- Choose a settle band \( |e(t)| < \epsilon \)
- Require band-hold for duration \( T_{\text{hold}} \)

Then Δt is:

\[
\Delta t
= \min_{t \ge t_{\text{event}}}
\left\{
t - t_{\text{event}}
\ \middle|\ 
|e(\tau)| < \epsilon,\ \forall \tau \in [t, t+T_{\text{hold}}]
\right\}
\]

This definition is:
- deterministic
- unit-consistent
- implementable both in simulation and runtime (with sampled data)

### Interpretation

- \( R_{\Delta t} \approx 1 \) : nominal timing behavior  
- \( R_{\Delta t} > 1 \) : degradation-induced delay (timing reliability loss)  
- Large values indicate loss of responsiveness and/or authority

### Guard Threshold

\[
R_{\Delta t} \le R_{\Delta t}^{\max}
\]

If violated, **adaptation must be blocked**.

---

## Metric 2: Gain Compensation Ratio (K / K₀)

### Definition (per gain)

Let:
- \( K_{P0}, K_{I0}, K_{D0} \) : nominal gains  
- \( K_P, K_I, K_D \)         : current gains  

Define per-gain ratios:

\[
R_{K_P} = \frac{K_P}{K_{P0}},\quad
R_{K_I} = \frac{K_I}{K_{I0}},\quad
R_{K_D} = \frac{K_D}{K_{D0}}
\]

If only \(K_P\) is adapted, then \(R_{K_P}\) is the primary guard.

### Interpretation

- \( R_{K_*} \approx 1 \) : nominal control effort  
- \( R_{K_*} \gg 1 \) : over-compensation risk  
- excessive gain escalation often precedes saturation, oscillation, or instability

### Guard Threshold

\[
R_{K_P} \le R_{K_P}^{\max},\quad
R_{K_I} \le R_{K_I}^{\max},\quad
R_{K_D} \le R_{K_D}^{\max}
\]

If any violated, adaptation is **blocked**.

### Rate Guard (Aggressiveness / “dK/dt”)

Even if absolute gains are within limits, rapid gain movement is risky.

Define a normalized gain rate guard (example for \(K_P\)):

\[
R_{\dot K_P} = \frac{|K_P(t) - K_P(t-\Delta T)|}{K_{P0}}
\]

Guard:

\[
R_{\dot K_P} \le R_{\dot K_P}^{\max}
\]

---

## Metric 3: Amplitude / Authority Ratio and Saturation

### Definition

Let:
- \( A_{\text{out}} \) : output response amplitude (or peak-to-peak)  
- \( A_{\text{ref}} \) : reference amplitude  

\[
R_A = \frac{A_{\text{out}}}{A_{\text{ref}}}
\]

Additionally, define saturation indicators:

- \( S_u \): fraction of time actuator is saturated  
- \( S_u = \frac{1}{T}\int \mathbf{1}(|u(t)| = u_{\max})\,dt \) (conceptual)
- or discrete equivalent in sampled systems

### Interpretation

- excessive amplitude suggests reduced damping / margin erosion
- frequent saturation indicates loss of motion authority (cannot realize commands)

### Guard Usage

Amplitude and saturation are typically used as:
- **secondary guards**, or
- components of a reliability cost function

Example guards:

\[
R_A \le R_A^{\max},\quad
S_u \le S_u^{\max}
\]

---

## Optional Metric: Adaptation Frequency (Chattering Detection)

### Definition

Let:
- \( N_{\text{adapt}} \) : number of gain updates per unit time window \(T_w\)

Guard:

\[
N_{\text{adapt}} \le N_{\text{adapt}}^{\max}
\]

If violated, adaptation is blocked to prevent oscillatory redesign behavior.

---

## Permission Logic (Minimal Specification)

B-Type permits adaptation **only if all conditions below are satisfied**:

\[
\begin{aligned}
R_{\Delta t} &\le R_{\Delta t}^{\max} \\
R_{K_P}      &\le R_{K_P}^{\max} \\
R_{\dot K_P} &\le R_{\dot K_P}^{\max} \\
\text{(optional)}\quad R_A &\le R_A^{\max} \\
\text{(optional)}\quad S_u &\le S_u^{\max}
\end{aligned}
\]

If **any** condition is violated:

- Adaptation is **disabled**
- Controller **falls back to fixed-gain PID**
- FSM enters a protective state until recovery

> Blocking adaptation is a **correct and expected outcome** in B-Type.

---

## FSM State Transitions (Operational)

```mermaid
stateDiagram-v2
    [*] --> NORMAL

    NORMAL --> DEGRADED : R_Δt > 1
    DEGRADED --> ADAPT_ALLOWED : All guards satisfied
    DEGRADED --> ADAPT_BLOCKED : Any guard violated

    ADAPT_ALLOWED --> DEGRADED : Metrics drift / guard at risk
    ADAPT_BLOCKED --> SAFE_MODE : Persistent violation or repeated blocking

    SAFE_MODE --> NORMAL : Manual reset / maintenance / re-baseline
```

---

## Design Implications

- Adaptation is **explicitly constrained**, not implicitly discouraged
- performance improvement never overrides reliability limits
- long-term degradation naturally leads to conservative control behavior

> In B-Type, the system is designed to converge toward safety,
> not to chase performance indefinitely.

---

## Summary

The FSM Reliability Guard provides:

- formal, quantitative reliability definitions  
- explicit measurement semantics for Δt (event-based)  
- deterministic permission logic for adaptation  
- guaranteed fallback to fixed PID  

By enforcing these guard conditions,  
B-Type transforms adaptive control into a **reliability-aware supervisory architecture**.

---

## Next Sections

- Reliability cost function formulation  
  → [`reliability_cost.md`](reliability_cost.md)

- Parameter selection guidelines for guard thresholds  
  → [`threshold_guidelines.md`](threshold_guidelines.md)

- Demo mapping and integration  
  → [`demo_mapping.md`](demo_mapping.md)
