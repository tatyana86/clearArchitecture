import math
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

# режимы работы устройства очистки
WATER = 1
SOAP = 2
BRUSH = 3


# взаимодействие с роботом вынесено в отдельную функцию
def transfer_to_cleaner(message):
    print(message)


# перемещение
def move(transfer, dist, state):
    angle_rads = state.angle * (math.pi / 180.0)
    new_state = RobotState(
        state.x + dist * math.cos(angle_rads),
        state.y + dist * math.sin(angle_rads),
        state.angle,
        state.state
    )
    transfer(f"POS({new_state.x}, {new_state.y})")
    return new_state

# поворот
def turn(transfer, turn_angle, state):
    new_state = RobotState(
        state.x,
        state.y,
        state.angle + turn_angle,
        state.state
    )
    transfer(f"ANGLE({new_state.angle})")
    return new_state

# установка режима работы
def set_state(transfer, new_internal_state, state):
    if new_internal_state == 'water':
        self_state = WATER
    elif new_internal_state == 'soap':
        self_state = SOAP
    elif new_internal_state == 'brush':
        self_state = BRUSH
    else:
        return state
    
    new_state = RobotState(
        state.x,
        state.y,
        state.angle,
        self_state
    )
    transfer(f"STATE({self_state})")
    return new_state

# начало чистки
def start(transfer, state):
    transfer(f"START WITH({state.state})")
    return state

# конец чистки
def stop(transfer, state):
    transfer("STOP")
    return state

# интерпретация набора команд
def make(transfer, code, state):
    current_state = state
    for command in code:
        cmd = command.split(' ')
        if cmd[0] == 'move':
            current_state = move(transfer, int(cmd[1]), current_state)
        elif cmd[0] == 'turn':
            current_state = turn(transfer, int(cmd[1]), current_state)
        elif cmd[0] == 'set':
            current_state = set_state(transfer, cmd[1], current_state)
        elif cmd[0] == 'start':
            current_state = start(transfer, current_state)
        elif cmd[0] == 'stop':
            current_state = stop(transfer, current_state)
    return current_state


class RobotCleaner:
    def __init__(self):
        self._state = RobotState(x=0.0, y=0.0, angle=0, state=WATER)
    
    def _transfer(self, message):
        transfer_to_cleaner(message)
    
    def move(self, distance):
        self._state = move(self._transfer, distance, self._state)
    
    def turn(self, angle):
        self._state = turn(self._transfer, angle, self._state)
    
    def set_state(self, mode):
        self._state = set_state(self._transfer, mode, self._state)
    
    def start(self):
        self._state = start(self._transfer, self._state)
    
    def stop(self):
        self._state = stop(self._transfer, self._state)
    
    def execute_commands(self, commands):
        self._state = make(self._transfer, commands, self._state)


if __name__ == "__main__":
    cleaner = RobotCleaner()

    cleaner.execute_commands(["move 100", "turn 90", "set brush", "start", "move 30", "stop"])