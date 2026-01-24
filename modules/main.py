from cleaningRobot import CleaningRobot
from command_handler import process_command

def transfer_to_cleaner(message):
    print(message)

def main():
    robot = CleaningRobot(transfer_to_cleaner)
    
    print("Доступные команды:")
    print("move <расстояние> - движение вперед (в метрах)")
    print("turn <угол>       - поворот (в градусах)")
    print("set <device>      - выбор устройства (water/soap/brush)")
    print("start             - включить устройство очистки")
    print("stop              - выключить устройство очистки")
    print("Введите команды (пустая строка для выхода):")
    
    while True:
        try:
            command = input()

            if not command:
                continue
            
            process_command(robot, command)
                
if __name__ == "__main__":
    main()