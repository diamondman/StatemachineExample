
class StateMachine(object):
    STATE_NAMES = [
        'IDLE',
        'ONEDIGIT',
        'TWODIGIT',
        'THREEDIGIT',
        'FOURDIGIT',
        'CODEOK',
        'CODEBAD',
        ]

    IDLE = 0
    ONEDIGIT = 1
    TWODIGIT = 2
    THREEDIGIT = 3
    FOURDIGIT = 4
    CODEOK = 5
    CODEBAD = 6

    E_TIMEOUT = 0
    E_KEYPRESS = 1

    def __init__(self):
        self._transition_IDLE()
        self.correct_code = ['1', '2', '3', '4']

    def do_event(self, event_type, event_param):
        if self.state == self.IDLE:
            if event_type == self.E_KEYPRESS:
                self._transition_1DIGIT(event_param)

        elif self.state == self.ONEDIGIT:
            if event_type == self.E_KEYPRESS:
                self._transition_2DIGIT(event_param)
            elif event_type == self.E_TIMEOUT:
                self._transition_IDLE()
            
        elif self.state == self.TWODIGIT:
            if event_type == self.E_KEYPRESS:
                self._transition_3DIGIT(event_param)
            elif event_type == self.E_TIMEOUT:
                self._transition_IDLE()
            
        elif self.state == self.THREEDIGIT:
            if event_type == self.E_KEYPRESS:
                self._transition_GOODBAD(event_param)
            elif event_type == self.E_TIMEOUT:
                self._transition_IDLE()

        elif self.state == self.CODEOK:
            if event_type == self.E_KEYPRESS:
                self._transition_IDLE()

        elif self.state == self.CODEBAD:
            if event_type == self.E_KEYPRESS:
                self._transition_IDLE()


    def _transition_IDLE(self):
        self.state = self.IDLE
        self.cur_code = []

    def _transition_1DIGIT(self, keycode):
        self.cur_code.append(keycode)
        self.state = self.ONEDIGIT

    def _transition_2DIGIT(self, keycode):
        self.cur_code.append(keycode)
        self.state = self.TWODIGIT

    def _transition_3DIGIT(self, keycode):
        self.cur_code.append(keycode)
        self.state = self.THREEDIGIT

    def _transition_GOODBAD(self, keycode):
        self.cur_code.append(keycode)
        if self.cur_code == self.correct_code:
            self.state = self.CODEOK
        else:
            self.state = self.CODEBAD

#This is simply prints an error if you run this file directly.
#If you import the file, this code will not run.
if __name__ == '__main__':
    print("This file is just a library. To get the example running "
          "run \n    python combolock.py\n"
          "from this directory.")
