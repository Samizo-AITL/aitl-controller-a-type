---
title: "AITL Controller B-Type"
description: "Reliability-first supervisory control architecture with deviation-based permissioned adaptation"
layout: default
nav_order: 1
parent: "B-Type Architecture"
---

# AITL Controller B-Type  
## Reliability-First Supervisory Control Architecture

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/aitl-controller-a-type/docs/b_type/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/aitl-controller-a-type/tree/main/docs/b_type) |

---

## Overview — Why B-Type Exists

AITL Controller **B-Type** is not an extension of adaptive capability,  
but an **architectural correction derived from A-Type reliability analysis**.

The core lesson from A-Type is clear:

> **Adaptation capability does not guarantee long-term reliability.**

While A-Type demonstrates *how adaptation can be performed*,  
B-Type defines **when adaptation is allowed — and when it must be suppressed**.

In short:

> **B-Type = Adaptation under explicit reliability permission**

---

## Design Lessons Inherited from A-Type

Reliability analysis under plant aging revealed the following:

- Adaptive control can temporarily compensate response delay (Δt)
- However, it may also cause:
  - Excessive gain escalation
  - Actuator saturation and authority loss
  - Long-term reliability degradation
- These risks are **not detectable from waveform performance alone**

This leads to a decisive architectural requirement:

> **Adaptation must be supervised by reliability metrics, not performance metrics.**

🔗 **Reference:**  
- A-Type Reliability Analysis  
  → [`../reliability/`](../reliability/)

---

## Core Design Philosophy of B-Type

B-Type is built on **three non-negotiable principles**.

---

### Principle 1: Adaptation Is Permission-Based

Adaptation is **never a default behavior**.

- It is *considered*
- It is *evaluated*
- It is *explicitly permitted or rejected*

based on predefined reliability conditions.

> Adaptation is a privilege, not a right.

---

### Principle 2: FSM Judges Reliability — Not Performance

A **Finite State Machine (FSM)** acts as a supervisory layer that evaluates  
*reliability deviation* rather than performance improvement.

Typical monitored quantities include:

- Response timing deviation ratio (Δt / Δt₀)
- Amplitude or authority deviation
- Gain deviation ratio (K / K₀)
- Saturation ratio (V–I limits)
- Adaptation frequency (chattering detection)

FSM responsibilities are intentionally limited:

- FSM **does not compute gains**
- FSM **does not optimize**
- FSM **only decides whether pre-approved actions are allowed**

🔗 **Details:**  
- FSM guard metrics and logic  
  → [`fsm_guard.md`](fsm_guard.md)

---

### Principle 3: Guaranteed Fallback to Fixed PID

Under **all conditions**, the controller must be able to revert to a  
**conservatively designed fixed PID controller**.

This guarantees:

- Minimum safe operation
- Deterministic behavior
- Explainability and auditability

> The fixed PID is not a failure mode.  
> It is the **reliability floor** of the system.

---

## Permission Logic (Minimal Specification)

B-Type formalizes adaptation control using an explicit **permission logic**.

Adaptation is enabled **only if all reliability conditions are satisfied**:

- **Δt / Δt₀ ≤ Δt_allow**  
  (temporal reliability is within acceptable degradation)
- **max|e| ≤ e_allow**  
  (safety envelope is preserved)
- **|ΔKp| / Kp₀ ≤ Kp_rate_allow**  
  (adaptation aggressiveness is bounded)

If **any** condition is violated:

- Adaptation is **disabled**
- Controller **falls back to fixed-gain PID**
- FSM remains in a *reliability protection* state until recovery

This logic ensures that adaptive behavior is  
**explicitly gated by reliability, not by optimism**.

---

## Architecture Positioning (PID × FSM × LLM)

B-Type explicitly separates responsibilities across time scales:

| Layer | Role | Time Scale |
|---|---|---|
| PID | Real-time control execution | ms |
| FSM | Reliability supervision & permission | s–min |
| Human / LLM | Gain design & validation | days–years |

Important clarification:

- **LLM is never a runtime decision-maker**
- LLM may assist *offline gain design*
- Final approval always belongs to the engineer

🔗 **Architecture details:**  
- PID × FSM × LLM structure  
  → [`architecture.md`](architecture.md)

---

## Positioning of A-Type vs B-Type

| Aspect | A-Type | B-Type |
|---|---|---|
| Purpose | Demonstrate adaptability | Guarantee reliability bounds |
| Adaptation | Always enabled | Conditionally permitted |
| Decision basis | Performance improvement | Reliability deviation |
| Gain handling | Dynamic | Pre-approved assets only |
| Intended use | Exploration / PoC | Deployment / long-term operation |

> **B-Type does not replace A-Type.**  
> It formalizes the operational discipline required to deploy A-Type safely.

---

## Mapping to Existing Demonstrations

B-Type intentionally reuses A-Type demonstrations,  
but **reinterprets their meaning through a reliability lens**.

> **Note:**  
> Demo numbers below refer to *conceptual roles*.  
> Concrete evidence is provided by A-Type demos (12, 13, 15),
> which are reinterpreted through B-Type reliability supervision.

- Degradation visualization → *baseline deviation reference*
- Δt / amplitude metrics → *FSM inputs*
- FSM explainability → *permission decision rationale*
- Reliability cost trade-off → *design-time decision support*

🔗 **Demo correspondence:**  
- A-Type → B-Type demo mapping  
  → [`demo_mapping.md`](demo_mapping.md)

---

## Summary — What B-Type Actually Is

AITL Controller B-Type is:

- A controller that **limits adaptation**
- A system that prioritizes **not breaking over optimizing**
- An architecture that explicitly encodes **engineering judgment**

In essence:

> **A-Type shows that a system *can* adapt.**  
> **B-Type ensures the system knows when it *should not*.**

---

## Recommended Reading Order

1. **Architecture overview**  
   → [`architecture.md`](architecture.md)

2. **FSM reliability guard (metrics & logic)**  
   → [`fsm_guard.md`](fsm_guard.md)

3. **Reliability cost formulation**  
   → [`reliability_cost.md`](reliability_cost.md)

4. **Deviation threshold design policy**  
   → [`threshold_guidelines.md`](threshold_guidelines.md)

5. **Demo mapping and integration**  
   → [`demo_mapping.md`](demo_mapping.md)

---

*End of B-Type Overview*
