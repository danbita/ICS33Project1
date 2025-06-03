class Command:
    def __init__(self, type: str, sender: int, receiver: int, message: str, time: int,
                 sending: bool):
        '''
        creates new command, complete with type, sender, receiver, the contents of the message,
        the time the command was sent, and whether the message is being sent or received.
        '''
        self._type = type
        self._sender = sender
        self._receiver = receiver
        self._message = message
        self._time = time
        self._sending = sending

    def get_type(self):
        '''getter for variable type'''
        return self._type

    def get_sender(self) -> int:
        '''getter for sender device'''
        return self._sender

    def get_receiver(self) -> int:
        '''getter for receiver device'''
        return self._receiver

    def get_message(self) -> str:
        '''getter for message content'''
        return self._message

    def time(self) -> int:
        '''getter for time'''
        return self._time

    def sending(self) -> bool:
        '''getter for sending vs receiving'''
        return self._sending

    def print(self) -> None:
        '''
        method for printing out the command, depending on what type it is and if its being
        send or received
        '''
        if self._sending:
            if self._type == 'ALERT':
                print('@' + str(self._time) + ': #' + str(self._sender), 'SENT ALERT TO #' + str(self._receiver) + ':',
                      self._message)
            elif self._type == 'CANCEL':
                print('@' + str(self._time) + ': #' + str(self._sender), 'SENT CANCELLATION TO #' + str(self._receiver) + ':',
                      self._message)
        else:
            if self._type == 'ALERT':
                print('@' + str(self._time) + ': #' + str(self._receiver), 'RECEIVED ALERT FROM #' + str(self._sender) + ':',
                      self._message)
            elif self._type == 'CANCEL':
                print('@' + str(self._time) + ': #' + str(self._receiver), 'RECEIVED CANCELLATION FROM #' + str(self._sender) + ':',
                      self._message)