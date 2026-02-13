import math
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3

def transfer_to_cleaner(message):
    print(message)

def move(transfer, dist, state):
    angle_rads = state.angle * (math.pi/180.0)
    new_state = RobotState(
        state.x + dist * math.cos(angle_rads),
        state.y + dist * math.sin(angle_rads),
        state.angle,
        state.state)
    transfer(('POS(', new_state.x, ',', new_state.y, ')'))
    return new_state

def turn(transfer, turn_angle, state):
    new_state = RobotState(
        state.x,
        state.y,
        state.angle + turn_angle,
        state.state)
    transfer(('ANGLE', state.angle))
    return new_state

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
        self_state)
    transfer(('STATE', self_state))
    return new_state

def start(transfer, state):
    transfer(('START WITH', state.state))
    return state

def stop(transfer, state):
    transfer(('STOP',))
    return state


class ConcatenativeRobot:
    def __init__(self, transfer_func):
        self.transfer = transfer_func
        self.state = RobotState(0.0, 0.0, 0, WATER)
        self.stack = []
    
    def execute(self, program):
        words = program.split()
        for word in words:
            try:
                num = float(word)
                self.stack.append(num)
                continue
            except ValueError:
                pass
            
            if word == 'move':
                dist = self.stack.pop()
                self.state = move(self.transfer, dist, self.state)
            elif word == 'turn':
                angle = self.stack.pop()
                self.state = turn(self.transfer, angle, self.state)
            elif word == 'set':
                mode = self.stack.pop()
                self.state = set_state(self.transfer, mode, self.state)
            elif word == 'start':
                self.state = start(self.transfer, self.state)
            elif word == 'stop':
                self.state = stop(self.transfer, self.state)
            else:
                self.stack.append(word)


robot = RobotInterpreter(transfer_to_cleaner)
robot.execute("100 move -90 turn soap set start 50 move stop")