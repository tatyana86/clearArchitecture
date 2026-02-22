from collections import namedtuple
import pure_robot

# хранилище событий
event_store = {}

def rebuild_state(robot_id):
    state = pure_robot.RobotState(0, 0, 0, 1)
    if robot_id in event_store:
        for event in event_store[robot_id]:
            if event[0] == 'move':
                state = pure_robot.move(lambda x: None, event[1], state)
            elif event[0] == 'turn':
                state = pure_robot.turn(lambda x: None, event[1], state)
            elif event[0] == 'set':
                state = pure_robot.set_state(lambda x: None, event[1], state)
            elif event[0] == 'start':
                state = pure_robot.start(lambda x: None, state)
            elif event[0] == 'stop':
                state = pure_robot.stop(lambda x: None, state)
    return state

def handle_command(robot_id, command):
    current_state = rebuild_state(robot_id)
    
    cmd = command.split(' ')
    new_state = current_state
    
    if cmd[0] == 'move':
        new_state = pure_robot.move(print, int(cmd[1]), current_state)
    elif cmd[0] == 'turn':
        new_state = pure_robot.turn(print, int(cmd[1]), current_state)
    elif cmd[0] == 'set':
        new_state = pure_robot.set_state(print, cmd[1], current_state)
    elif cmd[0] == 'start':
        new_state = pure_robot.start(print, current_state)
    elif cmd[0] == 'stop':
        new_state = pure_robot.stop(print, current_state)
    
    if robot_id not in event_store:
        event_store[robot_id] = []
    event_store[robot_id].append((cmd[0], cmd[1] if len(cmd) > 1 else None))
    
    return new_state

if __name__ == "__main__":
    robot_id = "robot"
    
    handle_command(robot_id, "move 10")
    handle_command(robot_id, "turn 90")
    handle_command(robot_id, "move 5")
    handle_command(robot_id, "set water")
    handle_command(robot_id, "start")