---
layout: default
title: Samizo-Lab AITL Controller
---

# Samizo-Lab AITL Controller (A-type)

A lightweight educational implementation of the **AITL layered control architecture**,  
written as a **design specification**, not a marketing document.

This document fixes **architectural responsibility**,  
**runtime authority**, and **reliability boundaries** explicitly in text.

---

## 🧱 Block 1 — Architecture Specification (Normative)

This block defines the **normative architecture** of the AITL Controller.  
All subsequent blocks are **subordinate to this specification**.

---

### 1.1 Architecture Declaration

The AITL Controller is defined as a **role-separated layered architecture**:

```
Inner Loop : PID Controller  
Middle Loop: FSM (Finite State Machine, Safety & Mode Supervision)  
Adaptive Assist Layer: NN / RL (Bounded epsilon-term, Runtime Optional)  
LLM: Offline / Non-Real-Time Design Assistant (Proposal & Documentation Only)
```

This structure is **fixed and normative**.

Any interpretation that violates this structure  
is considered **architecturally invalid**.

---

### 1.2 Runtime vs Offline Responsibility Boundary

#### Runtime (Real-Time Execution Domain)

Runtime authority is **strictly limited** to:

- **PID**: baseline stability and response
- **FSM**: safety supervision and mode selection
- **NN / RL (optional)**: bounded adaptive assistance

Valid runtime configurations are **only**:

- **PID × FSM**
- **PID × FSM × NN/RL**

No other runtime composition is permitted.

---

#### Offline (Non-Real-Time Design Domain)

The offline domain includes:

- log analysis
- reliability evaluation
- redesign proposal
- documentation and audit support

**LLM belongs exclusively to this domain.**

LLM is **explicitly prohibited** from:

- real-time input or output
- direct gain injection
- control command generation
- FSM state or transition control

---

### 1.3 Industry Validity Constraint

> **LLM must never be placed inside a real-time control loop.**

Any configuration that can be interpreted as:

- PID × FSM × LLM (runtime)

is **invalid by design**,  
regardless of simulation results or observed performance.

---

### 1.4 Scope of A-Type

A-Type is defined as:

> An architecture that demonstrates **adaptive capability under supervision**,  
> while making its **reliability boundary explicit**.

A-Type does **not** claim:

- universal effectiveness
- autonomous optimization
- replacement of classical control

These exclusions are intentional.

---

### 1.5 Reading Contract

By reading further blocks, the reader agrees that:

- runtime authority is limited to PID, FSM, and optional NN/RL
- LLM is treated solely as an offline design assistant
- demonstrations are **evidence**, not prescriptions

---

## ⚙️ Block 2 — A-Type Technical Specification  
### (PID / FSM / NN-RL Adaptive Assist)

This block specifies **how A-Type is realized technically**,  
under the constraints fixed in **Block 1**.

---

### 2.1 PID Layer — Baseline Stability

**Responsibilities**
- real-time error correction
- deterministic execution
- baseline disturbance rejection

**Non-Responsibilities**
- no learning
- no adaptation
- no decision authority

The PID layer is intentionally **static during runtime**.

---

### 2.2 FSM Layer — Safety and Supervision

**Responsibilities**
- mode selection
- safe transition enforcement
- gating of adaptive assistance

Typical switching logic:

```
normal → high   (if absolute error exceeds upper threshold)  
high   → normal (if absolute error falls below lower threshold)
```

FSM holds **final runtime authority**.

---

### 2.3 Adaptive Assist Layer (NN / RL)

The adaptive layer is defined as a **bounded epsilon-term**,  
never as a primary controller.

#### Canonical form:

$$
u = u_{\text{PID}} \cdot (1 + \epsilon)
$$

with the constraint:

$$
|\epsilon| \le \epsilon_{\text{max}}
$$

---

### 2.4 Enforcement Rules (Mandatory)

At runtime:

- epsilon is always bounded
- FSM may force epsilon to zero
- epsilon must not bypass PID
- epsilon must not alter FSM logic

Violation of these rules is an **architectural failure**.

---

### 2.5 What A-Type Explicitly Excludes

A-Type does **not** include:

- NN-generated direct control commands
- RL action selection at runtime
- adaptive rewriting of FSM logic
- autonomous optimization

Any system exhibiting these behaviors  
is **not A-Type**.

---

### 2.6 Role of Reliability Boundary

A-Type assumes:

- adaptive benefit exists only in a finite region
- degradation is observable before instability
- adaptation must be restricted when metrics degrade

The decision of **whether adaptation is allowed**  
is deferred to **Block 3 and beyond**.

---

## 📊 Block 3 — Evidence, Reliability Boundary, and Aging Investigation  
### (Why A-Type Must Be Restricted)

This block provides **empirical evidence** supporting the architectural claims
defined in **Block 1** and **Block 2**.

The purpose of this block is **not performance comparison**,  
but **boundary identification**.

---

## 3.1 Purpose of Evidence in AITL

In AITL, experimental results are used to answer **only one question**:

> **“Until when is adaptive assistance safe to apply?”**

This block does **not** attempt to prove that:
- adaptive control is always superior
- A-Type should be enabled permanently
- learning-based methods replace classical control

---

## 3.2 Experimental Context — Plant Aging Model

To evaluate reliability limits, the plant is intentionally degraded.

### Aging Model Assumptions
- friction increases monotonically over time
- degradation is slow relative to control dynamics
- no sudden faults are injected
- aging equivalent spans up to **1000 days**

This model represents **long-term industrial degradation**,  
not short-term disturbances.

---

## 3.3 Evaluation Metrics (Normative)

The following metrics are treated as **design-relevant**, not optional.

### Primary Metric: Recovery Time Consistency

- delta-t: time required for the system to recover to nominal range
- emphasis on **temporal reliability**, not peak performance

### Secondary Metrics
- maximum absolute error
- oscillation persistence
- mode-switch frequency (FSM stress indicator)

---

## 3.4 Experimental Results — Aging Sweep

Across all controllers, the following trend is observed:

- performance degrades monotonically with aging
- no controller is immune to degradation
- adaptive assistance improves recovery **only within a finite aging range**

Beyond that range:
- recovery time variance increases
- oscillations persist longer
- adaptation begins to **harm temporal reliability**

---

## 3.5 Interpretation (Design-Relevant)

The key observation is **not** that A-Type fails,
but that its **usefulness is bounded**.

This implies:

- adaptive assistance is **conditionally beneficial**
- the condition is **observable**
- continued adaptation beyond the boundary is unsafe

This directly contradicts any assumption that
“more adaptation is always better”.

---

## 3.6 Why This Is Not a Tuning Problem

The observed degradation **cannot** be resolved by:
- retuning gains
- increasing adaptation aggressiveness
- changing learning rates

The failure mode is **structural**, not parametric.

Once the reliability boundary is crossed:
- adaptation amplifies uncertainty
- recovery timing becomes inconsistent
- system predictability degrades

---

## 3.7 Design Consequence (Normative)

From this evidence, the following rule is fixed:

> **Adaptive assistance must be restricted  
> once reliability metrics degrade beyond predefined limits.**

This rule is **architectural**, not heuristic.

Any AITL implementation that:
- ignores this boundary
- continues adaptation unconditionally

is considered **invalid by design**.

---

## 3.8 Role of Block 3 in the Architecture

Block 3 serves as:

- empirical justification for restriction
- transition point from capability to responsibility
- evidence layer motivating architectural extension

This block **directly motivates Block 4**.

---

## 🛡️ Block 4 — Reliability Permission, B-Type, and True Robust Control  
### (From Capability to Responsibility)

This block finalizes the **architectural evolution** of AITL.

While **Block 1–3** establish:
- what the architecture is,
- how it is implemented,
- and where it is valid,

this block answers the final question:

> **“How should adaptive control be *operated* responsibly over time?”**

---

## 4.1 Why A-Type Alone Is Insufficient

From **Block 3**, it is established that:

- adaptive assistance has a **finite reliability boundary**
- this boundary is **observable before instability**
- continued adaptation beyond this boundary is harmful

Therefore, any architecture that:
- detects the boundary
- but does nothing with it

is **architecturally incomplete**.

A-Type demonstrates **capability**,  
but does not yet enforce **responsibility**.

---

## 4.2 B-Type — Reliability Permission Layer (Normative Extension)

**B-Type** is introduced as a **mandatory supervisory extension**.

Its purpose is **not optimization**,  
but **permission control**.

---

### 4.2.1 Core Principle

> **Adaptation is not a right.  
> It is a permission granted only when reliability conditions are satisfied.**

B-Type transforms empirical evidence into an **explicit operational rule**.

---

### 4.2.2 Responsibilities of B-Type

B-Type monitors reliability indicators such as:

- recovery time consistency (delta-t)
- maximum absolute error
- oscillation persistence
- magnitude and rate of adaptive change

Based on these indicators, B-Type decides:

- whether adaptive assistance is allowed
- whether it must be restricted
- whether fallback to conservative operation is required

---

### 4.2.3 Authority Boundary

B-Type has **permission authority only**.

- it does not generate control commands
- it does not optimize performance
- it does not redesign controllers

Its sole function is to **allow or deny adaptation**.

---

## 4.3 Integration with Existing Layers

The complete runtime authority hierarchy becomes:

```
PID        : executes control deterministically
FSM        : supervises modes and safety
B-Type     : grants or revokes adaptation permission
NN / RL    : provides bounded adaptive assistance (only if permitted)
```

This ordering is **strict** and **non-negotiable**.

---

## 4.4 True Robust Control — Operating Robustness

Beyond permission control lies a deeper question:

> **“How should robustness itself be *operated*  
> before theoretical guarantees collapse?”**

**True Robust Control** addresses this question.

---

### 4.4.1 Motivation

Classical robust control:
- assumes fixed uncertainty bounds
- provides static guarantees

Industrial reality:
- uncertainty evolves over time
- degradation is gradual
- intervention must occur *before* instability

---

### 4.4.2 Core Concepts

True Robust Control introduces:

- uncertainty treated as an **observable state**
- frequency-aware interpretation of degradation
  - low-frequency: performance loss
  - high-frequency: stability margin erosion
  - input-side: actuator stress
- proactive intervention before robustness margins collapse

---

### 4.4.3 Role Separation (Strict)

In True Robust Control:

- FSM decides **when** intervention is required
- LLM decides **which design lever** to adjust (offline only)
- controllers execute deterministically without reasoning

This preserves:
- auditability
- explainability
- safety guarantees

---

## 4.5 Position of LLM (Final and Fixed)

Across all AITL variants:

> **LLM is never a runtime controller.**

Its final, fixed role is:

- offline analysis
- design alternative generation
- documentation and rationale support

Any architecture that places LLM inside a real-time loop  
is **explicitly excluded** from AITL.

---

## 4.6 Final AITL Structure (Canonical)

The complete AITL framework is summarized as:

```
Block 1 : Architectural Responsibility (Normative)
Block 2 : A-Type Technical Realization
Block 3 : Evidence and Reliability Boundary
Block 4 : B-Type Permission and True Robust Control
```

Each block is **strictly dependent** on the previous one.

---

## 4.7 Final Statement

AITL does not claim that adaptive or intelligent control
is always beneficial.

It claims something more restrictive and more important:

> **Control systems must know  
> not only how to adapt,  
> but when to stop adapting.**

This principle defines AITL  
as an **industrial-grade control architecture**,  
not an experimental control technique.

---



