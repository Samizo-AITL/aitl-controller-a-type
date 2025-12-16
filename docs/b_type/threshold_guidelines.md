---
title: "Threshold Design Guidelines"
description: "Practical guidelines for selecting FSM guard thresholds in B-Type adaptive control"
layout: default
nav_order: 5
parent: "B-Type Architecture"
---

# Threshold Design Guidelines  
## Practical Selection of Reliability Guard Limits

---

## Purpose of Threshold Guidelines

Thresholds in B-Type architecture define **the boundary between acceptable adaptation and unsafe behavior**.

They are not tuning parameters for performance optimization, but  
**engineering limits that preserve reliability under degradation**.

> Thresholds answer the question:  
> **“How far are we willing to bend before we must stop adapting?”**

---

## Fundamental Design Principle

All thresholds must satisfy the following condition:

$$
\text{Stability and controllability must be preserved even when adaptation is blocked.}
$$

Therefore, thresholds should be:
- Conservative
- Interpretable
- Justifiable from physical or operational constraints

---

## Guideline 1: Response Delay Ratio Threshold

### Metric
$$
R_{\Delta t} = \frac{\Delta t}{\Delta t_0}
$$

### Recommended Range
$$
1.2 \le R_{\Delta t}^{\max} \le 1.5
$$

### Interpretation
- Lower bound (≈1.2):  
  High-sensitivity systems, tight timing constraints
- Upper bound (≈1.5):  
  Mechanically slow or non-time-critical systems

### Design Note
If control delay exceeds 150% of nominal,  
**the system is already operating in a degraded regime** and adaptation should be blocked.

---

## Guideline 2: Gain Compensation Ratio Threshold

### Metric
$$
R_K = \frac{K}{K_0}
$$

### Recommended Range
$$
1.5 \le R_K^{\max} \le 3.0
$$

### Interpretation
- Values near 1.5:  
  Actuator-limited or safety-critical systems
- Values near 3.0:  
  Lab-scale or non-critical experimental setups

### Design Note
Large gain increases often **precede actuator saturation and oscillatory behavior**,  
making this threshold a strong early-warning indicator.

---

## Guideline 3: Amplitude Ratio Threshold

### Metric
$$
R_A = \frac{A_{\text{out}}}{A_{\text{ref}}}
$$

### Recommended Range
$$
1.2 \le R_A^{\max} \le 2.0
$$

### Interpretation
- Lower values emphasize damping and smooth response
- Higher values tolerate transient overshoot

### Design Note
Amplitude thresholds should be coordinated with  
**mechanical limits, thermal constraints, and fatigue considerations**.

---

## Guideline 4: Reliability Cost Threshold

### Metric
$$
J_{\text{rel}}
$$

### Recommended Strategy

Instead of absolute values, define the threshold relative to nominal variance:

$$
J_{\text{rel}}^{\max} =
\alpha \cdot \mathbb{E}[J_{\text{rel}}^{\text{nominal}}]
$$

where:
- $$\alpha = 2 \sim 5$$ for conservative designs

### Design Note
The reliability cost threshold should **never override individual hard guards**.  
It acts as a secondary, integrative constraint.

---

## Guideline 5: Adaptation Frequency Threshold

### Metric
$$
N_{\text{adapt}} \quad [\text{events/time}]
$$

### Recommended Rule
$$
N_{\text{adapt}}^{\max} \le 1 \text{ per dominant time constant}
$$

### Interpretation
Frequent adaptation indicates:
- Unstable supervisory logic
- Poor metric observability
- Excessive noise sensitivity

Blocking adaptation in this case **improves reliability**, not degrades it.

---

## Conservative Default Threshold Set (Example)

| Metric | Default Value |
|---|---|
| $$R_{\Delta t}^{\max}$$ | 1.3 |
| $$R_K^{\max}$$ | 2.0 |
| $$R_A^{\max}$$ | 1.5 |
| $$J_{\text{rel}}^{\max}$$ | $$3 \times$$ nominal |
| $$N_{\text{adapt}}^{\max}$$ | 1 / time constant |

This set is suitable for **initial deployment and long-term operation**.

---

## Threshold Validation Strategy

Thresholds should be validated through:

1. Aging and degradation simulations  
2. Worst-case disturbance injection  
3. Actuator saturation testing  
4. Long-horizon reliability cost evaluation  

> A valid threshold is one that blocks adaptation **before** damage or instability occurs.

---

## Summary

Thresholds in B-Type architecture:

- Define explicit reliability boundaries  
- Transform adaptive control into a **permission-based mechanism**  
- Provide predictable and explainable system behavior  

> In B-Type, conservative thresholds are not a limitation—  
> **they are the core design feature.**

---

Possible next sections:
- Mapping thresholds to physical safety limits  
- Adaptive threshold scheduling (offline only)  
- Field tuning methodology under uncertainty
