# Reliability Analysis — AITL under Plant Aging (1000 days)

This document provides a **detailed reliability-oriented analysis**
of the AITL Controller A-Type under **long-term plant degradation**
equivalent to **1000 days of friction aging**.

This page expands on the brief introduction shown in the index page and
focuses on **temporal reliability**, particularly **timing degradation (Δt)**,
rather than nominal performance optimization.

---

## Scope of This Analysis

- Plant degradation modeled as progressive friction increase
- Comparison between:
  - fixed-gain PID control
  - AITL control with adaptive gain retuning
- Evaluation emphasis:
  - response timing consistency (Δt)
  - qualitative and quantitative reliability implications

The goal of this document is **not** to derive optimal control laws,
but to clarify how controller *structure* influences reliability
under uncertainty and aging.

---

## Relation to Index Page

This analysis corresponds to the following section in the main page:

- **Index.md**  
  *“Addition — Reliability Investigation under Plant Aging”*

The index page presents only representative results and conclusions,
while this document contains:
- full simulation figures
- detailed interpretation
- design-level implications for AITL

---

### Navigation

- ▶ **Index page (overview)**  
  [Reliability Analysis — AITL under Plant Aging (Index)]({{ site.url }}{{ site.baseurl }}/docs/reliability/)

- ▶ **Detailed demo analysis (friction aging)**  
  [Demo Analysis — Friction Aging (1000 days)]({{ site.url }}{{ site.baseurl }}/docs/reliability/demo_friction_aging_analysis.html)

### Figure Reference

- 🖼 **Timing degradation figure (PNG)**  
  [Open image: pid_vs_aitl_friction_aging.png](
  {{ site.url }}{{ site.baseurl }}/data/pid_vs_aitl_friction_aging.png
  )
