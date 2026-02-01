import math

# режимы работы устройства очистки
WATER = 1
SOAP = 2
BRUSH = 3

# взаимодействие с роботом
def transfer_to_cleaner(message):
    print(message)

# перемещение
def move(transfer, dist, x, y, angle, mode):
    angle_rads = angle * (math.pi / 180.0)
    new_x = x + dist * math.cos(angle_rads)
    new_y = y + dist * math.sin(angle_rads)
    
    transfer(f"POS({new_x}, {new_y})")
    return (new_x, new_y, angle, mode)

# поворот
def turn(transfer, turn_angle, x, y, angle, mode):
    new_angle = angle + turn_angle

    transfer(f"ANGLE({new_angle})")
    return (x, y, new_angle, mode)

# установка режима работы
def set_mode(transfer, new_mode, x, y, angle, mode):
    if new_mode == 'water':
        new_mode_code = WATER
    elif new_mode == 'soap':
        new_mode_code = SOAP
    elif new_mode == 'brush':
        new_mode_code = BRUSH
    else:
        new_mode_code = mode
    
    transfer(f"STATE({new_mode_code})")
    return (x, y, angle, new_mode_code)

# начало чистки
def start(transfer, x, y, angle, mode):
    transfer(f"START WITH({mode})")
    return (x, y, angle, mode)

# конец чистки
def stop(transfer, x, y, angle, mode):
    transfer("STOP")
    return (x, y, angle, mode)

# интерпретация набора команд
def make(transfer, code, x=0, y=0, angle=0, mode=WATER):
    current_x, current_y, current_angle, current_mode = x, y, angle, mode
    
    for command in code:
        cmd = command.split(' ')
        if cmd[0] == 'move':
            current_x, current_y, current_angle, current_mode = move(
                transfer, int(cmd[1]), current_x, current_y, current_angle, current_mode
            )
        elif cmd[0] == 'turn':
            current_x, current_y, current_angle, current_mode = turn(
                transfer, int(cmd[1]), current_x, current_y, current_angle, current_mode
            )
        elif cmd[0] == 'set':
            current_x, current_y, current_angle, current_mode = set_mode(
                transfer, cmd[1], current_x, current_y, current_angle, current_mode
            )
        elif cmd[0] == 'start':
            current_x, current_y, current_angle, current_mode = start(
                transfer, current_x, current_y, current_angle, current_mode
            )
        elif cmd[0] == 'stop':
            current_x, current_y, current_angle, current_mode = stop(
                transfer, current_x, current_y, current_angle, current_mode
            )
    
    return (current_x, current_y, current_angle, current_mode)


if __name__ == "__main__":
    commands = [
        'move 100',
        'turn -90',
        'set soap',
        'start',
        'move 50',
        'stop'
    ]
    
    # все состояние передается как значения и возвращается как новые значения
    x, y, angle, mode = make(transfer_to_cleaner, commands)