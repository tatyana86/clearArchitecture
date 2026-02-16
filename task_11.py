import math
from collections import namedtuple
import pure_robot

RobotState = namedtuple("RobotState", "x y angle state")
WATER = 1
SOAP = 2
BRUSH = 3


class StateMonad:
    def __init__(self, func):
        self.func = func
    
    def bind(self, f):
        def wrapper(state):
            result, new_state = self.func(state)
            return f(result).func(new_state)
        return StateMonad(wrapper)

def unit(value):
    return StateMonad(lambda s: (value, s))

def lift_action(action_func, *args):
    def wrapped(state):
        new_state = action_func(pure_robot.transfer_to_cleaner, *args, state)
        return (None, new_state)
    return StateMonad(wrapped)

def move(dist):
    return lift_action(pure_robot.move, dist)

def turn(angle):
    return lift_action(pure_robot.turn, angle)

def set_state(mode):
    return lift_action(pure_robot.set_state, mode)

def start():
    return lift_action(pure_robot.start)

def stop():
    return lift_action(pure_robot.stop)

def run(monad, initial_state):
    result, final_state = monad.func(initial_state)
    return final_state

def main():
    initial_state = RobotState(0.0, 0.0, 0, WATER)
    
    program = (unit(None) >>
               (lambda _: move(100)) >>
               (lambda _: turn(-90)) >>
               (lambda _: set_state("soap")) >>
               (lambda _: start()) >>
               (lambda _: move(50)) >>
               (lambda _: stop()))
    
    final_state = run(program, initial_state)