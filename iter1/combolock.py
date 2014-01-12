from statemachine import StateMachine

"""Curses is a library for displaying more complex"""
"""UIs in terminals. read more at:"""
"""http://docs.python.org/2/howto/curses.html"""
import curses
import signal
import sys

"""If you do not clean up curses before the program ends
The terminal will act super weird and be hard to use."""
def cleanup_curses():
    curses.nocbreak();
    curses.echo()
    curses.endwin()

"""unction handler for when you press CTRL+C"""
def signal_handler(signal, frame):
    #Make sure we clean up curses if the user hits CTRL+C 
    cleanup_curses()
    sys.exit(0)

def main():
    #This makes it so if you hit CTRL+C curses doesn't eat the terminal alive!
    signal.signal(signal.SIGINT, signal_handler)
    
    #Setup curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    
    #Create the State Machine instance
    s = StateMachine()
    
    win = curses.newwin(20, 40, 2, 2)
    win.addstr(1, 7, "CODE:\n")
    win.addstr(18, 7, "Press q or CTRL-c to quit.")
    win.border()
    win.refresh()
    
    #This while loop keeps checking the input you type on the keyboard
    while True:
        #Get a single keypress and turn it into a string
        win.border()
        c = chr(win.getch())
        win.addstr(13, 7, "Correct PIN: "+" ".join(s.correct_code))
    
        #if you press q, terminate the program
        if c == 'q':
            break
    
        if c.isalnum():
            win.addstr(10, 7, "Prev PIN: "+" ".join(s.cur_code))
    
            old_state = s.state
            s.do_event(StateMachine.E_KEYPRESS, c)
            new_state = s.state
    
            #Write out some debug data
            win.addstr(15, 7, "OLD STATE: %s        "%s.STATE_NAMES[old_state])
            win.addstr(16, 7, "NEW STATE: %s        "%s.STATE_NAMES[new_state])
            win.addstr(18, 7, "Press q or CTRL-c to quit.")
    
            if s.state == StateMachine.IDLE:
                win.erase()
                win.addstr(1, 7, "CODE:  ")

            win.addstr(2, 7, '* '*len(s.cur_code))
    
            if s.state == StateMachine.CODEOK:
                win.addstr(1, 7, "SUCCESS")
    
            elif s.state == StateMachine.CODEBAD:
                win.addstr(1, 7, "NO!    ")
    
            win.addstr(11, 7, "Curr PIN: "+" ".join(s.cur_code))
    
            #Curses only draws changes to the screen when you ask nicely.
            win.refresh()
    
    cleanup_curses()

"""This is simply calling the main function if you run this file directly. """
"""If you import the file, main will not auto run. This way you can make"""
"""libraries other people can use, but are programs that can run by """
"""themselves too!"""
if __name__ == '__main__':
    main()
