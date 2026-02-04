# 1 - интерфейс
class ICleaner():
    
    def move(self, distance: int) -> None:
        pass
    
    def turn(self, angle: int) -> None:
        pass
    
    def set_state(self, state_name: str) -> None:
        pass
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass
    
    def get_x(self) -> float:
        pass
    
    def get_y(self) -> float:
        pass
    
    def get_angle(self) -> float:
        pass
    
    def get_state(self) -> int:
        pass

# 2 - реализация
class CleanerImplementation(ICleaner):
    
    def __init__(self):
        self._state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
    
    def _transfer_to_cleaner(self, message):
        print(message)
    
    def move(self, distance: int) -> None:
        self._state = pure_robot.move(
            self._transfer_to_cleaner,
            distance,
            self._state
        )
    
    def turn(self, angle: int) -> None:
        self._state = pure_robot.turn(
            self._transfer_to_cleaner,
            angle,
            self._state
        )
    
    def set_state(self, state_name: str) -> None:
        self._state = pure_robot.set_state(
            self._transfer_to_cleaner,
            state_name,
            self._state
        )
    
    def start(self) -> None:
        self._state = pure_robot.start(
            self._transfer_to_cleaner,
            self._state
        )
    
    def stop(self) -> None:
        self._state = pure_robot.stop(
            self._transfer_to_cleaner,
            self._state
        )
    
    def get_x(self) -> float:
        return self._state.x
    
    def get_y(self) -> float:
        return self._state.y
    
    def get_angle(self) -> float:
        return self._state.angle
    
    def get_state(self) -> int:
        return self._state.state

# 3 - сервис с DI:
class CleanerService:
   
    def __init__(self, cleaner: ICleaner):
        self._cleaner = cleaner
    
    def execute_commands(self, commands):
        for command in commands:
            cmd = command.split(' ')
            if cmd[0] == 'move':
                self._cleaner.move(int(cmd[1]))
            elif cmd[0] == 'turn':
                self._cleaner.turn(int(cmd[1]))
            elif cmd[0] == 'set':
                self._cleaner.set_state(cmd[1])
            elif cmd[0] == 'start':
                self._cleaner.start()
            elif cmd[0] == 'stop':
                self._cleaner.stop()
    
# 4 - использование:
cleaner_impl = CleanerImplementation()
service = CleanerService(cleaner_impl)

commands = (
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
)

service.execute_commands(commands)