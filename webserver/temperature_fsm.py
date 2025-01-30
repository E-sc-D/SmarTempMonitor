# temperature_fsm.py
class TemperatureFSM:
    def __init__(self, T1, T2, F1, F2, DT):
        self.T1 = T1
        self.T2 = T2
        self.F1 = F1
        self.F2 = F2
        self.DT = DT
        self.state = 0
        self.window_percentage = 0.0
        self.time_in_too_hot = 0

    def update(self, T, elapsed_time):
        match self.state:
            case 0:
                if T >= self.T1:
                    self.state = 1
                    self.window_percentage = 0.01

            case 1:
                if T < self.T1:
                    self.state = 0
                    self.window_percentage = 0.0
                elif T > self.T2:
                    self.state = 2
                    self.window_percentage = 1.0
                    self.time_in_too_hot = 0
                else:
                    self.window_percentage = (T - self.T1) / (self.T2 - self.T1)

            case 2:
                if T <= self.T2:
                    self.state = 1
                else:
                    self.time_in_too_hot += elapsed_time
                    if self.time_in_too_hot >= self.DT:
                        self.state = 3

            case 3:
                pass

    def get_state(self):
        return self.state
    
    def get_frequency(self):
        if(self.state == 0):
            return self.F1
        else:
            return self.F2

    def resetState(self):
        self.state = 0
        
