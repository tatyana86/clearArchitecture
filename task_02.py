import math
from enum import Enum

class DeviceType(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

class RobotState:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle_degrees = 0.0
        self.current_device = DeviceType.WATER
        self.device_active = False

def move_robot(state, distance):
    angle_rad = math.radians(state.angle_degrees)
    dx = distance * math.cos(angle_rad)
    dy = distance * math.sin(angle_rad)
    
    state.x += dx
    state.y += dy

def turn_robot(state, angle_delta):
    state.angle_degrees += angle_delta

def set_device(state, device_str):
    try:
        state.current_device = DeviceType(device_str.lower())
        return True
    except ValueError:
        return False

def start_device(state):
    state.device_active = True

def stop_device(state):
    state.device_active = False

def get_normalized_angle(state):
    return state.angle_degrees % 360

def process_move_command(state, parts, output):
    if len(parts) < 2:
        output.append("Ошибка: неполная команда")
        return
    
    try:
        distance = float(parts[1])
        move_robot(state, distance)
        output.append(f"POS {state.x:.2f},{state.y:.2f}")
    except ValueError:
        output.append("Ошибка: неверный формат параметра")

def process_turn_command(state, parts, output):
    if len(parts) < 2:
        output.append("Ошибка: неполная команда")
        return
    
    try:
        angle_change = float(parts[1])
        turn_robot(state, angle_change)
        normalized_angle = get_normalized_angle(state)
        output.append(f"ANGLE {normalized_angle:.1f}")
    except ValueError:
        output.append("Ошибка: неверный формат параметра")

def process_set_command(state, parts, output):
    if len(parts) < 2:
        output.append("Ошибка: неполная команда")
        return
    
    device_str = parts[1]
    if set_device(state, device_str):
        output.append(f"STATE {state.current_device.value}")
    else:
        output.append("Ошибка: недопустимый параметр")

def process_start_command(state, parts, output):
    start_device(state)
    output.append(f"START WITH {state.current_device.value}")

def process_stop_command(state, parts, output):
    stop_device(state)
    output.append("STOP")

POSSIBLE_COMMANDS = {
    'move': process_move_command,
    'turn': process_turn_command,
    'set': process_set_command,
    'start': process_start_command,
    'stop': process_stop_command
}

def execute_command(state, command_str):
    parts = command_str.strip().lower().split()
    result = []
    
    if not parts:
        return result
    
    command = parts[0]
        
    if command in POSSIBLE_COMMANDS:
        POSSIBLE_COMMANDS[command](state, parts, result)
    else:
        result.append(f"Неизвестная команда '{command}'")
    
    return result

def run_robot_program():
    state = RobotState()
        
    while True:
        command = input()
        
        if not command:
            continue
        
        result = execute_command(state, command)
        print(result)


def main():
    print("Доступные команды:")
    print("move <расстояние> - движение вперед (в метрах)")
    print("turn <угол>       - поворот (в градусах)")
    print("set <device>      - выбор устройства (water/soap/brush)")
    print("start             - включить устройство очистки")
    print("stop              - выключить устройство очистки")
    print("Введите одну из команд:")
    
    run_robot_program()

if __name__ == "__main__":
    main()