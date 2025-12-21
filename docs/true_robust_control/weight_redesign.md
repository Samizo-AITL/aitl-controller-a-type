---
title: "Weight Redesign Strategy"
layout: default
---

# Weight Redesign Strategy

## Why Weights Are the Correct Levers

In H∞ control, weight functions define:
- performance demand
- robustness margin
- actuator protection

They encode **design intent**.

---

## Strict Rule

> **Never redesign all weights simultaneously.**

Global redesign:
- destroys design intent
- causes unnecessary conservatism
- complicates validation

---

## One-to-One Mapping

| Degradation Type | Weight to Redesign | Purpose |
|-----------------|-------------------|---------|
| Low-frequency Δ | \( W_s \) | Relax performance demand |
| High-frequency Δ | \( W_t \) | Increase robustness margin |
| Input-side Δ | \( W_u \) | Protect actuators |

---

## Role of the LLM

The LLM does:
- qualitative reasoning
- strategy selection
- direction-of-change decisions

The LLM does **not**:
- tune numerical parameters
- run optimization loops
- replace control synthesis

---

## Separation of Concerns

- LLM: *what to change*
- Templates / code: *how to change*
- FSM: *when to change*

---
