---
title: "AITL Controller B-Type"
description: "Reliability-first adaptive control architecture derived from A-Type reliability analysis"
layout: default
nav_order: 1
parent: "B-Type Architecture"
---

# AITL Controller B-Type  
## Reliability-First Adaptive Control Architecture

---

## Overview — Why B-Type Exists

AITL Controller **B-Type** is a reliability-oriented evolution of A-Type.  
It directly implements the key conclusion obtained from the A-Type reliability analysis:

> **Adaptive control does not necessarily guarantee reliability.**

While A-Type demonstrates *the capability to adapt*,  
B-Type is responsible for *deciding whether adaptation should be allowed*.

In short:

> **B-Type = Adaptive Control under Explicit Reliability Constraints**

---

## Design Lessons from A-Type Reliability Analysis

The A-Type reliability study under plant aging conditions revealed the following:

- Adaptive control can temporarily compensate response delay (Δt) caused by plant degradation.
- However, it may also introduce:
  - Over-compensation  
  - Loss of motion authority  
  - Long-term degradation of system reliability
- These risks cannot be identified from waveform inspection alone.

This leads to a critical design requirement:

> **A supervisory layer must judge adaptation based on reliability metrics, not performance alone.**

🔗 **Reference:**  
- A-Type Reliability Analysis  
  → [`../reliability/`](../reliability/)

---

## Design Philosophy of B-Type

B-Type is built upon three fundamental principles.

### Principle 1: Adaptation Is Permission-Based, Not a Right
Adaptive control is not always beneficial.  
Adaptation is enabled **only when reliability metrics remain within predefined limits**.

### Principle 2: Reliability Decisions Are Made by FSM
Instead of performance metrics, the FSM evaluates explicit reliability indicators such as:

- Response delay ratio: Δt / Δt₀  
- Gain compensation ratio: K / K₀  
- Amplitude ratio and saturation level  
- Adaptation frequency (chattering detection)

🔗 **Details:**  
- FSM guard metrics and logic  
  → [`fsm_guard.md`](fsm_guard.md)

### Principle 3: Guaranteed Fallback to Fixed PID
Under all circumstances, the controller must be able to fall back to a  
**conservatively designed fixed PID controller**, ensuring minimum safe operation.

---

## Architecture Overview (PID × FSM × LLM)

This layered architecture explicitly separates:
- Control execution  
- Reliability judgment  
- Design-time intelligence  

🔗 **Architecture details:**  
- PID × FSM × LLM structure  
  → [`architecture.md`](architecture.md)

---

## Positioning of A-Type and B-Type

| Aspect | A-Type | B-Type |
|---|---|---|
| Primary goal | Demonstrate adaptability | Guarantee reliability lower bound |
| Adaptive control | Always enabled | Conditionally permitted |
| Decision criterion | Performance improvement | Reliability metrics |
| Intended use | Proof of concept | Deployment and long-term operation |

> **B-Type does not replace A-Type.**  
> It builds upon the results and insights provided by A-Type.

---

## Mapping to Existing Demonstrations

B-Type directly reuses the A-Type reliability demonstrations:

- Demo06: Visualization of degradation effects  
- Demo07: Quantitative metrics (Δt, amplitude ratio)  
- Demo08: FSM-based reliability guard  
- Demo09: Reliability cost trade-off  

🔗 **Demo correspondence:**  
- A-Type → B-Type demo mapping  
  → [`demo_mapping.md`](demo_mapping.md)

---

## Summary

AITL Controller B-Type is:

- A controller that **constrains adaptation**
- A design that prioritizes **not breaking over optimizing**
- A reliability-oriented architecture for long-term operation under degradation

In essence:

> **A-Type = A controller that can adapt**  
> **B-Type = A controller that knows when it should not adapt**

---

## Next Sections (Recommended Reading Order)

1. **Architecture overview**  
   → [`architecture.md`](architecture.md)

2. **FSM reliability guard (metrics & logic)**  
   → [`fsm_guard.md`](fsm_guard.md)

3. **Reliability cost formulation**  
   → [`reliability_cost.md`](reliability_cost.md)

4. **Threshold design guidelines**  
   → [`threshold_guidelines.md`](threshold_guidelines.md)

5. **Demo mapping and integration**  
   → [`demo_mapping.md`](demo_mapping.md)
