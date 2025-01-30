# temperature_fsm.py
class TemperatureFSM:
    def __init__(self, T1, T2, F1, F2, DT):
        self.T1 = T1
        self.T2 = T2
        self.F1 = F1
        self.F2 = F2
        self.DT = DT
        self.state = "NORMAL"
        self.window_percentage = 0.0
        self.time_in_too_hot = 0

    def update(self, T, elapsed_time):
        match self.state:
            case "NORMAL":
                if T >= self.T1:
                    self.state = "HOT"
                    self.window_percentage = 0.01

            case "HOT":
                if T < self.T1:
                    self.state = "NORMAL"
                    self.window_percentage = 0.0
                elif T > self.T2:
                    self.state = "TOO_HOT"
                    self.window_percentage = 1.0
                    self.time_in_too_hot = 0
                else:
                    self.window_percentage = (T - self.T1) / (self.T2 - self.T1)

            case "TOO_HOT":
                if T <= self.T2:
                    self.state = "HOT"
                else:
                    self.time_in_too_hot += elapsed_time
                    if self.time_in_too_hot >= self.DT:
                        self.state = "ALARM"

            case "ALARM":
                pass

    def get_state(self):
        return {
            "state": self.state,
            "window_percentage": self.window_percentage,
            "frequency": self.F1 if self.state == "NORMAL" else self.F2
        }
