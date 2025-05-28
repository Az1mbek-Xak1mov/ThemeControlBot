from aiogram.fsm.state import State, StatesGroup

class StepByStepStates(StatesGroup):
    start = State()
    main = State()