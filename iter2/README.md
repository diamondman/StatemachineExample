ITERATION 2 README
===================
-------------------

Last iteration we were able to build a fully functional program, that interacted with the user. Using State Machines and some planning, it wasn't all that difficult to get the basic functionality in the StateMachine classing running. On the plus side, the program works and there are no known bugs. Unfortunately the code quality isn't particularly high, which leads to a few parts being hard to follow, and hard to add to. Lets see where we can do better.

CRITICISMS (statemachine.py)
-------------------

This class is pretty straightforward, and has only one function beyond the constructor that does everything it ever needs to do. But that is the problem. Lets list off the responsibilities of the do_event function.
    Check the value of and run code based on the current state of the state machine
    Check the event and run the code for the current state for that event

This seems simple enough, but it doesn't end there.
    Handle transitioning ONEDIGIT->IDLE
    Handle transitioning TWODIGIT->IDLE
    Handle transitioning THREEDIGIT->IDLE
    Handle transitioning IDLE->ONEDIGIT
    etc for all state transitions

Still not too bad, all related enough. But we also have to add 
    Adding the character pressed to the current code when transitioning to ONEDIGIT
    Adding the character pressed to the current code when transitioning to TWODIGIT
    Adding the character pressed to the current code when transitioning to THREEDIGIT
    Adding the character pressed to the current code when transitioning to CODEOK/CODEBAD
    Clearing the current code during any transition to idle (3 different copies of same code)

It turns out that this one function has a lot of responsibilities when its job mostly consists of dispatching what to do when you send an event while the state machine is in a certain state. It seems that the do_event function doesn't really need to know how to do the transitions, it just needs to determine what state we should be moving to.


IMPROVEMENTS (statemachine.py)
-------------------

The biggest target that will simplify the do_event function heavily is to make a function called _transition_IDLE. The _ at the beginning of the function is a convention saying that the function is for internal use... no one outside of the class should call that because they may cause problems. do_event doesn't have this _ because we want code outside of this class to call that function.

We can define our new function in the StateMachine class as follows:
    def _transition_IDLE(self):
        self.state = self.IDLE
        self.cur_code = []

Now we can replace all the places that the following lines appear in do_event
    self.state = self.IDLE
    self.cur_code = []
with
    self._transition_IDLE()

We have just pulled duplicate code out and turned it into a more general function. SUCCESS!

Now, the do_event function is burdened with less responsibility and the if statements that make up its primary role are more prominent/less cluttered by unrelated code. We also got rid of duplicate code! Previously if we wanted to add some effect to moving to the IDLE state, we would have to add the code to every transition to IDLE, but now only edits to _transition_IDLE are necessary! 

The other transitions don't give us the same amount of return for our work, but pulling the, all out gives us consistency and further simplifies do_event until it is only if statements that choose what _transition function to call.

For the transition functions that need to add something to cur_code, we can give them a parameter we will use to pass along the key code to the function.

These are all the transition functions we should have after pulling the code out of do_event.
    _transition_IDLE(self):
    _transition_1DIGIT(self, keycode):
    _transition_2DIGIT(self, keycode):
    _transition_3DIGIT(self, keycode):
    _transition_GOODBAD(self, keycode):

Now that we extracted the code into their functions, we get a nice benefit that we can more easily see how the code as a whole works. No one has to go over every line of the file to get a grip on what it does. 'These are the transition functions, and here is the logic choosing which transition to do.'


CRITICISMS (combolock.py)
-------------------

Skimming this file, we find several functions floating around, and one giant function called main that does almost everything. As with the last file, lets try to enumerate the responsibilities of this offending function.

    Set up the curses library to draw on the screen
    Create the StateMachine instance
    Draw the UI on the screen through curses (addstr is the curses function that draws text, similar to print)
    Read user input
    Validate input
    Draw changes to the UI
    Clean up and disable curses before the program ands.

Even worse, following all the places where draws text to the screen, erases text, or add some more text somewhere on the screen makes it difficult to visualize what the screen will look like when running the code unless you run the whole function through your mind a few times. We can do much better than this.


IMPROVEMENTS (combolock.py)
-------------------

We are going to create a class. A class called ComboLock. The definition is pretty much the same as the class definition for the StateMachine class.

    class ComboLock(object):

We will create an __init__ method just like in StateMachine. For now it will only have the line 'pass' in it which tells python to do nothing. We will come back to this function later and make it do more interesting things.

    def __init__(self):
        pass

We can then move the main function into the class and rename it run. This name is somewhat arbitrary, but the name main implies it is a function not in a class, it is just convention. The run function will be what you call on the new ComboLock instance to get it to display the UI and do its normal thing. 

When you move main into the class, be sure to include the new self variable that all member functions of a class require.

    def main():

becomes 

    class ComboLock(object):
    	def __init__(self):
	    pass
    
        def run(self):
	    ....

But now that we have changed the main function's name and put it in a class, the code at the bottom of the file that called the main function will not work, and currently the program will not run. Lets fix that. Because run is now inside of a class and takes a self variable, it needs to be called on an instance of its class. So we have to change out the call to main() with a call of run on a new instance of ComboLock as follows:

    if __name__ == '__main__':
        combo = ComboLock()
        combo.run()

If we run the file after this edit, it will run like normal. If you are following along editing a copy of the old file, feel free to try and run it with these edits. You should notice absolutely zero difference in how it runs. 

Now that we have the basic class set up, it is time to start actually using the features and abilities classes give us. The current state of the code is just wrapping functional code in an object, but it isn't really taking advantage of its new home. Lets start by making the state machine object a member of the ComboLock class. 

In the original code near the top we can change

    s = StateMachine()

to

    self._sm = StateMachine()

With this, the instance of the StateMachine we were using as s is now assigned as a part of this instance of ComboLock and can be used anywhere in the class after it is defined. Unfortunately the code is broken again and we have to change every time we use the s variable with self._sm. If we get every one of them, the program should work like normal again. 

Not that _sm is being used as a member of the class, we can define it anywhere in the class that runs before run() and it will stick around. The ideal place for this is the __init__ method. replace the pass with self._sm = StateMachine() and run the program again. It still works because when the instance is created, self._sm is set. When run is called after that, it reads self._sm and finds the StateMachine instance the __init__ method of ComboLock put there for it.

With the state machine initialization out of the run method, we are starting to take advantage of the class approach. We can replace the win variable with 

    self.win = curses.newwin(20, 40, 2, 2)

and then replace every time we read win with self.win. As usual if you do it right and get all of them, the program will run like normal. If the program crashes and the terminal acts weird because curses wasn't turned off correctly, run this in the terminal (it may not look like it is typing but it is): 
    stty sane
That will reset the terminal so it doesn't act all crazy.

Since we turned win into an instance variable (on self) we can now move its definition somewhere else and unclutter run even more. Wherever we put it though, we need to make sure that the curses initialization functions get called before it runs or it won't work. The easiest way to do this is move those initialization lines along with the self.win definition. 

So, where to put it. We could put it in the __init__ method like we did _sm, but that would make it so that as soon as you make the class object, the terminal initializes curses. That seems like something to me that should happen when you call the run function, so lets not do that. Instead lets make a new method on the ComboLock class called init_curses where we will put all this initialization code to create the window and set the curses settings. 

    def init_curses(self):
        #This makes it so if you hit CTRL+C curses doesn't eat the terminal alive!
        signal.signal(signal.SIGINT, signal_handler)
	
	#Setup Curses
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.win = curses.newwin(20, 40, 2, 2)

But again, the program is temporarily broken. Just creating the method doesn't mean it is called, so we have to add a call to the function in the place we removed the code from run. add a 

    self.init_curses()

in run where we took the lines out and put them into init_curses, and we should be back in business.

Because we now have an init_curses method, it would make sense to move the cleanup_curses function into the class and change the calls to it from 

    cleanup_curses()

to

    self.cleanup_curses()

It may seem weird to bring cleanup_curses into the classs, particularly because we need to give it a self variable, and it doesn't even ever use it! But it helps a lot with consistency and we know everything in the class works together. It is not necessary nor a good idea to pull every function you une into a class, but you will figure out a balance that sits well with you.

Yet again the code is broken. The reason is the signal_handler function which checks for when you hit CTRL+C to quit the program and makes sure it cleans up curses before you do. This function needed to call cleanup_curses, but now it has to call it through self, but it doesn't HAVE a self. The function itself is only used by this class, so there is no reason not to bring it into the class. Move it in and change the reference to signal_handler to self.signal_handler and we should be running again. Don't forget to give signal_handler a self parameter.

There is one more thing to do with this class before it is nice and clean. But it is the most complicated. Lets look over the run method. We have removed a lot of its jobs from last time. Now the tasks are only: 

    Draw the UI on the screen through curses (addstr is the curses function that draws text, similar to print)
    Read user input
    Validate input
    Draw changes to the UI

We can get that simpler. If you read over the code in run, most of it are calls to self.win functions like addstr, border, refresh, or erase (all documented in the curses docs). These functions all have to do with drawing the UI, so lets make a display_ui function and put all this stuff in there.

Something I would like to point out before we move this code over is that all the lines we are about to move all use values stores in self, so we don't have to pass anything off to the display_ui function, at least not yet. Everything is stored in self so we can call those drawing methods anytime we want. Lets start by moving ALL of the curses calls (through self.win) into the new function, including the if statements that only have curses code inside of them.

We get the following:
    def display_UI(self):

        self.win.addstr(1, 7, "CODE:\n")
        self.win.addstr(18, 7, "Press q or CTRL-c to quit.")
        self.win.border()
        self.win.refresh()
        self.win.border()
        self.win.addstr(13, 7, "Correct PIN: "+" ".join(self._sm.correct_code))
        self.win.addstr(10, 7, "Prev PIN: "+" ".join(self._sm.cur_code))

        old_state = self._sm.state
        new_state = self._sm.state
        self.win.addstr(15, 7, "OLD STATE: %s        "%self._sm.STATE_NAMES[old_state])
        self.win.addstr(16, 7, "NEW STATE: %s        "%self._sm.STATE_NAMES[new_state])
        self.win.addstr(18, 7, "Press q or CTRL-c to quit.")
        
 
        if self._sm.state == StateMachine.IDLE:
            self.win.erase()
            self.win.addstr(1, 7, "CODE:  ")
        
        self.win.addstr(2, 7, '* '*len(self._sm.cur_code))
        
        if self._sm.state == StateMachine.CODEOK:
            self.win.addstr(1, 7, "SUCCESS")
        
        elif self._sm.state == StateMachine.CODEBAD:
            self.win.addstr(1, 7, "NO!    ")
        
        self.win.addstr(11, 7, "Curr PIN: "+" ".join(self._sm.cur_code))
        
        #Curses only draws changes to the screen when you ask nicely.
        self.win.refresh()
             

Take a moment to read over that code. You will find a lot of it is redundant. If we sort the calls based on what line number they draw to (the first number passed to addstr) we can get a clearer picture. We will also want to move that erase call to the top of the function so it clears the display before we draw our text. The same with the border function. A little bit of thought to the order and we can get something like this:

    def display_UI(self):
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

        self.win.addstr(16, 7, "NEW STATE: %s"%StateMachine.STATE_NAMES[self._sm.state])

        self.win.addstr(18, 7, "Press q or CTRL-c to quit.")

        self.win.refresh()

There is a lot more documentation of how this code draws in the combolock.py file.

But the code won't do anything obvious yet, because dispay_UI is not called by anything. If we look through the run function which should now look like this:

    def run(self):
        self.init_curses()
        
        #This while loop keeps checking the input you type on the keyboard
        while True:
            #Get a single keypress and turn it into a string
            c = chr(self.win.getch())
        
            #if you press q, terminate the program
            if c == 'q':
                break
        
            if c.isalnum():           
                self._sm.do_event(StateMachine.E_KEYPRESS, c)

        cleanup_curses()

We can see that the UI should be drawn after do_event is called, so put a call to display_UI after do_event and we will have something. Unfortunately this won't be everything. When the user first runs the program, python will wait at 

    c = chr(self.win.getch())

until you press a button, but display_UI hasn't been called yet so the user will see nothing. If we put a call to display_UI above the while True block right after self.init_curses, we can have it draw the UI before getting the character, then every loop looking for info will redraw the UI! The run method should now look like this:

    def run(self):
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

More details are included in the source including the face that we are not drawing the old state of the state machine in the code above like we were in iter1.


REVIEW (combolock.py)
-------------------
Now looking over the finished file, we have sections of code that have definite purposes and names. Reading over main for someone who is not familiar with this code should be easy because there is no mixing of unrelated code to get in the way of understanding the overall purpose.

We can also easily edit the display_UI function to add, remove, or edit lines of text, all in one place.

This iteration has drastically increased the quality of code and the understandability of the structure.
