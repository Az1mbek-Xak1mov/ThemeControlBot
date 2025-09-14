from aiogram.fsm.state import State, StatesGroup

class StepByStepStates(StatesGroup):
    private_chat = State()
    main = State()
    lang = State()

class NewThemeStates(StatesGroup):
    waiting_for_text = State()
    ongoing = State()