from statemachine import StateMachine

"""Curses is a library for displaying more complex"""
"""UIs in terminals. read more at:"""
"""http://docs.python.org/2/howto/curses.html"""
import curses
import signal
import sys

class ComboLock(object):

    """This function is the constructor of the class. It is called when you create
    an instance of this class like at the bottom of the file: combo = ComboLock().
    The self variable is the new instance of the class. If you do not understand
    classes and instances, make sure you read up on it and understand this code 
    before you continue."""
    def __init__(self):
        #Create the State Machine instance
        self._sm = StateMachine()

        #The following two lines simply create the attributes for the instance
        #and assign them blank values so you can read them later and not get
        #an error even if you havn't set a real value to them. This is good 
        #practice for understanding how your class is structured, and avoiding
        #errors when returning None means more. None is a special value for 
        #variables that marks a variable as empty.
        self.stdscr = None
        self.win = None

    def init_curses(self):
        #This makes it so if you hit CTRL+C curses doesn't eat the terminal alive!
        signal.signal(signal.SIGINT, self.signal_handler)

        #Setup curses
        #This next line lets us store stdscr on the object for use later
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self.win = curses.newwin(20, 40, 2, 2)
        

    """If you do not clean up curses before the program ends
    The terminal will act super weird and be hard to use.
    NEW COMMENT: This function doesn't really benefit from 
    from being put in a class, but it helps with consistency."""
    def cleanup_curses(self):
        curses.nocbreak();
        curses.echo()
        curses.endwin()

    """function handler for when you press CTRL+C"""
    def signal_handler(self, signal, frame):
        #Make sure we clean up curses if the user hits CTRL+C 
        self.cleanup_curses()
        sys.exit(0)

    def _display_UI(self):
        """We can just erase and redraw this entire window because why not?
        It also means we don't write over parts of our previous results
        which is why in the last version draw commands had extra spaces.
        With all normal drawings happening here, we can be sure we don't 
        forget to draw something when a certain code path runs."""
        self.win.erase()
        self.win.border()

        if self._sm.state == StateMachine.CODEOK:
            self.win.addstr(1, 7, "SUCCESS")
        
        elif self._sm.state == StateMachine.CODEBAD:
            self.win.addstr(1, 7, "NO!")

        else:
            self.win.addstr(1, 7, "CODE:")

        self.win.addstr(2, 7, '* '*len(self._sm.cur_code))
        self.win.addstr(11, 7, "Curr PIN: "+" ".join(self._sm.cur_code))
        self.win.addstr(13, 7, "Correct PIN: "+" ".join(self._sm.correct_code))

        #You can access the STATE_NAMES variable from the class because it 
        #is not tied to instances. Look up static variables if it doesn't 
        #make sense.
        self.win.addstr(16, 7, "NEW STATE: %s"%StateMachine.STATE_NAMES[self._sm.state])

        self.win.addstr(18, 7, "Press q or CTRL-c to quit.")

        self.win.refresh()
    
    def run(self):
        self.init_curses()
        #This next line initializes the display so you see something 
        #before pressing the first code. The proceeding calls to this
        #function happen in the while loop after each read.
        self._display_UI()

        #This while loop keeps checking the input you type on the keyboard
        while True:
            #Get a single keypress and turn it into a string
            c = chr(self.win.getch())
        
            #if you press q, terminate the program.
            if c == 'q': 
                break
        
            #This function call is built into python and returns true if the string
            #contains letters and/or numbers.
            if c.isalnum():
                old_code = self._sm.cur_code
                old_state = self._sm.state

                self._sm.do_event(StateMachine.E_KEYPRESS, c)
                self._display_UI()

                #These two lines print off the old state of the state machine.
                #The old_code and old_state variables store the needed state
                #before the do_event function is called which causes that state
                #to change. This is only debug data so I am not making it super 
                #fancy. Note that if you wanted to add printing this code to the 
                #display_UI function, you would have to pass it to the function 
                #in one of several ways: 
                # 1) Pass it to the function like 
                #      self._display_UI(old_code, old_state)
                # 2) Store it as a variable in self.
                #      self.old_code = self._sm.cur_code
                #    and then read it in the display function from self.
                # 3) Make the state machine store the old state so when there would 
                #    be a state variable and old_state variable, etc.
                #      self.__sm.old_state
                #
                #It is important to think about haw data can be passed around, stored
                #and accessed. If you don't, then there will be lots of frustration
                #about not being able to get your data and you may never want to use
                #classes for anything.
                #
                #If this access management seems pointlessly complex, notice that 
                #without this comment or the following debug code, this whole function
                #is very simple and easy to follow with no unrelated code mixed together.
                self.win.addstr(10, 7, "Prev PIN: "+" ".join(old_code))
                self.win.addstr(15, 7, "OLD STATE: %s"%StateMachine.STATE_NAMES[old_state])
        
                #Curses only draws changes to the screen when you ask nicely.
                #We have to call this to draw everything since the _display_UI call
                self.win.refresh()
        
        self.cleanup_curses()

"""This is simply calling the main function if you run this file directly. """
"""If you import the file, main will not auto run. This way you can make"""
"""libraries other people can use, but are programs that can run by """
"""themselves too!"""
if __name__ == '__main__':
    combo = ComboLock()
    combo.run()
