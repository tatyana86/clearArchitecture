import math
from enum import Enum

class DeviceType(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

class CleaningRobot:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle_degrees = 0.0
        self.current_device = DeviceType.WATER
        self.device_active = False
    
    def move(self, distance: float):
        angle_rad = math.radians(self.angle_degrees)
        dx = distance * math.cos(angle_rad)
        dy = distance * math.sin(angle_rad)
        
        self.x += dx
        self.y += dy
        print(f"POS {self.x:.2f},{self.y:.2f}")
    
    def turn(self, angle_delta: float):
        self.angle_degrees += angle_delta
        normalized_angle = self.angle_degrees % 360
        print(f"ANGLE {normalized_angle:.1f}")
    
    def set_device(self, device_str: str):
        try:
            self.current_device = DeviceType(device_str.lower())
            print(f"STATE {self.current_device.value}")
        except ValueError:
            print("Ошибка: недопустимый параметр")
    
    def start(self):
        self.device_active = True
        print(f"START WITH {self.current_device.value}")
    
    def stop(self):
        self.device_active = False
        print("STOP")


def main():
    robot = CleaningRobot()
    
    print("Доступные команды:")
    print("move <расстояние> - движение вперед (в метрах)")
    print("turn <угол>       - поворот (в градусах)")
    print("set <device>      - выбор устройства (water/soap/brush)")
    print("start             - включить устройство очистки")
    print("stop              - выключить устройство очистки")
    print("Введите команды (пустая строка для выхода):")
    
    while True:
        try:
            command = input()

            if not command:
                continue
            
            parts = command.strip().lower().split()
                   
            cmd = parts[0]
            
            if cmd == 'move':
                if len(parts) < 2:
                    print("Ошибка: неполная команда")
                    continue
                try:
                    distance = float(parts[1])
                    robot.move(distance)
                except ValueError:
                    print("Ошибка: неверный формат параметра")
            
            elif cmd == 'turn':
                if len(parts) < 2:
                    print("Ошибка: неполная команда")
                    continue
                try:
                    angle_change = float(parts[1])
                    robot.turn(angle_change)
                except ValueError:
                    print("Ошибка: неверный формат параметра")
            
            elif cmd == 'set':
                if len(parts) < 2:
                    print("Ошибка: неполная команда")
                    continue
                robot.set_device(parts[1])
            
            elif cmd == 'start':
                robot.start()
            
            elif cmd == 'stop':
                robot.stop()
            
            else:
                print(f"Неизвестная команда '{cmd}'")
                
        except KeyboardInterrupt:
            print("\nЗавершение работы")
            break
        except EOFError:
            print("\nЗавершение работы")
            break


if __name__ == "__main__":
    main()