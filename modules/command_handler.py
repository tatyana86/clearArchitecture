def process_command(robot, command_line: str):
    parts = command_line.strip().lower().split()
    
    if not parts:
        return
    
    cmd = parts[0]
    
    if cmd == 'move':
        if len(parts) < 2:
            robot.transfer("Ошибка: неполная команда")
            return
        try:
            distance = float(parts[1])
            robot.move(distance)
        except ValueError:
            robot.transfer("Ошибка: неверный формат параметра")
    
    elif cmd == 'turn':
        if len(parts) < 2:
            robot.transfer("Ошибка: неполная команда")
            return
        try:
            angle_change = float(parts[1])
            robot.turn(angle_change)
        except ValueError:
            robot.transfer("Ошибка: неверный формат параметра")
    
    elif cmd == 'set':
        if len(parts) < 2:
            robot.transfer("Ошибка: неполная команда")
            return
        robot.set_device(parts[1])
    
    elif cmd == 'start':
        robot.start()
    
    elif cmd == 'stop':
        robot.stop()
    
    else:
        robot.transfer(f"Неизвестная команда '{cmd}'")