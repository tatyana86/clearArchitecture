import math
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3

def transfer_to_cleaner(message):
    print(message)

class Command:
    def execute(self, transfer, state):
        pass

class MoveCommand(Command):
    def __init__(self, dist):
        self.dist = dist
    
    def execute(self, transfer, state):
        angle_rads = state.angle * (math.pi/180.0)
        new_state = RobotState(
            state.x + self.dist * math.cos(angle_rads),
            state.y + self.dist * math.sin(angle_rads),
            state.angle,
            state.state)
        transfer(('POS(', new_state.x, ',', new_state.y, ')'))
        return new_state

class TurnCommand(Command):
    def __init__(self, turn_angle):
        self.turn_angle = turn_angle
    
    def execute(self, transfer, state):
        new_state = RobotState(
            state.x,
            state.y,
            state.angle + self.turn_angle,
            state.state)
        transfer(('ANGLE', state.angle))
        return new_state

class SetStateCommand(Command):
    def __init__(self, new_internal_state):
        self.new_internal_state = new_internal_state
    
    def execute(self, transfer, state):
        if self.new_internal_state == 'water':
            self_state = WATER
        elif self.new_internal_state == 'soap':
            self_state = SOAP
        elif self.new_internal_state == 'brush':
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

class StartCommand(Command):
    def execute(self, transfer, state):
        transfer(('START WITH', state.state))
        return state

class StopCommand(Command):
    def execute(self, transfer, state):
        transfer(('STOP',))
        return state

def make(transfer, code, state):
    commands = []
    for command in code:
        cmd = command.split(' ')
        if cmd[0] == 'move':
            commands.append(MoveCommand(int(cmd[1])))
        elif cmd[0] == 'turn':
            commands.append(TurnCommand(int(cmd[1])))
        elif cmd[0] == 'set':
            commands.append(SetStateCommand(cmd[1]))
        elif cmd[0] == 'start':
            commands.append(StartCommand())
        elif cmd[0] == 'stop':
            commands.append(StopCommand())
    
    for command in commands:
        state = command.execute(transfer, state)
    return state