---
title: "Demo Mapping"
description: "Mapping existing A-Type demonstrations to the B-Type reliability-first control framework"
layout: default
nav_order: 6
parent: "B-Type Architecture"
---

# Demo Mapping  
## From A-Type Demonstrations to B-Type Architecture

---

## Purpose of This Mapping

This document clarifies how existing **A-Type demonstration scripts**  
are reused, reinterpreted, and integrated within the **B-Type architecture**.

No demonstrations are discarded.  
Instead, their **roles and meanings are elevated** from performance analysis to  
**reliability-based decision support**.

> **B-Type does not add complexity by adding demos —  
> it adds structure by redefining their purpose.**

---

## Overall Mapping Concept

| Layer | Role in B-Type | Source |
|---|---|---|
| Visualization | Degradation awareness | Demo06 |
| Metrics | Reliability quantification | Demo07 |
| Decision logic | Adaptation permission | Demo08 |
| Evaluation | Long-term trade-off | Demo09 |
| Integration | B-Type orchestration | Demo10 (new) |

---

## Demo06  
### Plant Degradation Visualization

**Original Purpose (A-Type)**  
- Visualize plant behavior under friction aging
- Compare fixed PID vs adaptive response

**Role in B-Type**  
- Qualitative confirmation of degradation presence
- Operator-level intuition for aging effects

**B-Type Interpretation**  
> Demo06 answers:  
> **“Is the plant degrading in a way that may threaten reliability?”**

No decision is made here.  
This demo supports **situational awareness**, not control authority.

---

## Demo07  
### Reliability Metric Extraction

**Original Purpose (A-Type)**  
- Compute response delay (Δt)
- Measure amplitude ratio and related indicators

**Role in B-Type**  
- Primary source of **normalized reliability metrics**
- Feeds quantitative inputs to the FSM guard

**Key Outputs**
- $$R_{\Delta t} = \Delta t / \Delta t_0$$  
- $$R_A = A_{\text{out}} / A_{\text{ref}}$$  

**B-Type Interpretation**  
> Demo07 answers:  
> **“How far has the system deviated from nominal behavior?”**

---

## Demo08  
### FSM-Based Reliability Guard

**Original Purpose (A-Type)**  
- Demonstrate FSM-driven adaptation logic
- Show conditional mode switching

**Role in B-Type**  
- Core implementation of **adaptation permission logic**
- Explicit enforcement of reliability guard conditions

**FSM Decisions**
- ADAPT_ALLOWED  
- ADAPT_BLOCKED  
- SAFE_MODE  

**B-Type Interpretation**  
> Demo08 answers:  
> **“Should adaptation be allowed right now?”**

This demo marks the **architectural transition** from A-Type to B-Type.

---

## Demo09  
### Reliability Cost Trade-Off

**Original Purpose (A-Type)**  
- Compare adaptive and non-adaptive strategies over time
- Visualize cumulative degradation effects

**Role in B-Type**  
- Secondary evaluation criterion
- Long-horizon reliability assessment

**Key Quantity**
- Reliability cost $$J_{\text{rel}}$$  
- Accumulated cost $$J_{\text{rel}}^{\text{acc}}$$  

**B-Type Interpretation**  
> Demo09 answers:  
> **“Is adaptation helping or harming long-term reliability?”**

---

## Demo10 (B-Type Only)  
### B-Type Controller Orchestration

**Purpose**
- Integrate Demo06–09 into a single B-Type control flow
- Demonstrate end-to-end reliability-first operation

**Responsibilities**
- Instantiate AITL B-Type controller
- Apply FSM guard and reliability cost logic
- Log adaptation permission decisions over time

**Conceptual Role**
> Demo10 answers:  
> **“What does a complete B-Type controller actually do?”**

---

## Summary Table

| Demo | B-Type Function | Decision Level |
|---|---|---|
| Demo06 | Degradation awareness | None |
| Demo07 | Metric generation | Quantitative |
| Demo08 | Adaptation permission | Discrete / FSM |
| Demo09 | Reliability evaluation | Long-term |
| Demo10 | System integration | Architectural |

---

## Key Design Message

The demonstrations form a **logical pipeline**, not isolated examples:

```
Degradation → Metrics → Guards → Cost → Decision
```

> In B-Type, demos are no longer about  
> *how well the system performs*,  
> but about *when the system must restrain itself*.

---

## Conclusion

This mapping shows that:

- B-Type is fully grounded in existing A-Type demonstrations  
- No experimental results are wasted or invalidated  
- Reliability-first control emerges from **reinterpretation, not reinvention**

---

Possible next extensions:
- Demo10 detailed walkthrough  
- Logging and visualization standards for B-Type decisions  
- Mapping demo outputs to real-system monitoring signals

---

## Evaluation Results Mapping  
### How B-Type Was Actually Evaluated

This section summarizes **what was evaluated**, **using which demos**,  
and **what conclusions were drawn** specifically for **B-Type**.

The goal is to clearly separate:

- *What the demos do*  
- *What conclusions were extracted for B-Type*

---

### Evaluation Viewpoint

B-Type is **not evaluated by performance recovery**, but by the following question:

> **Does the controller preserve a minimum reliability bound under degradation?**

Accordingly, the evaluation focuses on:

- Suppression of excessive adaptation  
- Bounded FSM activity  
- Stability of reliability metrics over time  

---

### Mapping of Evaluation Results to Demos

| Demo | Evaluation Focus | B-Type Result |
|---|---|---|
| Demo06 | Visual degradation confirmation | Aging clearly observable |
| Demo07 | Quantitative deviation metrics | Δt, amplitude ratios normalized |
| Demo08 | Adaptation permission behavior | Over-adaptation successfully blocked |
| Demo09 | Long-term reliability cost | Lower cumulative risk vs A-Type |
| Demo10 | End-to-end behavior | Reliability-first orchestration confirmed |

---

### Key Observations

#### 1. Fixed PID vs B-Type

- Fixed PID shows predictable degradation but no self-protection.
- B-Type intentionally limits compensation, avoiding hidden reliability debt.

**Interpretation:**  
B-Type prioritizes *not breaking* over *tracking recovery*.

---

#### 2. A-Type vs B-Type

- A-Type recovers phase and amplitude more aggressively.
- B-Type blocks adaptation when reliability thresholds are exceeded.

**Interpretation:**  
B-Type does not reject adaptation — it **conditions it**.

---

#### 3. FSM Guard Effectiveness

FSM guard states observed:

- ADAPT_ALLOWED: Early / mild degradation
- ADAPT_BLOCKED: Excessive gain or delay detected
- SAFE_MODE: Conservative fallback enforced

No unstable oscillatory switching was observed in B-Type operation.

---

## Re-Evaluation Plan  
### Planned Extensions for B-Type Validation

To avoid overfitting conclusions to a single scenario, B-Type will be re-evaluated under controlled extensions.

---

### 1. Threshold Sensitivity Analysis

**Purpose**
- Understand how conservative the reliability guard must be.

**Method**
- Systematically vary:
  - Δt threshold
  - Gain ratio threshold
  - FSM dwell time

**Expected Outcome**
- Identify safe operating envelopes
- Provide threshold design guidelines

---

### 2. Control Target Diversification

Current demos focus on actuator-like dynamics.

Planned additional targets:
- Thermal system (slow dynamics)
- Fluid level control
- Structural damping (second-order)

**Purpose**
- Confirm B-Type generality beyond motor-like systems.

---

### 3. LLM-Assisted Design-Time Re-Evaluation

LLM will **not** participate in real-time control.

Its role in re-evaluation:
- Analyze accumulated reliability logs
- Suggest:
  - FSM threshold adjustments
  - PID parameter set revisions

**Constraint**
- All LLM outputs remain subject to FSM guard approval.

---

## Final Positioning

With these evaluations and re-evaluation plans:

- A-Type remains a proof of adaptability
- B-Type becomes a framework for **operational reliability assurance**

> **B-Type is not optimized for best-case performance,  
> but for worst-case survivability.**

This mapping ensures that every demo contributes  
to a **traceable reliability argument**, not just illustrative behavior.

---

_End of Demo Mapping (Evaluation Extension)_

