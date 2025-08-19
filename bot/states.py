from aiogram.fsm.state import State, StatesGroup

class StepByStepStates(StatesGroup):
    private_chat = State()
    main = State()