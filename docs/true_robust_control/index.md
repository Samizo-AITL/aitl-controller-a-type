---
title: "True Robust Control"
layout: default
---

# True Robust Control
### Operating H∞ Robustness with FSM and LLM

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/aitl-controller-a-type/docs/true_robust_control/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/aitl-controller-a-type/tree/main/docs/true_robust_control) |

---

## Overview

**True Robust Control** is a design philosophy that redefines classical H∞ robust control  
as an **operational capability**, rather than a static offline guarantee.

Instead of assuming a fixed worst-case uncertainty,  
this framework treats uncertainty as a *state* that is:

- monitored,
- interpreted,
- and acted upon *before* theoretical guarantees break.

---

## Core Idea

> **Robustness is not a number.  
> It is the ability to detect, decide, and adapt.**

In this framework:

- H∞ control defines the **guarantee boundary**
- FSM manages **operational state transitions**
- LLM performs **design-level reasoning**
- Weight functions \( W \) are used as **tactical levers**

---

## Architecture at a Glance

The framework is built on the AITL (Adaptive Intelligent Three-Layer) structure:

- **Inner Loop**  
  PID / H∞ control for real-time stability

- **Middle Layer**  
  FSM for degradation-aware mode switching

- **Outer Layer**  
  LLM for weight redesign decisions

- **Robust Monitor**  
  Frequency-domain uncertainty evaluation

---

## Key Concepts

- Uncertainty Δ is decomposed into:
  - low-frequency
  - high-frequency
  - input-side components
- When effective ∥Δ∥∞ reaches **0.8**,  
  the system proactively shifts its control strategy
- Only the relevant weight \( W_s, W_t, W_u \) is redesigned  
  — never all at once

---

## Relationship to AITL Types

- **A-Type**  
  Base architecture and operational mechanism

- **True Robust Control (this theme)**  
  Operational robustness as a first-class design concept

- **B-Type**  
  Future extension toward reliability-first systems

---

## Documents

- [Concept](concept.md)  
  Definition and motivation of True Robust Control

- [Architecture](architecture.md)  
  Layered structure and responsibility separation

- [Uncertainty as State](delta_as_state.md)  
  Why Δ must be monitored, not assumed

- [Weight Redesign Strategy](weight_redesign.md)  
  How and why only specific weights are modified

- [Roadmap](roadmap.md)  
  Planned implementation and validation steps

---

## Scope and Intent

This work is:

- not a replacement for H∞ theory
- not an AI-optimized control scheme

It is an attempt to formalize  
**how experienced control engineers actually operate robustness in the field**.

---

## Start Here

If you are new to this theme, begin with:

1. **Concept**
2. **Architecture**
3. **Uncertainty as State**

---

Robust control is not about never failing.  
**It is about knowing *when* and *how* to step back safely.**

---

*This documentation evolves alongside the AITL Controller A-Type project.*
