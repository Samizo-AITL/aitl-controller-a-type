from core.base import ControllerBase

class HybridController(ControllerBase):
    def __init__(self, fsm, pid_map, name="hybrid"):
        super().__init__(name)
        self.fsm = fsm
        self.pid_map = pid_map

    def reset(self):
        self.fsm.reset()
        for p in self.pid_map.values():
            p.reset()

    def step(self, observation, t=None):
        self.fsm.update_state(observation)
        s = self.fsm.current_state
        u = self.pid_map[s].step(observation, t)
        return u, s
