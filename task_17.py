from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from typing import Tuple, Any, List
import math

class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3

@dataclass(frozen=True)
class RobotState:
    x: float
    y: float
    angle: float
    mode: int

@dataclass(frozen=True)
class MoveResponse:
    distance: float
    success: bool

@dataclass(frozen=True)
class TurnResponse:
    angle: float
    success: bool

@dataclass(frozen=True)
class StateResponse:
    mode: CleaningMode
    success: bool

class Command(ABC):
    @abstractmethod
    def execute(self, state: RobotState) -> Tuple[Any, RobotState]:
        pass

class Move(Command):
    def __init__(self, distance: float):
        self._distance = distance

    def execute(self, state: RobotState):
        angle_rads = state.angle * math.pi / 180
        new_state = RobotState(
            state.x + self._distance * math.cos(angle_rads),
            state.y + self._distance * math.sin(angle_rads),
            state.angle,
            state.mode
        )
        return MoveResponse(self._distance, True), new_state

class Turn(Command):
    def __init__(self, angle: float):
        self._angle = angle

    def execute(self, state: RobotState):
        new_state = RobotState(
            state.x,
            state.y,
            state.angle + self._angle,
            state.mode
        )
        return TurnResponse(self._angle, True), new_state

class SetState(Command):
    def __init__(self, mode: CleaningMode):
        self._mode = mode

    def execute(self, state: RobotState):
        new_state = RobotState(
            state.x,
            state.y,
            state.angle,
            self._mode.value
        )
        return StateResponse(self._mode, True), new_state

class Interpreter:
    def run(self, program: List[Command], state: RobotState):
        current_state = state
        for command in program:
            _, current_state = command.execute(current_state)
        return current_state

class RobotAPI:
    def move(self, distance):
        return Move(distance)

    def turn(self, angle):
        return Turn(angle)

    def set_mode(self, mode: CleaningMode):
        return SetState(mode)

if __name__ == "__main__":
    api = RobotAPI()
    program = [
        api.move(100),
        api.turn(-90),
        api.set_mode(CleaningMode.SOAP),
        api.move(50)
    ]

    initial_state = RobotState(0, 0, 0, CleaningMode.WATER.value)
    interpreter = Interpreter()
    final_state = interpreter.run(program, initial_state)
    print(final_state)