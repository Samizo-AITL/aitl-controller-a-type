from core.base import ControllerBase

class FSMController(ControllerBase):
    def __init__(self, states, transitions, initial_state, name="fsm"):
        super().__init__(name)
        self.states = states
        self.transitions = transitions
        self.current_state = initial_state

        # 状態遷移したときの時刻を保持
        self.last_transition_time = 0.0

        # 各状態の最低滞在時間（秒）
        self.min_dwell = {
            "normal": 0.0,   # normal → high は即時OK
            "high":   0.5,   # high に入ったら最低 0.5秒は維持する
        }

    def reset(self):
        self.current_state = "normal"
        self.last_transition_time = 0.0

    def update_state(self, observation, t):
        current = self.current_state
        rules = self.transitions.get(current, [])

        # 状態滞在時間
        dwell_time = t - self.last_transition_time

        # 最低滞在時間未満 → 状態遷移を許可しない
        if dwell_time < self.min_dwell.get(current, 0.0):
            return

        # 通常の条件判定
        for cond, next_state in rules:
            if cond(observation):
                self.current_state = next_state
                self.last_transition_time = t
                break

    def compute(self, observation, t=None):
        ctrl = self.states[self.current_state]
        if hasattr(ctrl, "step"):
            return ctrl.step(observation, t)
        return ctrl(observation, t)

    def step(self, observation, t):
        self.update_state(observation, t)
        return self.compute(observation, t)
