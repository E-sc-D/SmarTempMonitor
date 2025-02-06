# temperature_fsm.py
import math

class TemperatureFSM:
    def __init__(self, T1, T2, F1, F2, DT):
        self.T1 = T1
        self.T2 = T2
        self.F1 = F1
        self.F2 = F2
        self.DT = DT
        self.state = 0
        self.window_percentage = 0
        self.time_in_too_hot = 0
        self.frequency_sent = 0

    def update(self, T, elapsed_time):
        match self.state:
            case 0:
                if T >= self.T1:
                    self.state = 1
                    self.frequency_sent = 0

            case 1:
                if T < self.T1:
                    self.state = 0
                    self.window_percentage = 0
                    self.frequency_sent = 0
                elif T > self.T2:
                    self.state = 2
                    self.window_percentage = 100
                    self.time_in_too_hot = 0
                    self.frequency_sent = 0
                else:
                    self.window_percentage = math.clamp(
                            math.round(((T - self.T1) / (self.T2 - self.T1)*100 ),0),
                        1,100)

            case 2:
                if T <= self.T2:
                    self.state = 1
                    self.frequency_sent = 0
                else:
                    self.time_in_too_hot += elapsed_time
                    if self.time_in_too_hot >= self.DT:
                        self.state = 3
                        self.frequency_sent = 0

            case 3:
                pass

    def get_state(self):
        return self.state
    
    def get_frequency(self):
        if(self.state == 0):
            return self.F1
        else:
            return self.F2

    def is_frequency_sent(self):
        return self.frequency_sent

    def resetState(self):
        self.state = 0


        
