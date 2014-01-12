ITERATION 1 README
===================
-------------------

It is assumed for this iteration that you understand some of the basic constructs of python coding: The `if` statement, loops (while and for), and functions. It is also assumed that you know at least a little bit about classes, such as the difference between a class and an instance of that class, and how to use the self variable. Not knowing any of this does not mean you can not learn from this tutorial, but either way, make sure you look up any pieces you do not understand since I will not explain every single line (this is also a good habit to get into anytime you see something new in code).


INTRO
-------------------
A common thing I see with people who are beginning to learn how to program after they get the basic building blocks down is they do not know how to piece them together to produce a quality program.

I usually see this in two areas.

  The first know the building blocks, but when presented with a task, have no idea how to break it down into chunks. When faced with this entire task at once, they can feel overwhelmed and that it is too big for them to accomplish.

  The second case are people who are comfortable enough with stringing together logic and can write simple programs that behave in a straightforward manner, but freeze up when their structure can not handle certain cases.

I hope that by reading the descriptions in these readmes and then digging through the code, I will show you how to split a task into subtasks you already know how to do, and introduce how to wind your thought process around abstractions to produce flexible code.

In each iteration I will improve on the implementation of the previous iteration. Each new README will start with a criticism of the previous iteration and propose ways to alleviate those issues. After reading the README of each section please read through the code until you feel you understand it.




IMPLEMENTING A PROGRAM
-------------------
The first thing you have to do when designing a program is decide what it should do. For these examples we will be building a 4 pin digital combo lock That displays CORRECT or INCORRECT on the screen. 

We will also draw *s for each digit of the code you have entered, similar to typing into a password field. This means that when no digits are entered, there will be no *s, after one key is pressed, there will be 1 *, etc. 

There will also be a timeout so that after a certain amount of time of no activity, whatever digits you have typed in clear.

Now that we have the basics, we need to think about how to implement it. We are going to use the concept of Finite State Machines.

Finite State Machines (or just State Machines or SM for now) are surprisingly simple. You have a 'machine' (which can be a program, and the machine can be in one state. The machine has 1 or more states it CAN be in, but only one can be active at any one point in time. The machine also has rules for what states the machine can change to, and what causes it to change its state. 


FINITE STATE MACHINE EXAMPLE PROBLEM
-------------------
Lets give a simple separate example. Say we have a SM with two states. OPEN and CLOSED. While the machine is in the OPEN state, a door is open. While the machine is in the CLOSED STATE, the door is closed. There are two buttons on each side of the door: one marked OPEN_BUTTON and the other marked CLOSE_BUTTON. Lets also say that when the machine is first turned on, it is initially set to the CLOSED state. 

What happens when we press OPEN_BUTTON? Surprise! The door opens. But this requires the state machine to be set to the OPEN state. Pressing CLOSE_BUTTON causes the state machine to change to the closed state, thus closing the door. But if you press CLOSE_BUTTON while the machine is in the CLOSED state, it stays in that state. the same for pressing OPEN_BUTTON while the machine is in the OPEN state.

We define the following:

    Possible States: OPEN, CLOSED
    Initial State: CLOSED
    Input Signals: CLOSE_BUTTON, OPEN_BUTTON
    Transitions (signal, starting state, end state):
        OPEN_BUTTON: OPEN->OPEN
        OPEN_BUTTON: CLOSED->OPEN
        CLOSE_BUTTON: OPEN->CLOSED
        CLOSE_BUTTON: CLOSED->CLOSED

(NOTE: If the transition starts and ends on the same state, for example, CLOSED->CLOSED, then nothing has changed. It did not leave the state and come back in some roundabout way.)

This is a simple enough case, but it is important to note that it explicitly defines all the control states that the system can be in, and how to move between them. 


If we wanted to add a lock to the door that can be set from one side of the door, we have to edit our machine. We need to add a LOCKED state, and a input BUTTON_LOCK. Note that I could have made two signals, one for locking and unlocking similar to how I made a button for opening the door and another one for closing it, but we can make both work either way.

Before we can define the new machine, we need to describe the behavior we want the door to have. Just like before, when you press OPEN_BUTTON the door should open if it is closed, and stay open if it was already open. If you press CLOSE_BUTTON, the door should close if open, and stay closed if it is closed. 

The difference now is that when the door is closed, pressing LOCK_BUTTON will cause it to become locked, pressing LOCK_BUTTON while the door is locked will cause it to become unlocked, pressing LOCK_BUTTON while the door is open will cause nothing to happen because the door can not be locked while open, and finally pressing OPEN_BUTTON while the door is locked will also do nothing because it can not be opened while locked.

Lets look at our new definition for the state machine:

    Possible States: OPEN, CLOSED, LOCKED
    Initial State: CLOSED
    Input Signals: CLOSE_BUTTON, OPEN_BUTTON, LOCK_BUTTON
    Transitions (signal, starting state, end state):
        OPEN_BUTTON: OPEN->OPEN
        OPEN_BUTTON: CLOSED->OPEN
        OPEN_BUTTON: LOCKED->LOCKED
        CLOSE_BUTTON: OPEN->CLOSED
        CLOSE_BUTTON: CLOSED->CLOSED
        CLOSE_BUTTON: LOCKED->LOCKED
        LOCK_BUTTON: LOCKED->CLOSE
        LOCK_BUTTON: CLOSED->LOCKED
        LOCK_BUTTON: OPEN->OPEN


Reading through this list of transitions you can see we correctly specify that you can not open a locked door without first unlocking it because there is no transition from the LOCKED state directly to the OPEN state.



BACK TO THE REAL EXAMPLE:
-------------------
Now that we have seen basic ways to specify a State Machine, lets try to come up with the specs for a combo lock. There are two primary ways to attack this, and one is very wrong. The wrong way is to have a state for every possible combination of codes in the machine... so if we were limited to numbers only, that would be 10*10*10*10 plus whatever else we end up needing.

Instead of that terrible nightmare of thousands of states, lets simplify it to just a few:
A state for when no digits of the code have been entered.
A state for when ONE digit of the code have been entered.
A state for when TWO digits of the code have been entered.
A state for when THREE digits of the code have been entered.
A state for when FOUR digits of the code have been entered.
A state for when the code entered is correct.
A state for when the code entered is wrong.

Next we need the signals that transition the state machine:
When a key is pressed.
When no activity has happened for a while to clear the incomplete PIN.

Notice that we made the key event the pressing of any key instead of having a different input for each key. This is because the actual key does not matter in moving the state, we only need to store it for checking the PIN later. 

Another thing that is important is that almost all the transitions are defined, but two... how do we transition from the 4 digits state to the code OK or code BAD state? Since our only input signals are button presses and timeouts, we would require pressing some key to initiate the transition where if the code is correct, we move to that state, otherwise we move to the bad code state. This final key could be required to be the enter key if that is how you wanted it to work, but for now, we will just remove the 4 digit state and make it transition directly from the three digit state to the code good or the code bad state.

Note: The last paragraph introduce state transitions based on other variables besides the state of the machine, which is ok if you do it reasonably even though it slightly breaks the rules of what is strictly a state machine. Another way that is more in line with the state machine idea is have one state that displays CORRECT or INCORRECT, which may be what we do in the future iterations. 

I have provided a state graph in the file StateMachine.png.
The file StateMachineExtraState.png shows how the diagram would look with the state for 4 digits. We will be following the StateMachine.png file; this one is provided just as an example.



THE ACTUAL CODE
-------------------
The main file for this project is statemachine.py, which unsurprisingly implements the state machine. 

Inside it you will find a class definition. The purpose of this being a class is that you can in theory make multiple of them, and that the state machine becomes a single entity that you can interact with. Each state is a static member (not important if you don't know what that means but feel free to look it up) of the class, and the class has a function called do_event. The function takes two parameters when you call it: an event type which is one of the integers defined in the class, and an optional event parameter such as what key is pressed.

The function is entirely a sequence of `if` statements that switch what to do based on the current state of the machine. Notice that each of these `if` statements is an `elif` which means it will not run if any of the previous blocks ran. The reason this is so nice is that the order of the blocks doesn't actually matter. You can move the whole state `if` blocks to be in any order, and the program will behave the same. 

If this doesn't make sense, think about this, if in every `if` block we check the current state and once we find it, we optionally change to another state, AND none of the other blocks will run because of the `elif`s, then only one block of code will run per call to the do_event function. This isn't just a novel feature. A high level of determinism is very important in making sure your program doesn't randomly break when you make a small change like changing the order of the `if` blocks. Yes, we could do something a little more clever that involves the order of those blocks, but we can't get too ahead of ourselves or when we debug we will have no idea what is going on when something breaks.

Inside each `if` statement, there are other `if`s that check what the event was that triggered the call. The code then basically choses which sub block to run based on the event. If a state doesn't do anything in the case of a certain event, then there is no code for that case. 



The combolock.py file is the front end of the program. It handles drawing to the terminal and receiving button inputs/dispatching events to the state machine. I decided to use the curses library that lets you draw to the screen in more interesting ways, but it is a bit more complicated.


OTHER THINGS
-------------------
And lastly... I decided not to do the timeout feature for this iteration because it requires creating threads and other asynchronous constructs that will be more confusing than helpful. Look forward to that after an iteration or two. Also, the curses library is used to make everything look better. A possible exercise is creating another file that does the smae thing with normal prints.

