import time

class TimedUser:

    def __init__(self, user, timeout_mins = 60, note = ''):
        self.user = user
        now = time.time()
        self.timeout = now + (timeout_mins * 60)
        self.note = note

    def get_remaining_time(self):
        return int((self.timeout - time.time()) / 60)
