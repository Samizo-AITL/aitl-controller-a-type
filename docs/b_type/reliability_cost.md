---
title: "Reliability Cost Function"
description: "Quantitative formulation of reliability cost for B-Type adaptive control decision making"
layout: default
nav_order: 4
parent: "B-Type Architecture"
---

# Reliability Cost Function  
## Quantifying Reliability Degradation in B-Type Control

---

## Purpose of the Reliability Cost

In B-Type architecture, **reliability is treated as a measurable quantity**,  
not an abstract design intention.

The reliability cost function provides:

- A unified scalar representation of multiple degradation indicators  
- A basis for **FSM guard decisions**  
- A tool for comparing adaptive and non-adaptive control strategies  

> **The goal is not optimization, but bounded degradation.**

---

## Conceptual Definition

Let the system reliability be evaluated using a cost function:

$$
J_{\text{rel}} \ge 0
$$

where:
- $$J_{\text{rel}} = 0$$ represents nominal, healthy operation  
- Larger values indicate increasing reliability degradation  

Adaptation is permitted **only when the reliability cost remains below a predefined limit**.

---

## Normalized Metric Set

Primary contributors:

Response delay ratio:
$$
R_{\Delta t} = \frac{\Delta t}{\Delta t_0}
$$

Gain compensation ratio:
$$
R_K = \frac{K}{K_0}
$$

Amplitude ratio:
$$
R_A = \frac{A_{\text{out}}}{A_{\text{ref}}}
$$

All metrics are dimensionless and centered around unity under nominal conditions.

---

## Basic Reliability Cost Formulation

A weighted quadratic form:

$$
J_{\text{rel}} =
w_{\Delta t}(R_{\Delta t} - 1)^2
+ w_K(R_K - 1)^2
+ w_A(R_A - 1)^2
$$

where:
- $$w_{\Delta t}, w_K, w_A$$ are design weights  

---

## Threshold-Based Decision Rule

$$
J_{\text{rel}} \le J_{\text{rel}}^{\max}
$$

If violated, the FSM transitions toward **ADAPT_BLOCKED** or **SAFE_MODE**.

---

## Time-Accumulated Reliability Cost (Optional)

$$
J_{\text{rel}}^{\text{acc}}(T)
= \int_0^T J_{\text{rel}}(t)\,dt
$$

This captures **chronic reliability degradation** over long horizons.

---

## Summary

The reliability cost function:

- Quantifies degradation explicitly  
- Supports explainable FSM decisions  
- Ensures performance gains do not erode reliability  

> In B-Type, adaptation is allowed  
> **only when reliability cost remains bounded**.
