import math
from collections import namedtuple, defaultdict
import uuid
import time

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3

class Event:
    def __init__(self, event_id=None, command_id=None):
        self.event_id = event_id or str(uuid.uuid4())
        self.command_id = command_id
        self.timestamp = time.time()

class MoveRequestedEvent(Event):
    def __init__(self, distance, **kwargs):
        super().__init__(**kwargs)
        self.distance = distance

class TurnRequestedEvent(Event):
    def __init__(self, angle, **kwargs):
        super().__init__(**kwargs)
        self.angle = angle

class SetStateRequestedEvent(Event):
    def __init__(self, mode, **kwargs):
        super().__init__(**kwargs)
        self.mode = mode

class StartRequestedEvent(Event):
    pass

class StopRequestedEvent(Event):
    pass

class RobotMovedEvent(Event):
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y

class RobotTurnedEvent(Event):
    def __init__(self, angle, **kwargs):
        super().__init__(**kwargs)
        self.angle = angle

class RobotStateChangedEvent(Event):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state

class RobotStartedEvent(Event):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state

class RobotStoppedEvent(Event):
    pass

class EventStore:
    def __init__(self):
        self.events = []
        self.subscribers = defaultdict(list)
    
    def append(self, event):
        self.events.append(event)
        self._notify_subscribers(event)
        return event
    
    def subscribe(self, event_type, callback):
        self.subscribers[event_type].append(callback)
    
    def _notify_subscribers(self, event):
        event_type = type(event)
        for callback in self.subscribers[event_type]:
            callback(event)
    
    def get_events(self):
        return self.events.copy()

class CommandHandler:
    def __init__(self, event_store):
        self.event_store = event_store
    
    def handle(self, command_str):
        parts = command_str.strip().split()
        if not parts:
            return None
        
        cmd = parts[0].lower()
        command_id = str(uuid.uuid4())
        
        if cmd == 'move' and len(parts) > 1:
            try:
                distance = float(parts[1])
                return self.event_store.append(
                    MoveRequestedEvent(distance, command_id=command_id)
                )
            except ValueError:
                return None
        
        elif cmd == 'turn' and len(parts) > 1:
            try:
                angle = float(parts[1])
                return self.event_store.append(
                    TurnRequestedEvent(angle, command_id=command_id)
                )
            except ValueError:
                return None
        
        elif cmd == 'set' and len(parts) > 1:
            mode = parts[1].lower()
            if mode in ['water', 'soap', 'brush']:
                return self.event_store.append(
                    SetStateRequestedEvent(mode, command_id=command_id)
                )
        
        elif cmd == 'start':
            return self.event_store.append(
                StartRequestedEvent(command_id=command_id)
            )
        
        elif cmd == 'stop':
            return self.event_store.append(
                StopRequestedEvent(command_id=command_id)
            )
        
        return None

class RobotStateProjector:
    def __init__(self):
        self.state = RobotState(0.0, 0.0, 0, WATER)
    
    def apply(self, event):
        if isinstance(event, RobotMovedEvent):
            self.state = RobotState(
                event.x,
                event.y,
                self.state.angle,
                self.state.state
            )
        elif isinstance(event, RobotTurnedEvent):
            self.state = RobotState(
                self.state.x,
                self.state.y,
                event.angle,
                self.state.state
            )
        elif isinstance(event, RobotStateChangedEvent):
            self.state = RobotState(
                self.state.x,
                self.state.y,
                self.state.angle,
                event.state
            )
        return self.state


class RobotEventProcessor:
    def __init__(self, event_store, projector):
        self.event_store = event_store
        self.projector = projector
        
        self.event_store.subscribe(MoveRequestedEvent, self.handle_move)
        self.event_store.subscribe(TurnRequestedEvent, self.handle_turn)
        self.event_store.subscribe(SetStateRequestedEvent, self.handle_set_state)
        self.event_store.subscribe(StartRequestedEvent, self.handle_start)
        self.event_store.subscribe(StopRequestedEvent, self.handle_stop)
    
    def handle_move(self, event):
        state = self.projector.state
        
        angle_rads = state.angle * (math.pi / 180.0)
        new_x = state.x + event.distance * math.cos(angle_rads)
        new_y = state.y + event.distance * math.sin(angle_rads)
        
        self.event_store.append(
            RobotMovedEvent(new_x, new_y, command_id=event.command_id)
        )
        
        transfer_to_cleaner(('POS(', new_x, ',', new_y, ')'))
    
    def handle_turn(self, event):
        state = self.projector.state
        new_angle = state.angle + event.angle
        
        self.event_store.append(
            RobotTurnedEvent(new_angle, command_id=event.command_id)
        )
        
        transfer_to_cleaner(('ANGLE', state.angle))
    
    def handle_set_state(self, event):
        if event.mode == 'water':
            new_state = WATER
        elif event.mode == 'soap':
            new_state = SOAP
        elif event.mode == 'brush':
            new_state = BRUSH
        
        self.event_store.append(
            RobotStateChangedEvent(new_state, command_id=event.command_id)
        )
        
        transfer_to_cleaner(('STATE', new_state))
    
    def handle_start(self, event):
        state = self.projector.state
        
        self.event_store.append(
            RobotStartedEvent(state.state, command_id=event.command_id)
        )
        
        transfer_to_cleaner(('START WITH', state.state))
    
    def handle_stop(self, event):
        self.event_store.append(
            RobotStoppedEvent(command_id=event.command_id)
        )
        
        transfer_to_cleaner(('STOP',))

def transfer_to_cleaner(message):
    print(message)

def main():
    event_store = EventStore()
    projector = RobotStateProjector()
    processor = RobotEventProcessor(event_store, projector)
    handler = CommandHandler(event_store)
    
    commands = [
        'move 100',
        'turn -90',
        'set soap',
        'start',
        'move 50',
        'stop'
    ]

    for cmd in commands:
        handler.handle(cmd)
        projector.apply(event_store.events[-1])
    
if __name__ == "__main__":
    main()