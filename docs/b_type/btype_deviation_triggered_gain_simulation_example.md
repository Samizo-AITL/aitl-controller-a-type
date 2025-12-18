---
title: "Simulation Example: Deviation Trigger → Pre-Approved Gain Application"
author: "Samizo-AITL"
date: 2025-12-19
category: "B-Type Control Design"
tags:
  - Simulation Example
  - PID Control
  - FSM
  - Gain Asset
  - V–I Constraint
  - Reliability Guard
---

# Simulation Example (Representative Only)

本節は、設計指針（Policy）の理解補助として、**代表的な1事例**を示します。  
ここで示す数値・波形は「一般性の証明」ではなく、**設計フローの妥当性を直感的に確認するための例示**です。

---

## 1. Scenario

### 1.1 Control Objective
- 位置応答 $x(t)$ を参照 $x_{\text{ref}}$ に追従させる（PIDが主制御）
- 経年劣化により摩擦が増加し、応答がベースラインから乖離する

### 1.2 Baseline (Initial Reference)
- **day=0** の PID 応答を **baseline波形**として保存する

### 1.3 Deviation Metrics (Example)
- Amplitude deviation: $\Delta A$
- Timing deviation: $\Delta t$

※本例では、実装の都合上「波形比較（窓比較）」により乖離を判定してもよい（ポリシーは「乖離で判断する」ことが本質）。

---

## 2. Deviation Trigger & Gain Application (Policy Demonstration)

### 2.1 Trigger Rule (Generic Form)
しきい値は設計パラメータ $\theta$ とする。

$$
\Delta A \ge \theta_A \;\; \textbf{OR} \;\; \Delta t \ge \theta_t
$$

成立時、FSMは **ゲインを計算しない**。  
FSMは **承認済みゲイン資産**（例：`PID_DEGRADED_1`）を適用する。

### 2.2 V–I Constraints (Runtime)
本例ではアクチュエータ入力を **V–I制約**で制限する。

- 電圧飽和：$|V| \le V_{\max}$
- 電流飽和：$|I| \le I_{\max}$

信頼性の観点では以下の監視が重要である。

- 飽和率：`isat_rate`
- 操作量：$\int |I|\,dt$（V–I負荷の累積）

---

## 3. How to Reproduce (Files)

### 3.1 Option A: Sweep Script (Reference Implementation)
対象スクリプト：
- `06a_incremental_comparison_friction_aging_sweep.py`

出力（例）：
- `data/06a_metrics_summary.csv`
- `data/06a_all_comparison_day{D}.png`
- `data/06a_sweep_amp.png`
- `data/06a_sweep_effort.png`
- `data/06a_sweep_isat.png`

### 3.2 Option B: Trigger-Focused Demo (Minimal Example)
対象スクリプト：
- `demos/11_fsm_trigger_10pct_demo.py`（“day0でB-Type≡PID”版）

出力（例）：
- `data/11_baseline_day0.csv`
- `data/11_metrics_vs_day.csv`
- `data/11_waveforms_day{day}.png`（FSM発火点の縦線付き）

---

## 4. Representative Example (One Case)

### 4.1 Selected Case
- **day = 1000**（例：劣化が進み、baselineからの乖離が検出されるケース）

比較する波形：
- Baseline：`day=0` PID 応答（破線）
- Current：`day=1000` PID 応答
- B-Type：`day=1000`（FSM + 承認済みゲイン資産 + Guard）

参照図（いずれか一つで十分）：
- `data/06a_all_comparison_day1000.png`（4系列比較）
  - または
- `data/11_waveforms_day1000.png`（Baseline / PID / B-Type + FSM発火線）

### 4.2 What to Observe (Checklist)
次が確認できれば、本Exampleは成立する。

1. **通常域**：乖離が小さい区間では、B-TypeはPIDに近い（不要な介入がない）
2. **乖離検出**：$\Delta A$ または $\Delta t$ が $\theta$ を超え、FSMが状態遷移する
3. **適用動作**：FSMは「承認済みゲイン資産」を適用する（計算はしない）
4. **安全側監督（任意/推奨）**：V–I制約と `isat_rate` / $\int |I|dt$ が悪化しない範囲で適用される

### 4.3 Minimal Metrics to Report (Example Format)
`06a_metrics_summary.csv` または `11_metrics_vs_day.csv` から、以下を1行だけ抜粋して載せる（値は実測で記入）。

- day = 1000
- deviation status: triggered / not triggered
- `isat_rate`（電流飽和率）
- $\int |I|dt$（操作量）
- （任意）$\Delta A$, $\Delta t$

記載例（数値はあなたの実測で置換）：

- day=1000：FSM trigger = **True**
- `isat_rate` = (measured)
- $\int |I|dt$ = (measured)
- $\Delta A$ または $\Delta t$ = (measured)

---

## 5. Notes (Interpretation)
- 本Exampleの目的は「特定プラントの性能最適化」ではなく、**設計指針（乖離検知 → 承認済みゲイン適用 → V–I制約下で安全）**の理解補助である。
- したがって、波形を baseline に完全一致させることよりも、**安定性とV–I負荷（飽和率・累積電流）を悪化させないこと**を優先する。

---

*End of Simulation Example*
