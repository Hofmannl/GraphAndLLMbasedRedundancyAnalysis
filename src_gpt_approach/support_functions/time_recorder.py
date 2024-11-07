class TimeRecorder:
    def __init__(self):
        self._nanoseconds = 0

    @property
    def nanoseconds(self):
        return self._nanoseconds

    @nanoseconds.setter
    def nanoseconds(self, value):
        if value is None:
            self._nanoseconds = 0
        else:
            self._nanoseconds = value

    @property
    def milliseconds(self):
        return self._nanoseconds / 1_000_000

    @property
    def seconds(self):
        return self._nanoseconds / 1_000_000_000

    @property
    def minutes(self):
        return self.seconds / 60
