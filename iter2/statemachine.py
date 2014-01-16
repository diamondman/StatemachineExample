
class StateMachine(object):
    """This variable is only used for getting the string names of the 
    states based on their number. Each stats is just a number below, and
    this array lets us check 
    StateMachine.STATE_NAMES[StateMachine.IDLE]
    or
    StateMachine.STATE_NAMES[0]
    and the result would be the string 'IDLE'."""
    STATE_NAMES = [
        'IDLE',
        'ONEDIGIT',
        'TWODIGIT',
        'THREEDIGIT',
        'CODEOK',
        'CODEBAD',
        ]

    """All of the following variables are called static variables. Instances
    of the class don't get a unique copy of them. Changing them from any 
    instance causes the value to change for all instances at the same time.
    Another interesting thing about static variables is that since they do not
    rely on an individual instance, you can access them without an instance at
    all.

    For example, the following two sections of code do the same thing:
        print(StateMachine.ONEDIGIT)
    versus
        s = StateMachine()
        print(s.ONEDIGIT)

    Do not change these variables while the program is running."""
    IDLE = 0
    ONEDIGIT = 1
    TWODIGIT = 2
    THREEDIGIT = 3
    CODEOK = 4
    CODEBAD = 5

    E_TIMEOUT = 0
    E_KEYPRESS = 1
    
    """Initially set the IDLE state by calling the new transition function.
    Set the correct code to a constant 4 digit pin. Variables created through 
    accessing self like the following line defining correct_code are not 
    static."""
    def __init__(self):
        self._transition_IDLE()
        self.correct_code = ['1', '2', '3', '4']

    """do_event is now a bit simplier. Instead of having duplicate code in it 
    that should always be the same (changing to idle state, etc), now it just 
    calls a function that does the necessary things for that state transition. 
    do_event now only has the control logic for what state and event should 
    cause what transition. 
    The reason this is desirable is that we can now look at the functions in the
    class and infer what the overall, and individual behavior of the functions 
    and the class as a whole without reading the whole thing. This ability to 
    communicate how the class works without requiring an entire through read is 
    an important skill that makes maintaining the code and adding features much 
    easier."""
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

    """These functions now handle setting the new state and doing whatever is 
    necessary to transition to that new state. The code is admittedly a bit 
    longer, but it is much more structured making it easier to see the side 
    effects of the transitions without having to see around a bunch of ifs. 
    Also if you need to add, remove, or edit a transition, you only have to do 
    it in one place and can't accidently miss one of the places it needed to 
    happen."""
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
    #In python, strings next to each other with only spaces or newlines
    #between are automatically attached together into one string.
    #The \n in the strings mark newlines.
    print("This file is just a library. To get the example running "
          "run \n    python combolock.py\n"
          "from this directory.")
