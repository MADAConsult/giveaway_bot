from aiogram.dispatcher.filters.state import StatesGroup, State

class ExecutedGivesStates(StatesGroup):
    select_executed_give = State()
    select_give = State()
    manage_selected_give = State()
    select_winner = State()
    winner_options = State()