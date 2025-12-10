class AITLLLM:
    """
    A-type LLM（適応ゲイン調整）。
    high のときだけ kp を増減する。
    """

    def __init__(
        self,
        high_thresh=0.4,
        low_thresh=0.1,
        kp_step_up=0.05,
        kp_step_down=0.02,
        kp_min=0.5,
        kp_max=3.0,
    ):
        self.high_thresh = high_thresh
        self.low_thresh = low_thresh
        self.kp_step_up = kp_step_up
        self.kp_step_down = kp_step_down
        self.kp_min = kp_min
        self.kp_max = kp_max

    def adjust(self, state, kp, error):
        if state != "high":
            return kp

        e = abs(error)

        if e > self.high_thresh:
            kp += self.kp_step_up
        elif e < self.low_thresh:
            kp -= self.kp_step_down

        return max(self.kp_min, min(kp, self.kp_max))
