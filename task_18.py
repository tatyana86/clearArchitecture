from typing import NamedTuple, Callable, Dict, Any
import math

class _State(NamedTuple):
    x: float
    y: float
    angle: float
    mode: int
    water: int
    soap: int
    blocked: bool

WATER = 1
SOAP = 2
BRUSH = 3

def robot(transfer: Callable[[Any], None]) -> Dict[str, Callable]:

    state = _State(0.0, 0.0, 0, WATER, 3, 3, False)

    def capabilities(s: _State):

        caps = {}

        if not s.blocked:

            def move(dist: int):
                angle_rads = s.angle * (math.pi / 180.0)
                new_x = s.x + dist * math.cos(angle_rads)
                new_y = s.y + dist * math.sin(angle_rads)

                blocked = not (0 <= new_x <= 100 and 0 <= new_y <= 100)

                nx = max(0, min(100, new_x))
                ny = max(0, min(100, new_y))
                transfer(('POS', nx, ny))
                return capabilities(_State(nx, ny, s.angle, s.mode, s.water, s.soap, blocked))

            caps["move"] = move

        def turn(angle: int):
            ns = _State(s.x, s.y, s.angle + angle, s.mode, s.water, s.soap, s.blocked)
            transfer(('ANGLE', ns.angle))
            return capabilities(ns)

        caps["turn"] = turn

        if s.water > 0:
            def set_water():
                transfer(('STATE', WATER))
                return capabilities(_State(s.x, s.y, s.angle, WATER, s.water-1, s.soap, s.blocked))
            caps["water"] = set_water

        if s.soap > 0:
            def set_soap():
                transfer(('STATE', SOAP))
                return capabilities(_State(s.x, s.y, s.angle, SOAP, s.water, s.soap-1, s.blocked))
            caps["soap"] = set_soap

        def brush():
            transfer(('STATE', BRUSH))
            return capabilities(_State(s.x, s.y, s.angle, BRUSH, s.water, s.soap, s.blocked))

        caps["brush"] = brush

        def start():
            transfer(('START', s.mode))
            return capabilities(s)

        def stop():
            transfer(('STOP',))
            return capabilities(s)

        caps["start"] = start
        caps["stop"] = stop

        return caps

    return capabilities(state)

def transfer_to_cleaner(msg):
    print(msg)


api = robot(transfer_to_cleaner)