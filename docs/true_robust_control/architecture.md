---
title: "Architecture"
layout: default
---

# Architecture

## Overview

True Robust Control is implemented on top of the  
**AITL (Adaptive Intelligent Three-Layer) architecture**.

Each layer has a clearly separated responsibility.

---

## Layer Responsibilities

### Inner Loop — Control Execution
- PID / H∞ controller
- Real-time stability and performance
- No reasoning, no adaptation

---

### Middle Layer — FSM (Supervision)
- Monitors degradation indicators
- Manages operational states
- Triggers design adaptation events

FSM answers:
> *What mode should the system be in now?*

---

### Outer Layer — LLM (Design Intelligence)
- Interprets degradation meaning
- Decides **which design lever to move**
- Generates redesign policies, not numbers

LLM answers:
> *What should be changed, and why?*

---

### Robust Monitor (Cross-Layer)
- Evaluates uncertainty in frequency domains
- Outputs scalar health indicators
- Feeds FSM decision logic

---

## Architectural Philosophy

- Controllers stabilize
- FSM decides
- LLM designs
- Monitors observe

No layer violates another’s responsibility.

---
