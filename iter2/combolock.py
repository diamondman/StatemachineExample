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

    """function handler for when you press CTRL+C"""
    def signal_handler(self, signal, frame):
        #Make sure we clean up curses if the user hits CTRL+C 
        self.cleanup_curses()
        sys.exit(0)

    """All the following functions were in iter1, but now that they are more 
    sanely organized, I will provide a brief description of what they do. in 
    the following function definition."""
    def init_curses(self):
        #This makes it so if you hit CTRL+C curses doesn't eat the terminal alive!
        signal.signal(signal.SIGINT, self.signal_handler)

        #Setup curses
        #This next line lets us store stdscr on the object for use later.
        #It turns out that we don't really use this variable, but the docs
        #say we do need to create it, so storing it just in case.
        #
        #This following 4 lines sets up our curses environment.
        #http://docs.python.org/2/howto/curses.html#starting-and-ending-a-curses-application
        #describes how to do this,
        #
        #This function, initscr, is documented here:
        #http://docs.python.org/2/library/curses.html#curses.initscr
        #Notice it returns a 'window' represengint everything in the terminal.
        #We create a window later that we use, so we don't use this window for much.
        self.stdscr = curses.initscr()
        #The following functions can be found on the same page as the docs for initscr
        #http://docs.python.org/2/library/curses.html#functions
        #noecho makes it so pressing a key doesn't cause it to immediate appear
        #on the screen. This is useful because we will be drawing *s instead.
        #The earlier link about curses how to describes practically what these
        #lines do. the function listing describes them in more technical detail.
        curses.noecho()
        curses.cbreak()
        #This disables the cursor from blinking.
        curses.curs_set(0)
 
        #Curses makes it easier to make a console program consisting of non-
        #overlapping 'windows' which are just rectangular regions in the
        #terminal. This function tells curses to create a new window region.
        #It returns an object representing that window. 
        #http://docs.python.org/2/library/curses.html#curses.newwin
        #
        #If you look at the docs, this function takes 4 things. 
        #    nlines, ncols, begin_y, begin_x
        #The docs describe what these variables mean. In this case they are the
        #size and position of the new window in characters.
        #The window object returned has functions for drawing text to the window.
        #We store this new window object to self so we can draw to it later.
        #
        #It is doable to return this window with the return keyword instead of 
        #setting it to a member variable of self. But since the window is long
        #term and relevant to the whole object, it makes more sense this way.
        self.win = curses.newwin(20, 40, 2, 2)
        

    """If you do not clean up curses before the program ends
    The terminal will act super weird and be hard to use.
    NEW COMMENT: This function doesn't really benefit from 
    from being put in a class because it doesn't use self, but
    its functionality belongs here so here it is."""
    def cleanup_curses(self):
        #Look at init_curses for links to documentation about these functions.
        #These calls just turn off curses.
        curses.nocbreak();
        curses.echo()
        curses.endwin()

    def _display_UI(self):
        #Window objects are how curses draws things to the screen. This page
        #documents the available functions:
        #http://docs.python.org/2/library/curses.html#window-objects
        #We set the curses window we want to use to self.win in the 
        #init_curses function. to use the methods on the window, we read it
        #in the same way: self.win.[whatever function]. Check the previous
        #link for what each function does.

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

        #win.addstr is the curses version of print. But, you get to say where
        #in the window to put the text.
        self.win.addstr(2, 7, '* '*len(self._sm.cur_code))
        self.win.addstr(11, 7, "Curr PIN: "+" ".join(self._sm.cur_code))
        self.win.addstr(13, 7, "Correct PIN: "+" ".join(self._sm.correct_code))

        #You can access the STATE_NAMES variable from the class because it 
        #is not tied to instances. Look up static variables if it doesn't 
        #make sense.
        self.win.addstr(16, 7, "NEW STATE: %s"%StateMachine.STATE_NAMES[self._sm.state])

        self.win.addstr(18, 7, "Press q or CTRL-c to quit.")

        #Curses doesn't draw to the screen as soon as you call addstr. 
        #It gets a list of changes together and puts them on the screen 
        #when you call refresh on the window. This allows your interface
        #to never look like it it being drawn because it puts it up once
        #you have everything ready in the background.
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
            #contains letters and/or numbers. If you want to allow other characters
            #like the home key, etc, you will need to edit or add to this if 
            #to accept that type of key too.
            if c.isalnum():
                old_state = self._sm.state

                self._sm.do_event(StateMachine.E_KEYPRESS, c)
                #It is a good idea to limit the number of places certain things 
                #happen. Idealy all drawing to the screen will be done in the 
                #display_ui function so looking only at that function we can see
                #everything that will be drawn. The following print of OLD STATE
                #is an example of when trying to do that can be hard.
                self._display_UI()

                #This following addstr prints off the old state of the state 
                #machine. The old_state variable stores the needed state before 
                #the do_event function is called which causes that state to 
                #change. This is only debug data so I am not making it super fancy. 
                #
                #Note that if you wanted to add printing this code to the
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
                self.win.addstr(15, 7, "OLD STATE: %s"%StateMachine.STATE_NAMES[old_state])
        
                #Curses only draws changes to the screen when you ask nicely.
                #We have to call this to draw everything since the _display_UI call
                self.win.refresh()
        
        self.cleanup_curses()


    """This function is the same as the run function above but without the weird
    printing. This code is not normally run in this program, but is here to show
    you how sinple this function truly is now that we pulled the functionality out 
    and split it out over the class. Looking at this function, you don't get 
    immediate access to how the whole thing works due to the code being split up, 
    but you do get a powerful overview and can look into the functions like 
    display_ui to see how it works. This design is much cleaner and clearer than 
    the last iteration."""
    def run_no_oldstate_messages(self):
        self.init_curses()
        #This next line initializes the display so you see something 
        #before pressing the first code. The proceeding calls to this
        #function happen in the while loop after each read.
        self._display_UI()

        #Keep getting user input until the user asks to quit.
        while True:
            #Get a single keypress and turn it into a string
            c = chr(self.win.getch())
        
            #if you press q, terminate the program.
            if c == 'q': 
                break
        
            #Check if the string contains letters and/or numbers. Ignore otherwise
            if c.isalnum():
                self._sm.do_event(StateMachine.E_KEYPRESS, c)
                self._display_UI()
    
        self.cleanup_curses()

"""This is simply calling the main function if you run this file directly. """
"""If you import the file, main will not auto run. This way you can make"""
"""libraries other people can use, but are programs that can run by """
"""themselves too!"""
if __name__ == '__main__':
    combo = ComboLock()
    combo.run()
    #combo.run_no_oldstate_messages()
