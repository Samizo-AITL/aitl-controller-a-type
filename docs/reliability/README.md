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

under identical plant aging and disturbance conditions.

---

## Analysis Structure (Demo Mapping)

This reliability study is organized as a **design-to-evidence sequence**,
linking **architectural intent** to **reproducible results**.

Rather than independent experiments, each demo represents a
**progressive refinement of reliability reasoning**.

| Demo | Artifact | Role |
|------|----------|------|
| **12** | `12_vi_current_control_sales_demo.py` | Phenomenon visualization (waveforms under aging & disturbance) |
| **13** | `13_aging_sweep_delta_t.py` | Quantitative reliability metrics (Δt, max|e| vs aging) |
| **15** | `15_fsm_explainability_demo.py` | Explainable supervisory decisions (FSM transition rationale) |
| **—** | *(design synthesis)* | Reliability boundary identification (motivation for B-Type) |

### Interpretation

- **Demo 12** answers *what happens* under aging and disturbance  
- **Demo 13** quantifies *how reliability degrades* using explicit metrics  
- **Demo 15** explains *why supervisory decisions occur*, enabling auditability  

Together, these demos establish that:

- performance recovery alone is insufficient to guarantee reliability
- temporal consistency (Δt) must be monitored explicitly
- adaptive actions require **design-time permission and stopping logic**

This sequence defines the **design boundary of the A-Type controller** and
provides the **evidence base** motivating a reliability-oriented **B-Type architecture**.

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
- but become explicit through Δt and FSM-based decision logic

This distinction marks the boundary between  
*performance optimization* and *reliability-oriented design*.

---

## Navigation

### ▶ Demonstration Results (Reproducible Evidence)

- **Demo 12 — V–I Current Control under Aging & Disturbance**  
  Phenomenological waveform comparison (Fixed PID / PID×FSM / AITL)  
  → Result: `data/12_vi_current_control_sales_demo.png`  
  → Code: `demos/12_vi_current_control_sales_demo.py`

- **Demo 13 — Reliability Metrics vs Aging (Δt, max|e|)**  
  Quantitative evaluation of temporal reliability and safety degradation  
  → Result: `data/13_aging_sweep_delta_t.png`  
  → Code: `demos/13_aging_sweep_delta_t.py`

- **Demo 15 — FSM Explainability (Why Adaptation Switched)**  
  Audit-ready visualization of supervisory decisions and thresholds  
  → Result: `data/15_fsm_explainability_demo.png`  
  → Code: `demos/15_fsm_explainability_demo.py`

These demos constitute the **evidence layer** supporting the
reliability conclusions of the A-Type controller.

---

## Reference Figure

- 🖼 **Timing degradation under friction aging**  
  [pid_vs_aitl_friction_aging.png](https://samizo-aitl.github.io/aitl-controller-a-type/data/pid_vs_aitl_friction_aging.png)

This figure provides a *phenomenological overview* only.  
All reliability conclusions are derived from quantitative metrics  
and FSM-based decisions described in the demos above.

---

## Summary

This reliability chapter demonstrates that:

- timing degradation can be quantified (Δt)
- authority loss can be detected (max|e|)
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

However, the current A-Type architecture is **not designed to guarantee
reliability**, as adaptive actions may degrade timing consistency and
motion authority.

This result clarifies the design boundary of the A-Type controller and
motivates the investigation of a **B-Type architecture explicitly designed
for reliability control**, in which adaptive actions are evaluated and
accepted only if overall reliability is improved.
