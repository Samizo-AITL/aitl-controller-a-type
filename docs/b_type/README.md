# AITL Controller  
## B-Type — Reliability-First Adaptive Control

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/aitl-controller-a-type/docs/b_type/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/aitl-controller-a-type/tree/main/docs/b_type) |

---

## What Is B-Type?

**AITL Controller B-Type** is a reliability-oriented control architecture  
designed to **constrain adaptive behavior under explicit reliability limits**.

It is a direct architectural evolution of **A-Type**, derived from  
quantitative reliability analysis under long-term plant degradation.

> **A-Type answers _“How can we adapt?”_**  
> **B-Type answers _“Should we adapt?”_**

---

## One-Page Comparison: A-Type vs B-Type

| Aspect | A-Type | B-Type |
|---|---|---|
| Primary objective | Performance recovery | Reliability preservation |
| Adaptation | Always enabled | Conditionally permitted |
| Decision basis | Response improvement | Reliability metrics |
| Supervisory logic | Mode switching | Explicit adaptation blocking |
| Long-term operation | Not guaranteed | Explicitly supported |
| Failure philosophy | Try to compensate | Stop before breaking |

---

## Architectural Difference at a Glance

```mermaid
flowchart LR
    subgraph A[A-Type]
        R1[Reference]
        PID1[PID + Adaptive Logic]
        P1[Plant]
        R1 --> PID1 --> P1
        P1 --> PID1
    end

    subgraph B[B-Type]
        R2[Reference]
        PID2[Fixed PID\n(Safe Baseline)]
        FSM[FSM\nReliability Guard]
        LLM[LLM\nDesign Support]
        P2[Plant]
        R2 --> PID2 --> P2
        P2 --> PID2
        PID2 --> FSM
        FSM --> PID2
        FSM -. redesign rules .-> LLM
        LLM -. offline updates .-> FSM
    end
```

---

## Core Design Principle

> **Performance optimization must never override reliability constraints.**

B-Type enforces this principle structurally by separating:
- Control execution (PID)
- Reliability judgment (FSM)
- Design evolution (LLM)

---

## Documentation Entry Points (Start Here)

### 📘 B-Type Core Documents
- **Concept & Philosophy**  
  → [`docs/b_type/index.md`](docs/b_type/index.md)

- **Architecture (PID × FSM × LLM)**  
  → [`docs/b_type/architecture.md`](docs/b_type/architecture.md)

- **FSM Reliability Guard (Δt, K/K₀)**  
  → [`docs/b_type/fsm_guard.md`](docs/b_type/fsm_guard.md)

- **Reliability Cost Function**  
  → [`docs/b_type/reliability_cost.md`](docs/b_type/reliability_cost.md)

- **Threshold Design Guidelines**  
  → [`docs/b_type/threshold_guidelines.md`](docs/b_type/threshold_guidelines.md)

- **Demo Mapping (A-Type → B-Type)**  
  → [`docs/b_type/demo_mapping.md`](docs/b_type/demo_mapping.md)

---

## Relation to Existing A-Type Analysis

- **A-Type Reliability Analysis**  
  → [`docs/reliability/`](docs/reliability/)

B-Type is explicitly built on the conclusions drawn in the A-Type reliability chapter.

---

## Repository Structure (B-Type Focus)

```
docs/
├─ reliability/          # A-Type reliability analysis
└─ b_type/               # B-Type architecture
   ├─ index.md
   ├─ architecture.md
   ├─ fsm_guard.md
   ├─ reliability_cost.md
   ├─ threshold_guidelines.md
   └─ demo_mapping.md
```

---

## Key Message

> **A controller that knows when not to adapt  
> is more reliable than one that always tries to adapt.**

---

## Next Steps

1. Read **Architecture** → FSM role  
2. Check **FSM Guard** → formal conditions  
3. Review **Demo Mapping** → how simulations support decisions  

---

**AITL Controller B-Type**  
*Adaptive control, constrained by reliability.*
