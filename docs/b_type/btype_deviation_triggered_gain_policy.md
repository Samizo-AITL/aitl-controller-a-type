---
title: "【AITL】Deviation-Triggered Gain Application Policy (FSM × Expert-Approved Gain Assets)"
author: "Samizo-AITL"
date: 2025-12-19
category: "B-Type Control Design"
tags:
  - PID Control
  - FSM
  - Gain Scheduling
  - Reliability Guard
  - Deviation Metrics
  - Design Policy
---

# Deviation-Triggered Gain Application Policy
**(FSM × Expert-Approved Gain Assets / AITL B-Type Design Guideline)**

## 1. Purpose
本書は、AITLのB-Type制御において、**初期（健全時）PID応答からの乖離**を用いてFSMが介入判断を行い、**事前に承認されたゲイン資産**を適用するための**設計指針（Policy）**を定義します。

本指針は「特定の閾値（例：10%）を固定する」ものではなく、**閾値を設計パラメータとして定義し、運用可能な形で責任分界を明確化する**ことを目的とします。

---

## 2. Core Principle (Separation of Roles)
AITLの基本方針は、役割分担を明確に分離することです。

- **PID**：実時間制御（主制御器）。通常運転の安定性と性能を担保する。
- **FSM**：監督層。乖離（deviation）を検知し、**ゲイン資産の適用条件成立**を判断する。
- **Engineer (Expert)**：ゲイン資産（Gain Set）をオフラインで設計・検証・承認する責任主体。
- **Reliability Guard（任意/推奨）**：V–I制約や飽和率等の信頼性指標で、適用の安全性を監督する。

> FSMは「ゲインを計算」しません。FSMは「適用するか否か」を判断し、適用するのは**承認済み資産のみ**です。

---

## 3. Baseline Definition (Initial Reference)
### 3.1 Baseline
- **day=0（健全時）**のPID応答を**基準波形（baseline）**として保存します。
- ベースラインは、以後の乖離判定の参照として用います。

### 3.2 Comparison Rule
乖離判定は、単なる絶対誤差ではなく、**初期ベースラインとの比較**で行います。

---

## 4. Deviation Metrics
本指針では、代表的な乖離指標として **Amplitude** と **Timing** を例示します（必要に応じて拡張可能）。

### 4.1 Amplitude Deviation
$$
\Delta A = \frac{\left|A_{\text{current}} - A_0\right|}{A_0}
$$

### 4.2 Timing / Period Deviation
$$
\Delta t = \frac{\left|t_{\text{current}} - t_0\right|}{t_0}
$$

---

## 5. Threshold Policy (No Fixed Number)
### 5.1 Threshold is a Design Parameter
乖離閾値は、特定の数値を固定せず、**設計パラメータ $\theta$**として定義します。

- $\theta_A$：Amplitude側の閾値
- $\theta_t$：Timing側の閾値

閾値は以下に基づき、技術者が決定します：
- 性能要求（精度、応答時間、オーバーシュート）
- 信頼性要求（飽和率、熱、寿命）
- 安全余裕（安定余裕、V–I制約）
- 顧客要求・商用制約（予防保全方針、説明可能性）

> 本指針の主張は「閾値が存在する設計思想」であり、特定の割合値は対象ごとに設計されます。

### 5.2 Trigger Logic
FSMの発動条件は、基本的に**OR条件**を推奨します（片側だけの悪化でも保護を開始するため）。

$$
\Delta A \ge \theta_A \;\; \textbf{OR} \;\; \Delta t \ge \theta_t
$$

---

## 6. Gain Asset Policy (Expert-Approved Only)
### 6.1 Gain Assets
運転中に適用可能なゲインは、**事前に設計・検証・承認された資産**に限定します。

例：
- `PID_BASE`：健全時（baseline）運転用
- `PID_DEGRADED_1`：乖離閾値到達時（例：閾値1）用
- `PID_DEGRADED_2`：さらに進行した劣化用（任意）

### 6.2 Who Designs Gains
ゲイン候補の算出において、技術者は任意の方法を用いて構いません。

- 手計算・経験則・従来の同定手法
- シミュレーションベース調整
- **LLMの活用（任意）**：候補生成・整理・設計理由の言語化支援

ただし、以下を厳守します。

> **LLMは候補を提案できるが、適用するか否かの判断と承認責任は技術者が負う。**  
> 運転時に適用されるのは、技術者が承認したゲイン資産のみである。

---

## 7. Runtime Application Rules (Safe Transition)
乖離閾値成立後にゲイン資産を適用する際は、以下の安全規則を適用します。

### 7.1 No Instant Switch
- **瞬時切替は禁止**（切替ショックにより安定性が損なわれるため）
- 推奨：ランプ適用（一定時間で補間）

### 7.2 Integrator Handling
- ゲイン切替時は、積分器を適切に扱います（例：リセット、フリーズ、アンチワインドアップ）
- 目的：切替直後の過大操作量や振動励起を防止

### 7.3 V–I Constraint Awareness
- 制御入力はV–I制約を常に満たすように設計します（飽和・熱・寿命を含む）
- 推奨：Reliability Guardで以下を監視
  - 飽和率（isat_rate）
  - 電流積分（例：$\int |I|\,dt$）
  - 長期コスト（累積）

---

## 8. Reliability Guard Policy (Recommended)
Reliability Guardは、FSMが「適用しようとする」資産に対して、信頼性観点で安全性を監督します。

- Guardは「より良い性能」ではなく「安全側」を優先します。
- 指標悪化時は、適用抑制・段階適用・ロールバック等を許容します。

---

## 9. Summary (Design Policy Statement)
- PIDは常に主制御器（通常運転の安定性と性能）
- FSMは乖離（Deviation）を監視し、閾値 $\theta$ 超過を判断するだけ
- 閾値の数値は固定しない（対象・要求・安全余裕に基づき技術者が設計）
- ゲインは運転中に計算しない（**承認済みゲイン資産のみ適用**）
- LLMは設計支援として利用可能だが、採用判断は技術者が担う
- 適用は安全遷移（ランプ、積分器処理、V–I制約、Guard監督）で行う

---

*End of document*
