---
layout: default
title: Samizo-Lab AITL Controller
---

# Samizo-Lab AITL Controller  
## Adaptive Intelligent Three-Layer Control Architecture

The **AITL Controller** is an educational and research-oriented control framework
based on a clear separation of responsibilities across three layers:

```
Inner Loop : PID Controller  
Middle Loop: FSM (Finite State Machine)  
Outer Loop: LLM (Design-Time Intelligence)
```

The goal of this project is **architectural clarity and reliability-aware design**,
rather than aggressive performance optimization.

---

## Architecture Variants

AITL is documented in two complementary architectural variants.

---

## 🔵 A-Type — Adaptive Control Capability

**A-Type** focuses on demonstrating *how adaptive control can be realized*.

Key characteristics:
- Hybrid PID × FSM control
- Online adaptive behavior
- Educational and proof-of-concept oriented
- Clear, interpretable control logic

👉 **A-Type Documentation**  
- Overview & demos  
  → [`a_type/`](a_type/)  
- Reliability investigation under plant aging  
  → [`reliability/`](reliability/)

Use A-Type when:
- Learning adaptive control concepts
- Exploring hybrid control architectures
- Running performance-oriented simulations

---

## 🟢 B-Type — Reliability-First Adaptive Control

**B-Type** is a reliability-oriented evolution of A-Type.

It addresses a critical design question:

> **Should adaptation be allowed under the current system condition?**

Key characteristics:
- Explicit reliability metrics (Δt, gain ratio, amplitude ratio)
- FSM-based adaptation permission / blocking
- Conservative fallback to fixed PID
- Long-term reliability cost evaluation

👉 **B-Type Documentation (Start Here)**  
→ [`b_type/`](b_type/)

Use B-Type when:
- Designing for long-term operation
- Operating under plant aging or uncertainty
- Reliability and explainability are required

---

## Architectural Perspective

| Variant | Core Question | Design Focus |
|------|---------------|--------------|
| A-Type | How can the system adapt? | Capability & performance |
| B-Type | Should the system adapt? | Reliability & safety |

> **A-Type demonstrates capability.**  
> **B-Type enforces responsibility.**

Together, they form a complete adaptive control methodology.

---

## Recommended Reading Order

1. **AITL Overview (this page)**  
2. **B-Type Architecture**  
   → [`b_type/index.md`](b_type/index.md)  
3. **FSM Reliability Guard**  
   → [`b_type/fsm_guard.md`](b_type/fsm_guard.md)  
4. **A-Type Demos & Reliability Analysis**  
   → [`reliability/`](reliability/)

---

## Author

**Shinichi Samizo**  
Former Engineer, Seiko Epson Corporation  
Expertise in semiconductor devices, precision actuators, and control architecture
