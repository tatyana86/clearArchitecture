import math

class Robot:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle_degrees = 0.0 
        self.current_device = 'water'
        self.device_active = False
        
    def execute_command(self, command_str):
        parts = command_str.strip().lower().split()
        if not parts:
            return
            
        command = parts[0]
        
        if command == 'move':
            if len(parts) < 2:
                print("Ошибка: неполная команда")
                return
                
            try:
                distance = float(parts[1])
                self._move(distance)
                print(f"POS {self.x},{self.y}")
            except ValueError:
                print("Ошибка: неверный формат параметра")
                
        elif command == 'turn':
            if len(parts) < 2:
                print("Ошибка: неполная команда")
                return
                
            try:
                angle_change = float(parts[1])
                self._turn(angle_change)
                normalized_angle = self.angle_degrees % 360
                print(f"ANGLE {normalized_angle}")
            except ValueError:
                print("Ошибка: неверный формат параметра")
                
        elif command == 'set':
            if len(parts) < 2:
                print("Ошибка: команда set требует параметр (water/soap/brush)")
                return
                
            device = parts[1]
            if device not in ['water', 'soap', 'brush']:
                print("Ошибка: недопустимый параметр")
                return
                
            self.current_device = device
            print(f"STATE {device}")
            
        elif command == 'start':
            self.device_active = True
            print(f"START WITH {self.current_device}")
                
        elif command == 'stop':
            self.device_active = False
            print("STOP")
                
        else:
            print(f"Неизвестная команда '{command}'")
    
    def _move(self, distance):
        angle_rad = math.radians(self.angle_degrees)
        dx = distance * math.cos(angle_rad)
        dy = distance * math.sin(angle_rad)
        
        self.x += dx
        self.y += dy
    
    def _turn(self, angle_delta):
        self.angle_degrees += angle_delta


def main():
    robot = Robot()

    print("Доступные команды:")
    print("move <расстояние> - движение вперед (в метрах)")
    print("turn <угол>       - поворот (в градусах)")
    print("set <device>      - выбор устройства (water/soap/brush)")
    print("start             - включить устройство очистки")
    print("stop              - выключить устройство очистки")
    print("Введите одну из команд:")
        
    while True:
        command = input()             

        if not command:
            continue

        robot.execute_command(command)
            
if __name__ == "__main__":
    main()