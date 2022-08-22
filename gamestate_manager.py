states = {}
current_state = None
current_state_active = False


def add_state(key, state):
    global states

    if key in states:
        raise KeyError(f"State '{key}' already added to GameStateManager")
    states[key] = state


def set_state(key):
    global states
    global current_state
    global current_state_active

    current_state = states[key]
    current_state_active = False


def get_state():
    global current_state

    return current_state


def set_current_state_active(state):
    global current_state_active

    current_state_active = state


def current_state_is_active():
    global current_state_active

    return current_state_active
