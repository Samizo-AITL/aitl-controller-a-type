class PIDController:
    def __init__(self, kp, ki, kd, dt=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.reset()

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0

    def step(self, error, t=None):
        p = self.kp * error
        self.integral += error * self.dt
        i = self.ki * self.integral
        d = self.kd * (error - self.prev_error) / self.dt
        self.prev_error = error
        return p + i + d
