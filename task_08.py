# api
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")
WATER = 1
SOAP = 2
BRUSH = 3

def make_robot(move_func, 
                turn_func, 
                set_state_func, 
                start_func, 
                stop_func, 
                transfer_func, 
                code, 
                state):

    for command in code:
        cmd = command.split(' ')
        
        if cmd[0] == 'move':
            state = move_func(float(cmd[1]), state, transfer_func)
        elif cmd[0] == 'turn':
            state = turn_func(float(cmd[1]), state, transfer_func)
        elif cmd[0] == 'set':
            state = set_state_func(cmd[1], state, transfer_func)
        elif cmd[0] == 'start':
            state = start_func(state, transfer_func)
        elif cmd[0] == 'stop':
            state = stop_func(state, transfer_func)
    
    return state

# реализация
def move(dist, state, transfer_func):
    angle_rads = state.angle * (math.pi / 180.0)
    new_x = state.x + dist * math.cos(angle_rads)
    new_y = state.y + dist * math.sin(angle_rads)
    
    new_state = RobotState(
        new_x,
        new_y,
        state.angle,
        state.state
    )
    
    transfer_func(f"POS({new_state.x:.1f},{new_state.y:.1f})")
    return new_state


def turn(turn_angle, state, transfer_func):
    new_angle = state.angle + turn_angle
    
    new_state = RobotState(
        state.x,
        state.y,
        new_angle,
        state.state
    )
    
    transfer_func(f"ANGLE {new_state.angle:.1f}")
    return new_state


def set_state(new_internal_state, state, transfer_func):
    if new_internal_state == 'water':
        new_mode = WATER
    elif new_internal_state == 'soap':
        new_mode = SOAP
    elif new_internal_state == 'brush':
        new_mode = BRUSH
    else:
        return state
    
    new_state = RobotState(
        state.x,
        state.y,
        state.angle,
        new_mode
    )
    
    transfer_func(f"STATE {new_state.state}")
    return new_state


def start(state, transfer_func):
    transfer_func(f"START WITH {state.state}")
    return state


def stop(state, transfer_func):
    transfer_func("STOP")
    return state

# главная программа
def transfer_to_cleaner(message):
    print(message)

def main():
    initial_state = RobotState(x=0.0, y=0.0, angle=0, state=WATER)
    
    # Команды
    commands = [
        'move 100',
        'turn -90',
        'set soap',
        'start',
        'move 50',
        'stop'
    ]
        
    final_state = make_robot(
        robot_functions.move,
        robot_functions.turn,
        robot_functions.set_state,
        robot_functions.start,
        robot_functions.stop,
        transfer_to_cleaner,
        commands,
        initial_state
    )