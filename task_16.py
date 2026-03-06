from abc import ABC, abstractmethod

class CommandNode(ABC):
    @abstractmethod
    def interpret(self, monad):
        pass

class Stop(CommandNode):
    def interpret(self, monad):
        new_state, new_log, response = stop(monad.state, monad.log, monad.response)
        return StateMonad(new_state, new_log, response)

class Move(CommandNode):
    def __init__(self, distance, next_func):
        self.distance = distance
        self.next = next_func

    def interpret(self, monad):
        new_state, new_log, response = move(self.distance)(
            monad.state, monad.log, monad.response
        )

        new_monad = StateMonad(new_state, new_log, response)

        next_node = self.next(response)

        if next_node:
            return next_node.interpret(new_monad)

        return new_monad

class Turn(CommandNode):
    def __init__(self, angle, next_func):
        self.angle = angle
        self.next = next_func

    def interpret(self, monad):
        new_state, new_log, response = turn(self.angle)(
            monad.state, monad.log, monad.response
        )

        new_monad = StateMonad(new_state, new_log, response)

        next_node = self.next(response)

        if next_node:
            return next_node.interpret(new_monad)

        return new_monad

class SetState(CommandNode):
    def __init__(self, new_state_mode, next_func):
        self.new_state_mode = new_state_mode
        self.next = next_func

    def interpret(self, monad):
        new_state, new_log, response = set_state(self.new_state_mode)(
            monad.state, monad.log, monad.response
        )

        new_monad = StateMonad(new_state, new_log, response)

        next_node = self.next(response)

        if next_node:
            return next_node.interpret(new_monad)

        return new_monad


program = Move(
    100,
    lambda r1: Turn(
        -90,
        lambda r2: SetState(
            SOAP,
            lambda r3: Move(
                50,
                lambda r4: Stop()
            )
        )
    )
)