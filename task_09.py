# api
import pure_robot

class RobotApi:
    def __init__(self):
        self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        self.command_handler = None
    
    def setup(self, command_handler_func):
        self.command_handler = command_handler_func
    
    def make(self, command, transfer_func):
        cmd = command.split(' ')
        cmd_type = cmd[0]
        
        self.cleaner_state = self.command_handler(transfer_func, cmd_type, cmd[1], self.cleaner_state)
        return self.cleaner_state
    
    def __call__(self, command, transfer_func):
        return self.make(command, transfer_func)


# функция-обработчик
def universal_robot_handler(transfer, cmd_type, arg, state):
    if cmd_type == 'move':
        return pure_robot.move(transfer, float(arg), state)
    elif cmd_type == 'turn':
        return pure_robot.turn(transfer, float(arg), state)
    elif cmd_type == 'set':
        return pure_robot.set_state(transfer, arg, state)
    elif cmd_type == 'start':
        return pure_robot.start(transfer, state)
    elif cmd_type == 'stop':
        return pure_robot.stop(transfer, state)
    else:
        return state


# использование

api = RobotApi()
api.setup(universal_robot_handler)