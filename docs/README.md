# AITL Controller Documentation

This site documents the **AITL (Adaptive Intelligent Three-Layer) Controller**,  
a control architecture combining:

- 🎛️ **PID** for real-time stability  
- 🔀 **FSM** for supervisory logic  
- 🧠 **LLM** for design-time intelligence  

The documentation is organized around **architectural intent**,  
not just implementation details.

---

## 🔗 Links

| Language | GitHub Pages 🌐 | GitHub 💻 |
|----------|----------------|-----------|
| 🇺🇸 English | [![GitHub Pages EN](https://img.shields.io/badge/GitHub%20Pages-English-brightgreen?logo=github)](https://samizo-aitl.github.io/aitl-controller-a-type/docs/) | [![GitHub Repo EN](https://img.shields.io/badge/GitHub-English-blue?logo=github)](https://github.com/Samizo-AITL/aitl-controller-a-type/tree/main/docs) |

---

## 🅰️ A-Type: Adaptive Control Capability

**A-Type** focuses on demonstrating *how adaptive control can be realized*.

It emphasizes:
- 🔁 Hybrid PID + FSM control
- 📈 Online adaptation behavior
- 🧪 Performance recovery under plant degradation

📘 **A-Type Reliability Analysis**  
→ [`reliability/`](reliability/)

---

## 🛡️ True Robust Control: Operational Robustness Layer

**True Robust Control** extends the AITL framework by addressing a limitation
shared by both A-Type and B-Type:

> **How should robustness itself be *operated* before theoretical guarantees fail?**

Rather than treating robustness as a fixed design outcome,
True Robust Control defines robustness as an **operational capability**.

---

### What It Adds to AITL

True Robust Control introduces the following concepts:

- 🔍 **Uncertainty $\Delta$ as a monitored state**, not a static bound
- 📡 **Frequency-aware interpretation of degradation**
  - low-frequency: performance degradation
  - high-frequency: stability margin loss
  - input-side: actuator stress
- 🚨 **Proactive intervention at $\|\Delta\|_\infty \approx 0.8$**, before guarantee breakdown
- 🧮 **Selective redesign of robustness weight functions**
  - $W_s$: performance demand  
  - $W_t$: robustness margin  
  - $W_u$: actuator protection
- 🧱 **Clear role separation**
  - FSM: *when to intervene*
  - LLM: *what design lever to move*
  - Controller: *execute safely*

---

### Relationship to A-Type and B-Type

| Layer | Role |
|---|---|
| A-Type | Demonstrates *adaptive capability* |
| B-Type | Enforces *reliability permission and responsibility* |
| **True Robust Control** | **Operates robustness as a dynamic design process** |

> **A-Type asks:** *Can the system adapt?*  
> **B-Type asks:** *Should the system adapt?*  
> **True Robust Control asks:** *How should robustness itself be operated?*

---

## ✅ Summary

> **A-Type** → proves that adaptation is possible  
> **B-Type** → ensures adaptation is applied responsibly  

Together, they form a complete adaptive control design methodology.
