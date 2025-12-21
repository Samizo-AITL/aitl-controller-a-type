---
title: "AITL Controller Documentation"
description: "Adaptive Intelligent Three-Layer (AITL) Control Architecture Documentation"
layout: default
nav_order: 1
---

# AITL Controller Documentation

This site documents the **AITL (Adaptive Intelligent Three-Layer) Controller**,  
a control architecture combining:

- **PID** for real-time stability  
- **FSM** for supervisory logic  
- **LLM** for design-time intelligence  

The documentation is organized around **architectural intent**,  
not just implementation details.

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/aitl-controller-a-type/docs/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/aitl-controller-a-type/tree/main/docs) |

---

## A-Type: Adaptive Control Capability

**A-Type** focuses on demonstrating *how adaptive control can be realized*.

It emphasizes:
- Hybrid PID + FSM control
- Online adaptation behavior
- Performance recovery under plant degradation

📘 **A-Type Reliability Analysis**  
→ [`reliability/`](reliability/)

Use A-Type when:
- Exploring adaptive control concepts
- Evaluating performance improvements
- Running proof-of-concept simulations

---

## B-Type: Reliability-First Adaptive Control

**B-Type** is a reliability-oriented evolution of A-Type.

It addresses a critical question left open by A-Type:

> **Should adaptation be allowed under the current system condition?**

B-Type introduces:
- Explicit reliability metrics (Δt, gain ratio, amplitude ratio)
- FSM-based adaptation permission and blocking
- Conservative fallback to fixed PID control
- Long-term reliability cost evaluation

📘 **B-Type Architecture (Start Here)**  
→ [`b_type/`](b_type/)

Use B-Type when:
- Designing for long-term operation
- Operating under plant aging or uncertainty
- Reliability and explainability are required

---

## Architectural Perspective

| Type | Core Question | Design Focus |
|---|---|---|
| A-Type | How can the system adapt? | Capability & performance |
| B-Type | Should the system adapt? | Reliability & safety |

> **A-Type demonstrates capability.**  
> **B-Type enforces responsibility.**

They are designed to coexist within the same framework.

---

## Recommended Reading Order

1. **B-Type Overview**  
   → [`b_type/index.md`](b_type/index.md)

2. **B-Type Architecture (PID × FSM × LLM)**  
   → [`b_type/architecture.md`](b_type/architecture.md)

3. **FSM Reliability Guard**  
   → [`b_type/fsm_guard.md`](b_type/fsm_guard.md)

4. **Reliability Cost & Thresholds**  
   → [`b_type/reliability_cost.md`](b_type/reliability_cost.md)  
   → [`b_type/threshold_guidelines.md`](b_type/threshold_guidelines.md)

5. **Demo Mapping**  
   → [`b_type/demo_mapping.md`](b_type/demo_mapping.md)

---

## Scope of This Documentation

This site focuses on:
- Control architecture design
- Reliability-aware adaptive control
- Explainable supervisory logic

Low-level implementation details are intentionally minimized  
in favor of **design intent and architectural clarity**.

---

## True Robust Control: Operational Robustness Layer

**True Robust Control** extends the AITL framework by addressing a limitation
shared by both A-Type and B-Type:

> **How should robustness itself be *operated* before theoretical guarantees fail?**

Rather than treating robustness as a fixed design outcome,
True Robust Control defines robustness as an **operational capability**.

---

### What It Adds to AITL

True Robust Control introduces the following concepts:

- **Uncertainty Δ as a monitored state**, not a static bound
- **Frequency-aware interpretation of degradation**
  - low-frequency (performance degradation)
  - high-frequency (stability margin loss)
  - input-side (actuator stress)
- **Proactive intervention at ∥Δ∥∞ ≈ 0.8**, before guarantee breakdown
- **Selective redesign of H∞ weight functions**
  - \( W_s \): performance demand
  - \( W_t \): robustness margin
  - \( W_u \): actuator protection
- **Clear role separation**
  - FSM: *when to intervene*
  - LLM: *what design lever to move*
  - Controller: *execute safely*

---

### Relationship to A-Type and B-Type

| Layer | Role |
|---|---|
| A-Type | Demonstrates *adaptive capability* |
| B-Type | Enforces *reliability permission and responsibility* |
| **True Robust Control** | **Operates robustness as a dynamic design process** |

> **A-Type asks:** *Can the system adapt?*  
> **B-Type asks:** *Should the system adapt?*  
> **True Robust Control asks:** *How should robustness itself be operated?*

These are not competing approaches,  
but **orthogonal layers of the same architecture**.

---

### Position in the Documentation

📘 **True Robust Control (Start Here for Robustness Operation)**  
→ [`true_robust_control/`](true_robust_control/)

This section is recommended when:
- H∞ control feels too conservative or too static
- Plant degradation evolves over time
- Robustness must be explained, not just assumed
- Design decisions must be auditable and intentional

---

### Architectural Perspective (Extended)

| Aspect | Focus |
|---|---|
| A-Type | Adaptation capability |
| B-Type | Reliability and safety gating |
| **True Robust Control** | **Operational robustness and design intervention** |

> **Capability without responsibility is dangerous.**  
> **Responsibility without operational robustness is blind.**  
> **True Robust Control connects the two.**

---

## Summary

The AITL Controller framework evolves as follows:

> **A-Type** → proves that adaptation is possible  
> **B-Type** → ensures adaptation is applied responsibly  

Together, they form a complete adaptive control design methodology.
