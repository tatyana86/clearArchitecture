import math

class CleaningRobot:
    def __init__(self, transfer_func):
        self.x = 0.0
        self.y = 0.0
        self.angle_degrees = 0.0
        self.current_device = "water"
        self.device_active = False
        self.transfer = transfer_func
    
    def move(self, distance: float):
        angle_rad = math.radians(self.angle_degrees)
        dx = distance * math.cos(angle_rad)
        dy = distance * math.sin(angle_rad)
        
        self.x += dx
        self.y += dy
        self.transfer(f"POS {self.x:.2f},{self.y:.2f}")
    
    def turn(self, angle_delta: float):
        self.angle_degrees += angle_delta
        normalized_angle = self.angle_degrees % 360
        self.transfer(f"ANGLE {normalized_angle:.1f}")
    
    def set_device(self, device_str: str):
        device = device_str.lower()
        if device in ["water", "soap", "brush"]:
            self.current_device = device
            self.transfer(f"STATE {self.current_device}")
        else:
            self.transfer("Ошибка: недопустимый параметр")
    
    def start(self):
        self.device_active = True
        self.transfer(f"START WITH {self.current_device}")
    
    def stop(self):
        self.device_active = False
        self.transfer("STOP")