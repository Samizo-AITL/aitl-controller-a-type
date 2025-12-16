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

### Principle 3: Guaranteed Fallback to Fixed PID
Under all circumstances, the controller must be able to fall back to a  
**conservatively designed fixed PID controller**, ensuring minimum safe operation.

---

## Architecture Overview (PID × FSM × LLM)

### Inner Loop: PID (Conservative and Invariant)
- Fixed gains designed on the safe side
- Stability margin and phase margin prioritized
- Maintains minimum control authority even under severe degradation

### Middle Layer: FSM (Reliability Guard)
The FSM manages the control mode using explicit reliability states:

- NORMAL  
- DEGRADED  
- ADAPT_ALLOWED  
- ADAPT_BLOCKED  
- SAFE_MODE  

A key role of the FSM is to explicitly support  
**“the decision to stop adaptation.”**

### Outer Layer: LLM (Design-Time Intelligence)
- Redesigns FSM guard conditions and PID candidates
- Provides human-readable explanations for adaptation decisions
- Does not participate in real-time control loops

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

B-Type integrates these components into a unified  
**adaptation permission framework**.

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

The following sections detail:
- Formal definitions of reliability metrics  
- FSM guard conditions for B-Type operation  
- B-Type demonstration scenarios
