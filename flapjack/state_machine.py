class FiniteStateMachine:
    """A simple Finite State Machine implementation in Python."""
    def __init__(self, states={}, initial_state=""):
        self._states = states
        self._current_state = initial_state

    def add_state(self, state, actions):
        """Add  a state to the machine.

        :param state: The name of the state to be added.
        :type state: str
        :param actions: The map of actions that can be taken and corresponding states.
        :type actions: dict
        :return: This object so that function calls can be chained.
        """
        self._states[state] = actions
        return self

    def get_current_state(self):
        """Get the current state of the machine.

        :return: The current state of the machine.
        """
        return self._current_state

    def get_actions_for(self, state):
        """Get the map of actions for a given state

        :param state: The state that you want the actions map for.
        :type state: str
        :return: The actions you can take at the given state. None if the state doesn't exist.
        :rtype: dict
        """
        if state in self._states.keys():
            return self._states[state]
        return None

    def do_action(self, action):
        """Performs an given action at the current state, changing state accordingly.
        If the action does nothing, then the current state is simply not changed.

        :param action: The action to perform.
        :type action: str
        :return: This object so that function calls can be chained.
        """
        if action in self._states[self._current_state].keys():
            self._current_state = self._states[self._current_state][action]
        return self

    @staticmethod
    def load_from_file(path):
        """Creates a FiniteStateMachine instance from a correctly formatted .json file and returns it.

        :param path: The path to the .json file to be loaded.
        :type path: str
        :return: FiniteStateMachine
        """
        from flapjack.asset_manager import AssetManager
        states = AssetManager.load_json(path)
        return FiniteStateMachine(states=states)

    def __iter__(self):
        for state, actions in self._states.items():
            yield state, actions
