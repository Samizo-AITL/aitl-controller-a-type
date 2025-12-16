# 【Reliability Analysis】Friction Aging における Δt・振幅・FSM 評価まとめ

【AITL Controller A-Type】

---

## 1. 目的（Why this analysis exists）

本解析の目的は、**摩擦老化（1000 days）** 下において、

* 従来 PID 制御
* AITL（PID × FSM による再チューニング）

が **「何を守り、何を犠牲にしたか」** を、
**定量指標（Δt・振幅）および FSM 判断で明確化すること**である。

波形の印象評価（demo 06）では見落とされがちな、
**過補償・制御権限低下・適応の止め時**を数値とロジックで可視化する。

---

## 2. 評価指標の定義

### 2.1 Δt（Timing Deviation）

* 定義
  基準応答（Initial）のピーク時刻と、比較対象のピーク時刻との差

[
\Delta t = t_{\text{cmp, peak}} - t_{\text{ref, peak}}
]

* 本解析では **ピーク差の平均値（Δt mean）** を使用

* 解釈

  * Δt > 0 ：遅れ（lag）
  * Δt < 0 ：前倒し（lead）

---

### 2.2 振幅比（Amplitude Ratio）

* 定義

[
A / A_0 = \frac{\max(x) - \min(x)}{\max(x_{\text{ref}}) - \min(x_{\text{ref}})}
]

* 解釈

  * 1.0 ：基準と同等の制御権限
  * < 0.9 ：制御権限低下
  * < 0.7 ：実用上危険域

---

## 3. 評価条件

* 老化モデル：摩擦項（Fc, Fs）のみ増加

* 老化量：1000 days 相当

* 制御器構成：

  * PID_only
  * AITL（FSM によるゲイン再チューニング付き）

* 使用デモ：

  * `demos/06_pid_initial_vs_aitl_friction_aging_demo.py`
  * `demos/07_reliability_metrics_dt_amp.py`
  * `demos/08_reliability_fsm_dt_amp_guard.py`

---

## 4. 数値結果（demo 08 実測）

```
=== Reliability FSM (Δt mean + Amp guard) ===

Controller | Δt mean [s] | |Δt| [s] | Amp ratio | State | GainBoost | Action
----------------------------------------------------------------------------------------------
PID       |     -0.4730 |   0.4730 |     0.902 | OK   | BLOCK    | NO ACTION
AITL      |     -1.3807 |   1.3807 |     0.888 | LEAD | BLOCK    | GAIN BOOST BLOCKED + REVERT/RELAX
```

---

## 5. 結果の解釈

### 5.1 Δt に関する考察

* **PID_only**

  * 摩擦老化により位相遅れが発生
  * 補償能力は限定的だが、|Δt| は許容範囲内

* **AITL**

  * 摩擦劣化を検出し FSM が介入
  * ゲイン強化により遅れを過剰補償
  * 結果として **ピークが大きく前倒し（LEAD）**

👉 **AITL は遅れ補償に成功したが、時間基準維持には失敗**

---

### 5.2 振幅に関する考察

* PID_only：A/A₀ = 0.902

  * 制御権限はほぼ維持

* AITL：A/A₀ = 0.888

  * 位相改善の代償として振幅が低下
  * 操作量制約・安定余裕確保が優先された挙動

👉 **時間を守るために motion authority を犠牲にした制御**

---

## 6. FSM による Reliability 判断（demo 08）

### 6.1 FSM 状態定義

| State | 条件           |    |          |
| ----- | ------------ | -- | -------- |
| OK    |              | Δt | ≤ Δt_max |
| LAG   | Δt > +Δt_max |    |          |
| LEAD  | Δt < -Δt_max |    |          |

（Δt_max = 0.8 s）

---

### 6.2 ガード条件

* 振幅下限制約：

  * A / A₀ < 0.9 → ゲイン強化禁止

* LEAD 状態：

  * 「進みすぎ」も劣化と定義
  * ゲイン強化は禁止、ロールバック／緩和を推奨

---

### 6.3 FSM 判断結果

* PID_only：

  * 状態 = OK
  * 再チューニング不要

* AITL：

  * 状態 = LEAD
  * 振幅下限違反
  * **適応は信頼性を悪化させるため BLOCK**

👉 **Adaptive 制御を止める判断が可能になった**

---

## 7. 設計的に重要な結論

### 7.1 単一指標最適化の限界

* Δt 最小化のみを目的とすると、

  * 過補償（LEAD）
  * 振幅低下（制御権限喪失）
    を引き起こす

👉 **Reliability ≠ Δt 最小化**

---

### 7.2 AITL Controller A-Type の現状位置づけ

* 遅れ検出能力：あり
* 再チューニング能力：あり
* 適応停止判断：demo 08 で初めて実装

👉 **Adaptive → Reliable Adaptive への転換点**

---

## 8. 次ステップ（設計指針）

1. Δt の絶対値化（|Δt|）を信頼性指標とする
2. Δt と振幅を統合した Reliability cost の導入

[
J_{rel} = w_t |\Delta t| + w_a \max(0, 0.9 - A/A_0)
]

3. FSM を「状態判定」から「コスト改善判定」へ拡張

---

## 9. まとめ

* demo 06：現象提示（波形）
* demo 07：定量評価（Δt・振幅）
* demo 08：判断層（FSM ガード）

本解析により、
**AITL の過補償問題を数値で特定し、設計として止められることを証明**した。

本結果は失敗報告ではなく、
**Reliability Control 設計を前進させた成果**である。

---

【END】
