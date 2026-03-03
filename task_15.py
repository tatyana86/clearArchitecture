from functools import wraps
from collections import namedtuple
import math
from enum import Enum

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1  
SOAP = 2   
BRUSH = 3  

class MoveResponse(Enum):
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"

class SetStateResponse(Enum):
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"

class StateMonad:
    def __init__(self, state, log=None, response=None):
        self.state = state
        self.log = log or []
        self.response = response
    
    def bind(self, func):
        new_state, new_log, new_response = func(self.state, self.log, self.response)
        return StateMonad(new_state, new_log, new_response)

def move(dist):
    def inner(old_state, log, response):
        angle_rads = old_state.angle * (math.pi/180.0)
        new_x = old_state.x + dist * math.cos(angle_rads)
        new_y = old_state.y + dist * math.sin(angle_rads)
        
        final_x, final_y, move_response = check_position(new_x, new_y)
        
        new_state = RobotState(
            final_x,
            final_y,
            old_state.angle,
            old_state.state
        )
        
        log_entry = f'POS({int(final_x)},{int(final_y)})'
        if move_response == MoveResponse.BARRIER:
            log_entry += " (HIT BARRIER!)"
        
        return new_state, log + [log_entry], move_response
    return inner

def turn(angle):
    def inner(old_state, log, response):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle + angle,
            old_state.state
        )
        return new_state, log + [f'ANGLE {new_state.angle}'], response
    return inner

def set_state(new_mode):
    def inner(old_state, log, response):
        resource_response = check_resources(new_mode)
        
        if resource_response == SetStateResponse.OK:
            new_state = RobotState(
                old_state.x,
                old_state.y,
                old_state.angle,
                new_mode
            )
            log_entry = f'STATE {new_mode}'
        else:
            new_state = old_state
            log_entry = f'STATE FAILED: {resource_response.value}'
        
        return new_state, log + [log_entry], resource_response
    return inner

def start(old_state, log, response):
    if old_state.state == WATER and water_amount <= 0:
        return old_state, log + ['START FAILED: NO WATER'], SetStateResponse.NO_WATER
    elif old_state.state == SOAP and soap_amount <= 0:
        return old_state, log + ['START FAILED: NO SOAP'], SetStateResponse.NO_SOAP
    return old_state, log + ['START'], response

def stop(old_state, log, response):
    return old_state, log + ['STOP'], response

def check_position(x: float, y: float) -> tuple[float, float, MoveResponse]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))
    
    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)

def check_resources(new_mode: int) -> SetStateResponse:
    global water_amount, soap_amount
    
    if new_mode == WATER:
        if water_amount > 0:
            water_amount -= 1
            return SetStateResponse.OK
        return SetStateResponse.NO_WATER
    elif new_mode == SOAP:
        if soap_amount > 0:
            soap_amount -= 1
            return SetStateResponse.OK
        return SetStateResponse.NO_SOAP
    return SetStateResponse.OK