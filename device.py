class Device:
    def __init__(self, id: int):
        '''
        method to create a new device with its number, the dictionary of who it can talk to, and
        what messages have been cancelled
        '''
        self._id = id
        self._prop_dict = {}
        self._cancelled = set()

    def get_id(self) -> int:
        '''getter for the id of the device'''
        return self._id

    def get_prop_dict(self) -> dict:
        '''
        getter for the propogation dictionary of what devices it can talk to, with the key
        being a device it can talk to, and the value being how long it takes for the message
        to go through
        '''
        return self._prop_dict

    def add_prop(self, prop_id: int, prop_duration: int) -> None:
        '''adds a new relationship to the propogation dictionary'''
        self._prop_dict[prop_id] = prop_duration

    def get_cancelled(self) -> set[str]:
        '''returns the set of cancelled messages'''
        return self._cancelled

    def add_cancelled(self, message: str) -> None:
        '''adds a new cancelled message to the list of cancelled messages'''
        self._cancelled.add(message)
