---
layout: default
title: Reliability Analysis — AITL under Plant Aging
nav_order: 10
parent: Documentation
has_children: false
---

# Reliability Analysis — AITL under Plant Aging (1000 days)

This section provides a **reliability-oriented analysis** of the  
**AITL Controller A-Type** under **long-term plant degradation**,  
modeled as **friction aging equivalent to 1000 days**.

Unlike conventional performance-driven evaluations,  
the focus here is on **temporal reliability**:

- timing consistency (Δt)
- motion authority preservation
- and explicit decisions on *when adaptation should be stopped*

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/aitl-controller-a-type/docs/reliability/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/aitl-controller-a-type/tree/main/docs/reliability) |

---

## Purpose and Scope

The goal of this analysis is **not** to optimize controller performance.

Instead, it aims to answer the following design questions:

- How does plant aging affect response timing?
- What does adaptive control *actually* preserve?
- When does adaptation begin to **harm reliability**?
- Can this degradation be **quantified and detected by design**?

The analysis compares:

- fixed-gain PID control  
- AITL control with FSM-based adaptive gain retuning  

under identical friction aging conditions.

---

## Analysis Structure (Demo Mapping)

This reliability study is organized as a **four-step design sequence**:

| Demo | File | Role |
|------|------|------|
| **06** | `demo_06_friction_aging_waveform.md` | Phenomenon visualization (waveforms) |
| **07** | `demo_07_metrics_dt_amp.md` | Quantitative metrics (Δt, amplitude ratio) |
| **08** | `demo_08_fsm_dt_amp_guard.md` | FSM-based reliability decision (guard) |
| **09** | `demo_09_reliability_cost.md` | Unified reliability cost evaluation |

Each demo builds on the previous one and represents  
a **design-phase progression**, not independent experiments.

---

## Key Design Message

> **Adaptive control is not automatically reliable.**

In this study, AITL successfully compensates for delay,  
but at the cost of:

- excessive lead (over-compensation)
- reduced motion authority
- and degraded overall reliability

Crucially, these effects are:

- **not obvious from waveforms alone**
- but become explicit through Δt, amplitude, and FSM logic

This distinction marks the boundary between  
*performance optimization* and *reliability-oriented design*.

---

## Navigation

### ▶ Detailed Demo Analyses

- **Demo 06 — Friction Aging Waveforms**  
  [demo_06_friction_aging_waveform.md](./demo_06_friction_aging_waveform.md)

- **Demo 07 — Reliability Metrics (Δt, Amplitude)**  
  [demo_07_metrics_dt_amp.md](./demo_07_metrics_dt_amp.md)

- **Demo 08 — FSM Guard for Reliability**  
  [demo_08_fsm_dt_amp_guard.md](./demo_08_fsm_dt_amp_guard.md)

- **Demo 09 — Reliability Cost Trade-off**  
  [demo_09_reliability_cost.md](./demo_09_reliability_cost.md)

---

## Reference Figure

- 🖼 **Timing degradation under friction aging**  
  [pid_vs_aitl_friction_aging.png](
  https://samizo-aitl.github.io/aitl-controller-a-type/data/pid_vs_aitl_friction_aging.png
  )

This figure provides a *phenomenological overview* only.  
All reliability conclusions are derived from quantitative metrics  
and FSM-based decisions described in the demos above.

---

## Relation to Other Documentation

- This section corresponds to the **Reliability Investigation**  
  introduced briefly in the main documentation index.
- The index page presents only representative conclusions.
- Detailed reasoning, metrics, and design implications are contained here.

---

## Summary

This reliability chapter demonstrates that:

- timing degradation can be quantified (Δt)
- authority loss can be detected (amplitude ratio)
- adaptive behavior can and **should be stopped by design**

The result is not a failure of AITL,  
but a **clear design boundary** between:

> *Adaptive* control  
> and  
> *Reliable adaptive* control

---

## Design Implication and Next Step

The A-Type controller successfully demonstrated adaptive control capability
under plant aging conditions.

While the feasibility of reliability-oriented control was investigated,
the current A-Type architecture was not designed to guarantee reliability,
as adaptive actions may degrade timing consistency and motion authority.

This result clarifies the design boundary of the A-Type controller and
motivates the investigation of a **B-Type architecture explicitly designed
for reliability control**, in which adaptive actions are evaluated and
accepted only if overall reliability is improved.

