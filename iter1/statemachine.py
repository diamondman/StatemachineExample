
class StateMachine(object):
    STATE_NAMES = [
        'IDLE',
        'ONEDIGIT',
        'TWODIGIT',
        'THREEDIGIT',
        'CODEOK',
        'CODEBAD',
        ]

    IDLE = 0
    ONEDIGIT = 1
    TWODIGIT = 2
    THREEDIGIT = 3
    CODEOK = 4
    CODEBAD = 5

    E_TIMEOUT = 0
    E_KEYPRESS = 1

    def __init__(self):
        self.state = self.IDLE
        self.cur_code = []
        self.correct_code = ['1', '2', '3', '4']

    def do_event(self, event_type, event_param):
        if self.state == self.IDLE:
            if event_type == self.E_KEYPRESS:
                self.cur_code.append(event_param)
                self.state = self.ONEDIGIT

        elif self.state == self.ONEDIGIT:
            if event_type == self.E_KEYPRESS:
                self.cur_code.append(event_param)
                self.state = self.TWODIGIT
            elif event_type == self.E_TIMEOUT:
                self.cur_code = []
                self.state = self.IDLE
            
        elif self.state == self.TWODIGIT:
            if event_type == self.E_KEYPRESS:
                self.cur_code.append(event_param)
                self.state = self.THREEDIGIT
            elif event_type == self.E_TIMEOUT:
                self.cur_code = []
                self.state = self.IDLE
            
        elif self.state == self.THREEDIGIT:
            if event_type == self.E_KEYPRESS:
                self.cur_code.append(event_param)
                if self.cur_code == self.correct_code:
                    self.state = self.CODEOK
                    #print "CODE GOOD!"
                else:
                    self.state = self.CODEBAD
                    #print "WRONG CODE"
            elif event_type == self.E_TIMEOUT:
                self.cur_code = []
                self.state = self.IDLE

        elif self.state == self.CODEOK:
            if event_type == self.E_KEYPRESS:
                self.state = self.IDLE
                self.cur_code = []
        elif self.state == self.CODEBAD:
            if event_type == self.E_KEYPRESS:
                self.state = self.IDLE
                self.cur_code = []



#This is simply prints an error if you run this file directly.
#If you import the file, this code will not run.
if __name__ == '__main__':
    print("This file is just a library. To get the example running "
          "run \n    python combolock.py\n"
          "from this directory.")
