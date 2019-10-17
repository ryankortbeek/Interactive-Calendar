# ------------------------------------------------
#   Name: Ryan Kortbeek / Justin Boileau
#   Project: Virtual Assistant
#   File: displays.py
#
# ------------------------------------------------

import pygame, time, sys, string, datetime, math
# Imports our other code
import setup, events
# Initializes the pygame module
pygame.init()

# Creates userevents and config directories if they are not
# in the current working directory
initial = setup.checkFiles()
# If initial is 1 then it creates the alias dictionary, if
# initial is 0 it just gets the alias dictionary
wordAlias = setup.getAlias(initial)
# Gets the global variable corresponding to the name of the
# virtual assistant
name = setup.getSettings(initial)

# Global variables corresponding to select colors in their
# RGB form
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 125)
lightBlue = (0, 0, 255)
# Global variables corresponding to display height and width
displayWidth = 900
displayHeight = 600


def textDisp(text, size, x, y, colour = None, newFont = None):
    """
    This function displays text to the pygame display. The text that
    is being displayed is centered as the x and y position that are
    given as parameters are the coordinates of the character in the
    center of the message

    textDisp takes 6 inputs:
      - text: the characters to be printed
      - size: size of the font
      - x, y: location on display window text is centered around
      - colour: RGB value for text colour (defaults to black if none given)
      - newfont: font file to be used (defaults to freesansbold if none
        given)

    Text will not be displayed until the display is updated (i.e.
    pygame.display.update() is called)
    """
    # Checks if font is given
    if newFont is None:
        newFont = pygame.font.SysFont("Lucida Console", size)
    else:
        newFont = pygame.font.Font(newFont, size)
    # Checks if colour is given
    if colour is None:
        colour = (0, 0, 0)

    # Renders the text and colour
    textSurface = newFont.render(text, True, colour)
    # Sets the position (rectangle) where the text will be printed
    textSurf = textSurface
    textRect = textSurface.get_rect()
    textRect.center = ((x, y))
    # Writes the given text to given position
    mainDisplay.blit(textSurf, textRect)


def messageDisplay(text, size, x, y, color, timed, autoDisplay = None):
    """
    This function displays text to the pygame display one character at a
    time. This allows for the characters to be displayed in sequence (one
    at a time), with 0.03 seconds in between each character being displayed,
    or all at once. As well, the message that is being displayed is left
    oriented as the x and y position that are given as parameters are the
    coordinates of the first character. Uses the textDisp function to display
    each character

    messageDisplay takes 7 inputs:
      - text: the message to be printed
      - size: size of the font
      - x, y: location on display window of the first character
      - colour: RGB value for text colour
      - timed: boolean true or false for whether the message is to be
        displayed in sequential order with a 0.03 second delay in between
        each character being printed
      - autoDisplay: value for if the text is supposed to be displayed all
        at once with no visual lag
    """
    message = list(text)
    # Checks if the text is supposed to be displayed in sequential order or
    # all at once
    if timed:
        # Displays the message one character at a time
        for i in range(len(message)):
            textDisp(message[i], size, (i*12) + x, y, color)
            pygame.display.update()
            time.sleep(0.03)
    else:
        # If timed == False and autoDisplay has a value, the message will not
        # be displayed until the display is updated (i.e.
        # pygame.display.update() is called)
        for i in range(len(message)):
            textDisp(message[i], size, (i*12) + x, y, color)
            # Displays text all at once
            if autoDisplay is None:
                pygame.display.update()


def options(optionArray, x, y):
    """
    This function displays all the options in the list optionArray. Each option
    is displayed 0.3 seconds after the previous one. Uses the messageDisplay
    function

    options takes 3 inputs:
      - optionArray: list containing the different options
      - x, y: location on the display window of the first character for each
        option in the list (the y value changes for each indice of the list)
    """
    for i in range(len(optionArray)):
        messageDisplay(optionArray[i], 17, x, (i*45) + y, black, False)
        time.sleep(0.3)


def loadImage(file, start_x, start_y, final_x, final_y, change_x, change_y):
    """
    This function moves an image from one location to another

    loadImage takes 7 inputs:
      - file: image file to load and display
      - start_x, start_y: the initial x, y coordinates of the image
      - final_x, final_y: the final x, y coordinates of the image
      - change_x: the change in the x-position of the image every 0.0006
        seconds
      - change_y: the change in the y-position of the image every 0.0006
        seconds
    """
    img = pygame.image.load(file)
    # Displays the image in the pygame window at its starting coordinates
    (x, y) = (start_x, start_y)
    mainDisplay.blit(img, (x, y))
    pygame.display.update()
    # Increments the x, y coordinates of the image by change_x and change_y,
    # updates the images location, and then pauses for 0.0006 seconds. Repeats
    # until the image is at its final x, y coordinates
    while ((round(x), round(y)) != (final_x, final_y)):
        x += change_x
        y += change_y
        mainDisplay.fill(white)
        mainDisplay.blit(img, (x, y))
        pygame.display.update()
        time.sleep(0.0006)


def mainMenu():
    """
    This function creates the pygame display and opens the main menu
    """
    # We decided to make mainDisplay a global variable because it ends up
    # being more efficient than passing it as an argument to all the functions
    # that use it
    global mainDisplay
    # Initializes the pygame display
    mainDisplay = pygame.display.set_mode((displayWidth, displayHeight))
    mainDisplay.fill(white)
    # Animate our mascots movement from an initial position (0, 0) to its final
    # position on the right side of the display window
    loadImage("face1.png", 0, 0, 5*displayWidth/9, displayHeight/5, 1, 120/500)
    # Displays the opening messages in sequential order with a slight delay in
    # between each character being printed
    messageDisplay("I'm " + name + ", your virtual assistant.", 19,
                   (displayWidth/14) - 10, 30 + (displayHeight/4), black, True)
    messageDisplay("What would you like to do?", 19, displayWidth/12,
                   70 + (displayHeight/4), black, True)
    # Displays the four modes of the virtual planner
    options(["(1) New Event", "(2) Today's Schedule",
             "(3) This Week's Schedule", "(4) Settings"], displayWidth/10,
            110 + (displayHeight/4))

    # Enters a loop where the user can interact with the program
    while True:
        if pygame.mixer.get_busy() is not None:
            for event in pygame.event.get():
                # Exits the pygame window and the program if the user tries
                # to exit the window
                if (event.type == pygame.QUIT):
                    pygame.display.quit()
                    sys.exit()
                # Checks if the user is typing and then responds accordingly.
                # If the user selects a mode by typing either 1, 2, 3, or 4,
                # then mainMenu() will return the respective value. If any
                # other value is entered, the program will prompt the user to
                # enter a valid character
                if event.type == pygame.KEYDOWN:
                    character = event.unicode
                    # Exits the pygame window and the program if the user
                    # presses the escape key (uses sys.exit() to exit program)
                    if character == '\x1b':
                        pygame.display.quit()
                        sys.exit()
                    # Selects the make new event mode
                    if (character == '1'):
                        selection = 1
                        return selection
                    # Selects the mode that displays todays events
                    if (character == '2'):
                        selection = 2
                        return selection
                    # Selects the mode that displays this weeks events
                    if (character == '3'):
                        selection = 3
                        return selection
                    # Selects the settings mode
                    if (character == '4'):
                        selection = 4
                        return selection
                    # If the user enters an invalid character, the program will
                    # prompt the user to select a valid option and remind the
                    # user of the valid options
                    elif (character not in '1234'):
                        messageDisplay("Please select a valid option", 16,
                            displayWidth/14, 10*displayHeight/12, red, False)
                        messageDisplay("Press 1, 2, 3, or 4 for the desired\
 functionality", 15, (displayWidth/14), 30 + (10*displayHeight/12), red, False)


def interaction(iteration, initialize = None):
    """
    This function displays the respective message according to the value of
    the variable iteration when called. If the variable initialize has a value
    then the message displays with no lag, otherwise each message will display
    in sequential order (as per messageDisplay)

    interaction takes 2 inputs:
      - iteration: variable storing a value which represents what iteration of
        the loop the function newEvent() is on
      - initialize: determines whether the message is loaded to the pygame
        window (not displayed until pygame.display.update() is called)
        immediately or displayed sequentially (will display sequentially if no
        value is passed through initialize)
    """
    if initialize is None:
        # Displays the desired message based on the current value of iteration
        # in sequential order (character by character)
        if (iteration == 0):
            messageDisplay("What is the name of your event?", 18,
                           2*displayWidth/5, displayHeight/2, black, True)
        if (iteration == 1):
            messageDisplay("What date is your event?", 18, 2*displayWidth/5,
                           displayHeight/2, black, True)
        if (iteration == 2):
            messageDisplay("What time is your event at?", 18, 2*displayWidth/5,
                           displayHeight/2, black, True)
        if (iteration == 3):
            messageDisplay("Where is your event?", 18, 2*displayWidth/5,
                           displayHeight/2, black, True)
        if (iteration == 4):
            messageDisplay("Do you have any extra notes?", 18,
                           2*displayWidth/5, displayHeight/2, black, True)
        if (iteration == 5):
            messageDisplay("Is all the information entered above correct?", 18,
                           (2*displayWidth/5) - 40, displayHeight/2,
                           black, True)
        if (iteration == 6):
            messageDisplay("Which part is incorrect?", 18, (2*displayWidth/5)
                           - 40, displayHeight/2, black, True)
            messageDisplay("Press (1) to customize the event name", 18,
                           (2*displayWidth/5) - 40, 30 + 2*displayHeight/3,
                           black, True)
            messageDisplay("(2) to customize the event date", 18,
                           (2*displayWidth/5) + 32, 60 + 2*displayHeight/3,
                           black, True)
            messageDisplay("and so on...", 18, (2*displayWidth/5) + 36, 90 +
                           2*displayHeight/3, black, True)
        if (iteration > 6):
            messageDisplay("Enter new information: ", 18,
                           (2*displayWidth/5) - 40, displayHeight/2, black,
                           True)
    else:
        # Loads the desired message based on the current value of iteration
        # to the display window (message will not display until
        # pygame.display.update() is called)
        if (iteration == 0):
            messageDisplay("What is the name of your event?", 18,
                           2*displayWidth/5, displayHeight/2, black, False, 0)
        if (iteration == 1):
            messageDisplay("What date is your event?", 18, 2*displayWidth/5,
                           displayHeight/2, black, False, 0)
        if (iteration == 2):
            messageDisplay("What time is your event at?", 18, 2*displayWidth/5,
                           displayHeight/2, black, False, 0)
        if (iteration == 3):
            messageDisplay("Where is your event?", 18, 2*displayWidth/5,
                           displayHeight/2, black, False, 0)
        if (iteration == 4):
            messageDisplay("Do you have any extra notes?", 18,
                           2*displayWidth/5, displayHeight/2, black, False, 0)
        if (iteration == 5):
            messageDisplay("Is all the information entered above correct?", 18,
                           (2*displayWidth/5) - 40, displayHeight/2, black,
                           False, 0)
        if (iteration == 6):
            messageDisplay("Which part is incorrect?", 18, (2*displayWidth/5) -
                           40, displayHeight/2, black, False, 0)
            messageDisplay("Press (1) to customize the event name", 18,
                           (2*displayWidth/5) - 40, 30 + 2*displayHeight/3,
                           black, False, 0)
            messageDisplay("(2) to customize the event date", 18,
                           (2*displayWidth/5) + 32, 60 + 2*displayHeight/3,
                           black, False, 0)
            messageDisplay("and so on...", 18, (2*displayWidth/5) + 36, 90 +
                           2*displayHeight/3, black, False, 0)
        if (iteration > 6):
            messageDisplay("Enter new information: ", 18,
                           (2*displayWidth/5) - 40, displayHeight/2, black,
                           False, 0)


def newEventDisplay(firstIteration):
    """
    This function initializes the display for the new event mode of the
    virtual assistant

    newEventDisplay takes 1 input:
      - firstIteration: boolean true or false value reflecting whether
        or not it is the first iteration of newEvent - basically only
        animates the movement of our image (of our mascot) to its final
        location (via loadImage function) if firstIteration is true.
        Other than that it sets up the display for the new event mode
    """
    if firstIteration:
        # Clears the pygame window
        mainDisplay.fill(white)
        # Animates the movement of the mascot from an initial position
        # on the bottom right side of the display to its final position
        # on the bottom left side of the display
        loadImage("face.png", displayWidth, 30 + (5*displayHeight/12),
                  (displayWidth/9) - 50, 30 + (5*displayHeight/12), -2, 0)
        pygame.display.update()
        # Displays the headers and layout for the new event mode
        messageDisplay("New Event", 22, 50, 40, black, False)
        messageDisplay("_________", 22, 50, 43, black, False)
        messageDisplay("PRESS ESCAPE TO RETURN", 14, 600, 40, red, False)
        messageDisplay("TO MAIN MENU", 14, 600, 60, red, False)
        messageDisplay("Event name: ", 18, 50, 100, black, False)
        messageDisplay("Event date: ", 18, 50, 130, black, False)
        messageDisplay("Time of event: ", 18, 50, 160, black, False)
        messageDisplay("Location of event: ", 18, 50, 190, black, False)
        messageDisplay("Extra notes: ", 18, 50, 220, black, False)
    else:
        # Clears the pygame window
        mainDisplay.fill(white)
        # Loads the image to its position on the bottom left side of the
        # display
        img = pygame.image.load("face.png")
        mainDisplay.blit(img, ((displayWidth/9) - 50,
                               30 + (5*displayHeight/12)))
        # Loads the headers and layout for the new event mode
        messageDisplay("New Event", 22, 50, 40, black, False, 0)
        messageDisplay("_________", 22, 50, 43, black, False, 0)
        messageDisplay("PRESS ESCAPE TO RETURN", 14, 600, 40, red, False, 0)
        messageDisplay("TO MAIN MENU", 14, 600, 60, red, False, 0)
        messageDisplay("Event name: ", 18, 50, 100, black, False, 0)
        messageDisplay("Event date: ", 18, 50, 130, black, False, 0)
        messageDisplay("Time of event: ", 18, 50, 160, black, False, 0)
        messageDisplay("Location of event: ", 18, 50, 190, black, False, 0)
        messageDisplay("Extra notes: ", 18, 50, 220, black, False, 0)
        # Displays everything all at once
        pygame.display.update()


def refresh(iteration, translatedEvent = None):
    """
    This function is used to aid in providing backspace functionality to the
    new event mode. It basically reloads the pygame display by redisplaying
    whatever is currently shown (other than the user inputted information)

    refresh takes 2 inputs:
      - iteration: value corresponding to the iteration of newEvent that the
        program is on. Used to refresh the message associated with the
        current iteration of newEvent
      - translatedEvent: optional value to include while iteration is less
        than or equal to 4. However once iteration is greater than 4, this
        class object must be included as it corresponds to the information
        entered by the user
    """
    # Reloads current state of pygame display (in new event mode)
    mainDisplay.fill(white)
    img = pygame.image.load("face.png")
    mainDisplay.blit(img, ((displayWidth/9) - 50, 30 + (5*displayHeight/12)))
    messageDisplay("New Event", 22, 50, 40, black, False, 0)
    messageDisplay("_________", 22, 50, 43, black, False, 0)
    messageDisplay("PRESS ESCAPE TO RETURN", 14, 600, 40, red, False, 0)
    messageDisplay("TO MAIN MENU", 14, 600, 60, red, False, 0)
    messageDisplay("Event name: ", 18, 50, 100, black, False, 0)
    messageDisplay("Event date: ", 18, 50, 130, black, False, 0)
    messageDisplay("Time of event: ", 18, 50, 160, black, False, 0)
    messageDisplay("Location of event: ", 18, 50, 190, black, False, 0)
    messageDisplay("Extra notes: ", 18, 50, 220, black, False, 0)
    # Loads the message associated with the current iteration that newEvent
    # is on
    interaction(iteration, 0)
    if iteration > 4:
        # Loads the interpreted input (by the user) information to the
        # display
        eventInfo(translatedEvent)
    # Immediately displays all the aspects of the new event mode that are
    # currently displayed. Useful for backspace functionality as it will
    # reload the display with virtually no lag so everything but the
    # deleted character(s) will look the same
    pygame.display.update()


def translatedEventInfo(createEvent):
    """
    This function uses the user inputted information to get the programs
    interpretation of the input. Uses our other file events.py to sort
    through the input and get a class object containing all the
    interpreted information

    translatedEventInfo takes 1 input:
      - createEvent: list containing all of the users responses to each
        aspect about the new event they want to create
    """
    # Uses the event class from the file events.py to get the programs
    # interpretation of the users input re their new event.
    # Indices of the list createEvent are in the same order as they
    # are enter (createEvent[0] is event name, createEvent[1] is event
    # date, etc...)
    translatedEvent = events.event(createEvent[0], createEvent[1],
                                   createEvent[2], createEvent[3],
                                   createEvent[4])
    # Pads the endtime aspect of class object translatedEvent
    # in order to allow for customization of the entered time (if the
    # user wishes to overwrite the programs interpretation of their
    # input for time, their customized input is assigned to
    # translatedEvent.starttime and translatedEvent.endtime is assigned
    # a value of "". Thus by padding this initial value with 2 spaces,
    # it allows us to trim the last two characters in the string at all
    # times. As a result, it removes the usual "- " that the program
    # adds between starttime and endtime if the user customizes the
    # programs interpretation of their time input). See the eventInfo
    # function for where this happens
    translatedEvent.endtime += "  "
    return translatedEvent


def eventInfo(translatedEvent):
    """
    This function displays all of the user-entered information about the new
    event that the user is creating. Uses the data from the class object
    translatedEvent and formats it for better aesthetic

    options takes 1 input:
      - createEvent: list containing all of the user-entered information for
        the new event
    """
    # Creates the output format for date of the event as (Day Month Date Year)
    date = (translatedEvent.weekday + " " + translatedEvent.month + " " +
        translatedEvent.daynum + " " + translatedEvent.year)
    # Creates the output format for the time of the event
    # The " - " is the part that is trimmed if the user customizes the
    # value for time (translatedEvent.endtime would have a value of "")
    time = (translatedEvent.starttime + " - " + translatedEvent.endtime)
    # Loads the event info to the display via messageDisplay (won't actually
    # display until pygame.dislpay.update() is called)
    messageDisplay(translatedEvent.name, 17, 300, 100, lightBlue, False, 0)
    messageDisplay(date, 17, 300, 130, lightBlue, False, 0)
    # Displays the string assigned to the variable time except for the last
    # two characters (see comments above, as well as the comments in the
    # function translatedEventInfo for more details)
    messageDisplay(time[:-2], 17, 300, 160, lightBlue, False, 0)
    messageDisplay(translatedEvent.location, 17, 300, 190, lightBlue, False, 0)
    messageDisplay(translatedEvent.additionalNotes, 17, 300, 220, lightBlue,
                   False, 0)


def newEvent(iteration, fix = None):
    """
    This function runs the mode newEvent and is responsible for providing
    an interface for the user to interact with in order to create a new
    event

    newEvent takes 2 inputs:
      - iteration: an integer value that tells the function what stage
        of interaction the user is on with the program with regards to
        the making of their new event
      - fix: an optional argument to pass to the function that allows for
        the user to customize the programs interpretation of their input
        re their new event (relevant after the user has answered all of
        the programs questions regarding their new event)

    Returns to the main menu if the user presses the escape key
    """
    # Initializes the display (including the animated motion of our
    # mascot to its final position). This only happens at the beginning
    # of the newEvent sequence (i.e iteration == 0)
    if iteration == 0:
        # Initializes a list for the users input to be stored in and makes
        # it a global variable
        global createEvent
        createEvent = []
        newEventDisplay(True)
    elif iteration > 0:
        # Refreshes the display
        newEventDisplay(False)
        # Uses the user entered input regarding their event and uses the
        # function translatedEventInfo to translate it. The interpretation
        # is then displayed to the pygame window via the function
        # eventInfo
        if (iteration == 5) and (fix is None):
            global translatedEvent
            translatedEvent = translatedEventInfo(createEvent)
            eventInfo(translatedEvent)
            pygame.display.update()
        # Displays the current information associated with the class
        # object translatedEvent (used after the user has customized part
        # of the programs interpretation of their info)
        elif (iteration == 5) and (fix is not None):
            eventInfo(translatedEvent)
            pygame.display.update()
        # More general case that has the same functionality as the above
        # elif statement
        elif (iteration > 5):
            eventInfo(translatedEvent)
            pygame.display.update()

    # Displays the appropriate message corresponding to the current
    # of iteration. See the function interaction for more details
    # on what message is associated with each value of iteration
    interaction(iteration)
    # Initializes a variable for the users input to be stored
    string = ""
    # Initializes a variable corresponding to the spacing between each
    # displayed input character on the pygame window
    i = 0
    # Enters a loop where the user can interact with the program
    while True:
        if pygame.mixer.get_busy() is not None:
            for event in pygame.event.get():
                # Exits the pygame window and the program if the user
                # presses the exit button
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                # Enters this if statement if the user is typing
                if event.type == pygame.KEYDOWN:
                    # Returns to the main menu if the user presses the
                    # escape key
                    character = event.unicode
                    if character == '\x1b':
                        main()
                    # Enters this if statement if the user presses enter
                    if character == '\r':
                        # If the program is finished asking questions
                        # about the users event
                        if (iteration > 4):
                            # If all of the displayed information
                            # regarding the users event is correct,
                            # (i.e. the user enters "yes" or "ya" in any
                            # part of their input (when iteration is 5))
                            # a verification message is displayed on an
                            # all blue screen and then the program
                            # returns to the main menu
                            if (iteration == 5):
                                if (('yes' in string.lower()) or
                                    ('ya' in string.lower())):
                                    translatedEvent.eventWrite(translatedEvent)
                                    mainDisplay.fill(blue)
                                    textDisp("Your event has been created, you\
 will now return to the main menu.", 18, displayWidth/2, displayHeight/2,
                                   white)
                                    pygame.display.update()
                                    time.sleep(3)
                                    main()
                                # Otherwise newEvent is recursively
                                # called where the program will then
                                # ask the user how they want to
                                # customize the displayed info re
                                # their event
                                else:
                                    iteration += 1
                                    newEvent(iteration)
                            # Checks which aspect of the event info
                            # that the user wishes to customize and
                            # then recursively calls newEvent with
                            # a value corresponding to the aspect of
                            # the event info that they would like to
                            # change, passed as the value for "fix"
                            elif (iteration == 6):
                                iteration += 1
                                if ('1' in string):
                                    newEvent(iteration, 1)
                                elif ('2' in string):
                                    newEvent(iteration, 2)
                                elif ('3' in string):
                                    newEvent(iteration, 3)
                                elif ('4' in string):
                                    newEvent(iteration, 4)
                                elif ('5' in string):
                                    newEvent(iteration, 5)
                            # Depending on the value of fix, the
                            # program will overwrite the old info
                            # corresponding to a certain aspect of
                            # their new event with the users new
                            # input
                            elif (iteration == 7):
                                # We had to change the attributes
                                # value of the class object
                                # translatedEvent corresponding to
                                # the aspect of the users new event
                                # that they would like to change
                                # along with the characteristic value
                                # of translatedEvent in order for the
                                # program to store the customized
                                # information instead of the
                                # initially translated info
                                if (fix == 1):
                                    translatedEvent.attributes[0] = string
                                    translatedEvent.name = string
                                elif (fix == 2):
                                    translatedEvent.attributes[1] = string
                                    translatedEvent.attributes[2] = ""
                                    translatedEvent.attributes[3] = ""
                                    translatedEvent.attributes[4] = ""
                                    translatedEvent.weekday = string
                                    translatedEvent.month = ""
                                    translatedEvent.daynum = ""
                                    translatedEvent.year = ""
                                elif (fix == 3):
                                    translatedEvent.attributes[5] = string
                                    translatedEvent.attributes[6] = ""
                                    translatedEvent.starttime = string
                                    translatedEvent.endtime = ""
                                elif (fix == 4):
                                    translatedEvent.attributes[7] = string
                                    translatedEvent.location = string
                                elif (fix == 5):
                                    translatedEvent.attributes[8] = string
                                    translatedEvent.additionalNotes = string
                                iteration = 5
                                # Recursively calls newEvent with an
                                # iteration value of 5 so that the program
                                # asks the user if all the displayed info
                                # about their event is correct. A value of
                                # 0 is passed as the value for "fix" so
                                # that the program doesn't recreate
                                # the class object translatedEvent based
                                # on the original input (i.e. so the
                                # customization actually changes the
                                # initial value of whatever aspect the
                                # user was changing)
                                newEvent(iteration, 0)
                        # If the value of iteration is <= 4 it means
                        # that the program has not asked all its questions
                        # regarding the users event, so the current string
                        # which contains the users answer to the current
                        # question regarding their event, is added to the
                        # list createEvent in the appropriate location.
                        # newEvent is then called with an iteration value
                        # of += 1
                        else:
                            iteration += 1
                            createEvent.append(string)
                            newEvent(iteration)
                    # Backspace functionality
                    else:
                        if character == '\x08':
                            # If the current iteration is <= 4, the pygame
                            # window will refresh and load all of the
                            # present information to the screen except for
                            # the most recent character (which is
                            # essentially deleted)
                            if iteration <= 4:
                                string = string[:-1]
                                refresh(iteration)
                                messageDisplay(string, 16, 2*displayWidth/5,
                                               40 + (displayHeight/2), blue,
                                               False, 0)
                                # If a character has been displayed, the
                                # location where the next character will be
                                # displayed is moved back a space. Otherwise
                                # if the user has not typed anything yet,
                                # the location where the next character will
                                # be displayed remains the preset starting
                                # location
                                if (i > 0):
                                    i -= 1
                            # This case is run when the iteration is
                            # greater than 4. It essentially does the same
                            # as the above (if iteration <= 4) statement
                            # however, it also refreshes the displayed info
                            # regarding the users event
                            else:
                                string = string[:-1]
                                refresh(iteration, translatedEvent)
                                messageDisplay(string, 16, 2*displayWidth/5,
                                               40 + (displayHeight/2), blue,
                                               False, 0)
                                # Same functionality as the identical if
                                # statement abvoe
                                if (i > 0):
                                    i -= 1
                        # If none of the above cases happen, the character
                        # corresponding to the pressed key is added to the
                        # string and loaded to the pygame window
                        else:
                            string += character
                            textDisp(character, 16, i*12 + (2*displayWidth/5),
                                     40 + (displayHeight/2), blue)
                            # Shifts the location of where the next character
                            # is to be displayed
                            i += 1
                        # Displays all the changes made to the pygame window
                        pygame.display.update()


def currentDate(dayToday = None):
    """
    This function uses the datetime module in order to get the
    current date. We use the current date (month-day-year) in order to get
    the name of the file that contains the events that the user has "today"
    (however this does not happen in this function)

    currentDate takes 1 optional argument:
      - dayToday: if the function is called with a value passed associated
        to dayToday, the function will return the weekday (a value between
        0 and 6 where 0 corresponds to Monday, 1 corresponds to Tuesday,
        etc.) on top of the usual values it returns

    Returns the current month, date, and year according to the datetime
    module. If the function is called with a value associated with
    dayToday, the current weekday will also be returned (value between 0
    and 6)
    """
    # Uses the datetime module to get the current day
    today = datetime.datetime.now()
    # Gets the current month, date and year
    month, day, year = str(today.month), str(today.day), str(today.year)
    # If the function is called with a value associated with
    # dayToday, the current weekday will also be returned (value
    # between 0 and 6)
    if dayToday is not None:
        weekday = today.weekday()
        return month, day, year, weekday
    else:
        return month, day, year


def todaysCalendar(rows, eventsToday, displayNumber):
    """
    This function displays a calendar-like layout to the pygame window.
    The coordinates of some of the strings that are displayed were
    mostly found by the method of guess and check to find what
    looked best, which is why some may look quite random. This function
    uses messageDisplay to print to the pygame window

    calendar takes 1 input:
      - rows: number of rows to be displayed (max of 4 per page)
      - eventsToday: a list containing n number of lists for each n
        events that day
      - displayNumber: value corresponding to the display number (since
        there is a max of 4 events that can be displayed each day, in
        cases where there are more than 4 events on a given day, this
        variable accounts for the current display number which tells
        the program which events to display). In this way the first
        display would show events 1-4, the second would display events
        5-8, etc.
    """
    # Sets the max number of rows (4) per display if the user has
    # > 4 events today
    if rows > 4:
        rows = 4

    # Sets parameters responsible for setting up where objects are
    # printed on the display based on the number of events for the
    # day (numbers were chosen based off what generally looked the
    # best for all the cases)

    # Changes the size of the font based on the number of events today
    size = 17 - rows
    change_y = 42 - (4*rows)
    add_y = (20*rows) - 70
    # Prints sections on the display based on the value associated with
    # "rows", seperated by horizontal lines
    for j in range(1, rows):
        for i in range(0, 900):
            textDisp("_", 18, i*1, j*displayHeight/rows, black)
    pygame.display.update()
    # Variable responsible for scaling the y-value of an aspect of
    # eventsToday so that everything displays in the correct location
    diff_y = 1
    # Displays todays calendar if the user only has one event for the day
    if rows == 1:
        messageDisplay("Event name: ", size, 100, 200, black, False)
        messageDisplay("Event date: ", size, 100, 250, black, False)
        messageDisplay("Time of event: ", size, 100, 300, black, False)
        messageDisplay("Location of event: ", size, 100, 350, black, False)
        messageDisplay("Extra notes: ", size, 100, 400, black, False)
        # Displays the info corresponding to the users events today
        for a in range(len(eventsToday[0])):
            messageDisplay(eventsToday[0][a], size, 350, 200 + (a*50),
                           lightBlue, False)
    # Displays todays calendar for cases where the user has more than one
    # event today
    else:
        # Displays each aspect of the event info in each section (number of
        # sections based on the number of events today)
        for k in range(1, rows + 1):
            messageDisplay("Event name: ", size, 50, add_y +
                           (k*displayHeight/rows) - (5*change_y), black, False)
            messageDisplay("Event date: ", size, 50, add_y +
                           (k*displayHeight/rows) - (4*change_y), black, False)
            messageDisplay("Time of event: ", size, 50, add_y +
                           (k*displayHeight/rows) - (3*change_y), black, False)
            messageDisplay("Location of event: ", size, 50, add_y +
                           (k*displayHeight/rows) - (2*change_y), black, False)
            messageDisplay("Extra notes: ", size, 50, add_y +
                           (k*displayHeight/rows) - change_y, black, False)
            # Displays the info corresponding to the users events today in
            # each appropriate section (i.e. different section for each event)

            # If it is not the initial display (first 4 events), the program
            # gets the appropriate events from the list eventsToday (if its the
            # second display, the program will print events 5-8 from the
            # eventsToday as the outer loop cycles through the defined values
            # of k)
            if displayNumber > 0:
                # Case where eventsToday would be out of range (in other words,
                # all events have been displayed)
                if (k + displayNumber*4 - 1) >= len(eventsToday):
                    pass
                # Displays the info corresponding to an event if eventsToday is
                # still in range
                elif (k + displayNumber*4 - 1) < len(eventsToday):
                    for b in range(len(eventsToday[k + (displayNumber*4) - 1])):
                        messageDisplay(eventsToday[k + (displayNumber*4) - 1][b],
                                       size, 300, add_y +
                                       (diff_y*displayHeight/rows) -
                                       ((5-b)*change_y), lightBlue, False)
            # Prints the info corresponding to an event if it is the first
            # display. Responsible for printing event info when there are
            # <= 4 events today
            elif displayNumber == 0:
                for b in range(len(eventsToday[k - 1])):
                    messageDisplay(eventsToday[k - 1][b], size, 300, add_y +
                                   (k*displayHeight/rows) - ((5-b)*change_y),
                                   lightBlue, False)
            # Allows for the scaling of the y-location of event info (so
            # everything displays in the right spot)
            diff_y += 1


def preProcess(today):
    """
    This function formats the information associated with all of the users
    events today

    preProcess takes 1 input:
      - today: list containg n lists corresponding to each n events today

    Returns a list containing n lists corresponding to each n events
    for which the info is preprocessed
    """
    todayPP = []
    # Formats the info for each event today
    for i in range(len(today)):
        # Creates a temporary list for the formatted info of an event to be
        # stored in, formats all of the info related to an event, appends
        # the preprocessed info to the temporary list and then appends the
        # temporary list to the list for preprocessed events today (i.e.
        # the info corresponding to each event is in the right format)
        tempList = []
        tempList.append(today[i][0])
        date = (today[i][1] + " " + today[i][2] + " " + today[i][3] + ", " +
                today[i][4])
        tempList.append(date)
        if "none" == today[i][6].lower():
            time = today[i][5] + " - ..."
        else:
            time = today[i][5] + " - " + today[i][6]
        tempList.append(time)
        tempList.append(today[i][7])
        tempList.append(today[i][8])
        todayPP.append(tempList)
    return todayPP


def todaysSchedule():
    """
    This function runs the mode todaysSchedule and is responsible for providing
    an interface for the user to view all their events for the day. At most 4
    events are displayed per display, however the user can press enter to see
    the next 1-4 events and so on as long as they have more events. As soon as
    all events have been displayed, pressing enter will not take them to a new
    page, but they can return to the main menu by pressing escape. If the user
    has less than 4 events on a given day, todays schedule will scale/look
    differently!
    """
    # Clears display
    mainDisplay.fill(white)
    # Uses the function currentDate (which uses the datetime module) to get
    # the current date
    month, day, year = currentDate()
    # Uses the current date to get the events that happen today. Calls
    # getDayEvents from the events.py file which gets the appropriate
    # events
    today = events.getDayEvents(month, day, year)
    # If there are no events today, displays a special message
    if len(today) == 0:
        messageDisplay("Today's Schedule", 22, 50, 30, black, True)
        messageDisplay("________________", 22, 50, 33, black, False)
        messageDisplay("PRESS ESCAPE TO RETURN", 14, 600, 30, red, False)
        messageDisplay("TO MAIN MENU", 14, 600, 50, red, False)
        messageDisplay("No events scheduled for today :(", 20, 75, 100,
                       black, True)
        # Sets these values to 0 so that the variables are defined when
        # mentioned in the while loop below, however they have no
        # significance when equal to 0, as there are no events today
        displayNumber = 0
        numDisplays = 0
    else:
        # If there is one event today, the header is displayed in the top
        # left corner of the window
        if len(today) == 1:
            messageDisplay("Today's Schedule", 22, 50, 30, black, True)
            messageDisplay("________________", 22, 50, 33, black, False)
        # Displays a special message if there are more than 4 events today.
        # The program then clears the window and sets the header in the top
        # right corner of the pygame window (more space to display events
        # and event info)
        elif len(today) > 4:
            messageDisplay("Better get a coffee, today looks busier than usual!",
                           20, 75, 100, black, True)
            messageDisplay("Press enter to see more of your events for the day.",
                           20, 75, 150, black, True)
            messageDisplay("Your first 4 events are as follows...", 20, 75,
                           200, black, True)
            # Pauses the program for 2.5 seconds
            time.sleep(2.5)
            mainDisplay.fill(white)
            messageDisplay("Today's Schedule", 22, 640, 40, black, True)
            messageDisplay("________________", 22, 640, 43, black, False)
        # If there are (1 < events <= 4) today, sets the header in the top
        # right corner of the pygame window
        else:
            messageDisplay("Today's Schedule", 22, 640, 40, black, True)
            messageDisplay("________________", 22, 640, 43, black, False)

        messageDisplay("PRESS ESCAPE TO RETURN TO MAIN MENU", 13, 450, 15,
                       red, False)
        # Preprocesses the information regarding all of the users events today
        todayPP = preProcess(today)
        # Initializes the display number and displays todays calendar to the
        # pygame window via the function todaysCalendar
        displayNumber = 0
        todaysCalendar(len(todayPP), todayPP, displayNumber)
        # Gets the max number of displays needed (uses the math module to
        # round up so no events get cut off)
        numDisplays = math.ceil(len(todayPP)/4)

    # Enters a loop where the user can interact with the program
    while True:
        if pygame.mixer.get_busy() is not None:
            for event in pygame.event.get():
                # Exits the pygame window and the program if the user
                # presses the exit button
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                # Enters this if statement if the user is typing
                if event.type == pygame.KEYDOWN:
                    character = event.unicode
                    # Returns to the main menu if the user presses the
                    # escape key
                    if character == '\x1b':
                        main()
                    if character == '\r':
                        # While there is still more events than currently
                        # displayed, pressing the enter key allows the
                        # user to see their next 1-4... events
                        displayNumber += 1
                        if displayNumber < numDisplays:
                            mainDisplay.fill(white)
                            messageDisplay("Today's Schedule", 22, 640, 40,
                                           black, False, 0)
                            messageDisplay("________________", 22, 640, 43,
                                           black, False, 0)
                            messageDisplay("PRESS ESCAPE TO RETURN TO MAIN MENU",
                                           13, 450, 15, red, False, 0)
                            pygame.display.update()
                            # Displays the users next n events while n is
                            # in the range of todayPP
                            todaysCalendar(len(todayPP), todayPP,
                                displayNumber)


def weeklyCalendar(columns, weekPP, currentDay):
    """
    This function displays a calendar-like layout to the display window.
    In this function the location of many messages that are printed to
    the pygame window were found by guess and check, based on what
    looked/worked best. As a result some may be random

    calendar takes 3 inputs:
      - columns: number of columns to be displayed
      - weekPP: preprocessed list containing lists corresponding to the
        users events that week
      - currentDay: string value containing the name of the current day
    """
    # Prints 7 columns to the screen seperated by verticle lines
    for i in range(1, columns):
        for j in range(80, 600):
            textDisp("|", 18, i*displayWidth/columns, j*1, black)

    dayOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                 "Saturday", "Sunday"]
    weekDays = []
    cycle = 0
    # Uses the current day passed to the function to find the
    # appropriate index in the list dayOfWeek. Builds a new list
    # where today is the zeroth element and so on
    x = dayOfWeek.index(currentDay)
    while (cycle < 7):
        weekDays.append(dayOfWeek[x])
        x += 1
        if x == 7:
            x = 0
        cycle += 1
    # Prints the name of each day for the upcoming week with the first
    # day displayed (left-most) being today
    for day in range(len(weekDays)):
        messageDisplay(weekDays[day], 15, (2*(day + 1)*displayWidth/14)-110,
                       90, black, False, 0)
        # Prints an underline under each weekday name
        for letter in range(round(2.25*len(weekDays[day]))):
            messageDisplay("_", 12, (letter*5) +
                           (2*(day + 1)*displayWidth/14)-110, 92,
                           black, False, 0)
    # If there are no events on a given day in the upcoming week, the
    # program prints the message "No events" under that day
    for day in range(len(weekPP)):
        if len(weekPP[day]) == 0:
            messageDisplay("No events", 14,
                           (2*(day + 1)*displayWidth/14)-110, 110,
                           blue, False, 0)
        # If there are more events on a given day, the program will
        # display them on the pygame window in the appropriate
        # location
        else:
            for event in range(len(weekPP[day])):
                y = 90 + (event*70)
                # We figured that for optimal viewing, it was best to show
                # a max of 6 events per day and if there were more,
                # displayed a "cont..." message at the bottom of the column
                # under the corresponding day
                if event > 6:
                    messageDisplay("cont...", 12,
                                   (2*(day + 1)*displayWidth/14)-110, y + 10,
                                   red, False, 0)
                # Otherwise displays the events on a given day
                else:
                    for info in range(len(weekPP[day][event])):
                        y += 20
                        # Gets the relevant info with regards to the current
                        # iteration of the loop and checks if its too long
                        # to fit in the column for a given day. If the
                        # string is too long, the program prints the first
                        # 6 characters and replaces the rest with "..." so
                        # that the info fits in its column
                        string = weekPP[day][event][info]
                        if len(string) > 9:
                            string = string[:6] + "..."
                        messageDisplay(string, 14,
                                       (2*(day + 1)*displayWidth/14)-110, y,
                                       blue, False, 0)
    # Updates the display so that everything loaded to the pygame window is
    # displayed
    pygame.display.update()


def weeklyEvents():
    """
    This function gets the current day and then uses it to create a list
    which stores the events for the next week. The zeroth index of the
    list stores a list which contains n lists corresponding to the n
    events the user has today, and so on. Uses the getDayEvents function
    from our events.py file which gets the events for each day in the
    upcoming week

    Returns a list containing the events for the upcoming week and the
    name of the current weekday
    """
    week = []
    dayOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                 "Saturday", "Sunday"]
    # Uses the currentDate function to get the current month, date, year,
    # and current day
    month, day, year, currentDay = currentDate(0)
    # Uses the integer value associated with the current weekday (from
    # currentDay) to get the name of the weekday
    currentDay = dayOfWeek[currentDay]
    # Uses the current date to get the events that happen today. Increases
    # the value of the date by 1 to get the events for the upcoming week.
    # Calls getDayEvents from the events.py file which gets the
    # appropriate events
    for nextDay in range(7):
        week.append(events.getDayEvents(month, str(int(day) + nextDay), year))
    # If there are no events on a given day the function getDayEvents
    # returns an empty list for that day
    return week, currentDay


def weeklyPreProcess(week, today):
    """
    This function formats the information associated with all of the users
    events in the upcoming week

    weeklyPreProcess takes 2 inputs:
      - week: all the users events for the upcoming week
      - today: the name of the current weekday

    Returns a list containing n lists corresponding to each day where
    each day is composed of n lists corresponding to the n events that
    occur that day, where the info for each event is preprocessed
    """
    weekPP = []

    # For each day in the list week, the function goes through the
    # events on that day and formats them in the desired way
    for day in range(len(week)):
        currentDay = []
        # If there are no events on a given day, an empty list will
        # be appended to the preprocessed list
        if len(week[day]) == 0:
            weekPP.append([])
        # Otherwise if there are events on a given day, the relevant
        # info, including the event name and start-end time is
        # formatted
        else:
            for event in range(len(week[day])):
                eventsToday = []
                # Gets the event name
                eventsToday.append(week[day][event][0])
                # Gets the start and end time
                if "none" == week[day][event][6].lower():
                    eventsToday.append(week[day][event][5])
                    eventsToday.append("-...")
                else:
                    eventsToday.append(week[day][event][5])
                    eventsToday.append("-" + week[day][event][6])
                # Appends the info for an event to a list for the
                # events that day
                currentDay.append(eventsToday)
            # Appends the list of events (with preprocessed info)
            # for a given day to the list for the weeks events
            weekPP.append(currentDay)
    return weekPP


def weeklySchedule():
    """
    This function runs the mode weeklySchedule and is responsible for
    providing an interface for the user to view all their events for
    the upcoming week
    """
    # Clears the display and prints headers for the weeklySchedule
    # mode
    mainDisplay.fill(white)
    messageDisplay("This Week's Schedule", 22, 30, 30, black, True)
    messageDisplay("____________________", 22, 30, 33, black, False)
    messageDisplay("PRESS ESCAPE TO RETURN", 14, 600, 30, red, False)
    messageDisplay("TO MAIN MENU", 14, 600, 50, red, False)
    # Uses the weeklyEvents function to get the events for the week
    # as well as the currentDay
    week, currentDay = weeklyEvents()
    # Creates a preprocessed version of the list "week" to be
    # displayed in the pygame window
    weekPP = weeklyPreProcess(week, currentDay)
    # Displays the weekly calendar according to the preprocessed list
    # of events for the week
    weeklyCalendar(7, weekPP, currentDay)

    # Enters a loop where the user can interact with the program
    while True:
        if pygame.mixer.get_busy() is not None:
            for event in pygame.event.get():
                # Exits the pygame window and the program if the user
                # presses the exit button
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                # Enters this if statement if the user is typing
                if event.type == pygame.KEYDOWN:
                    # Returns to the main menu if the user presses the
                    # escape key
                    character = event.unicode
                    if character == '\x1b':
                        main()


def refreshSettings(selection, timed = None):
    """
    This function sets up the display for the settings mode of the
    program/virtual assistant. Also helps in adding backspace
    functionality, as if no value is passed with timed, the current
    state of the pygame display will be refreshed so the program
    can delete the last character typed by the user (the deletion
    part is done in settings). If a value is passed with timed,
    the program will display the appropriate message character by
    character (via messageDisplay)

    refreshSettings takes 2 inputs:
      - selection: value that determines the current state of the
        setttings mode. For each value of selection, a different
        message/prompt is displayed/refreshed
      - timed: optional parameter. When the function is called and
        timed has no value, the program will refresh the current
        state of settings
    """
    mainDisplay.fill(white)
    messageDisplay("Settings", 22, 30, 30, black, False, 0)
    messageDisplay("________", 22, 30, 33, black, False, 0)
    messageDisplay("PRESS ESCAPE TO RETURN", 14, 600, 30, red, False, 0)
    messageDisplay("TO MAIN MENU", 14, 600, 50, red, False, 0)
    if (selection == 1) and (timed is None):
        messageDisplay("Please enter the new name for your virtual assistant:",
                       18, displayWidth/8, displayHeight/3, black, False, 0)
    elif (selection == 1) and (timed is not None):
        # Displays character by character
        messageDisplay("Please enter the new name for your virtual assistant:",
                       18, displayWidth/8, displayHeight/3, black, True)
    elif (selection == 2) and (timed is None):
        messageDisplay("Enter the word to create an alias for:", 18,
                       displayWidth/8, displayHeight/3, black, False, 0)
    elif (selection == 2) and (timed is not None):
        # Displays character by character
        messageDisplay("Enter the word to create an alias for:", 18,
                       displayWidth/8, displayHeight/3, black, True)
    elif (selection == 3) and (timed is None):
        messageDisplay("Ok, what word should I associate with that word?", 18,
                       displayWidth/8, displayHeight/3, black, False, 0)
        # Displays character by character
    elif (selection == 3) and (timed is not None):
        messageDisplay("Ok, what word should I associate with that word?", 18,
                       displayWidth/8, displayHeight/3, black, True)
    pygame.display.update()


def settings(selection = None):
    """
    This function runs the mode settings and is responsible for
    providing an interface for the user to either change the name
    of their virtual assistant or to add an alias

    settings takes 1 optional input:
      - selection: integer value which represents the users
        selected functionality for the settings mode (i.e.
        when the user selects (1) the program will prompt the user
        to change the name of their virtual assistant and if
        the user selects (2) the program will prompt the user
        to add an alias)
    """
    # Initial case where the header and options are printed to the
    # pygame window
    if selection is None:
        mainDisplay.fill(white)
        messageDisplay("Settings", 22, 30, 30, black, True)
        messageDisplay("________", 22, 30, 33, black, False)
        messageDisplay("PRESS ESCAPE TO RETURN", 14, 600, 30, red, False)
        messageDisplay("TO MAIN MENU", 14, 600, 50, red, False)
        options(["(1) Name of virtual assistant", "(2) Add Alias"],
                displayWidth/8, displayHeight/3)
    # Prompts the user to enter the desired name for their virtual
    # assistant via refreshSettings
    elif selection == 1:
        refreshSettings(selection, 0)
    # Prompts the user to add an alias via refreshSettings
    elif selection == 2:
        refreshSettings(selection, 0)

    string = ""
    i = 0
    x = 0
    # Enters a loop where the user can interact with the program
    while True:
        if pygame.mixer.get_busy() is not None:
            for event in pygame.event.get():
                # Exits the pygame window and the program if the user
                # presses the exit button
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                # Enters this if statement if the user is typing
                if event.type == pygame.KEYDOWN:
                    # Returns to the main menu if the user presses the
                    # escape key
                    character = event.unicode
                    if character == '\x1b':
                        main()
                # Initial case
                if selection is None:
                    if event.type == pygame.KEYDOWN:
                        # Runs the desired functionality of settings
                        # based on the users selection. If the user
                        # doesn't enter a valid selection, the
                        # program will prompt the user to enter
                        # a valid suggestion
                        character = event.unicode
                        if (character == '1'):
                            selection = 1
                            settings(selection)
                        if (character == '2'):
                            selection = 2
                            settings(selection)
                        elif (character not in '12'):
                            messageDisplay("Please select a valid option", 16,
                                           displayWidth/14,
                                           10*displayHeight/12, red, False)
                            pygame.display.update()
                            messageDisplay("Press 1 or 2 for the desired\
 functionality", 15, (displayWidth/14), 30 + (10*displayHeight/12), red, False)
                            pygame.display.update()

                # Enters this if the user wants to change their virtual
                # assistants name
                elif selection == 1:
                    if event.type == pygame.KEYDOWN:
                        # Changes the name and returns the user to the main
                        # menu when the user presses enter after entering
                        # the new name for their virtual assistant
                        character = event.unicode
                        if character == '\r':
                            global name
                            name = string
                            pygame.display.set_caption(name)
                            y = setup.getSettings(0, name)
                            mainDisplay.fill(blue)
                            textDisp("Success, you will now return to the main\
 menu.", 18, displayWidth/2, displayHeight/2, white)
                            pygame.display.update()
                            time.sleep(3)
                            main()
                        # Backspace functionality
                        if character == '\x08':
                            string = string[:-1]
                            refreshSettings(selection)
                            messageDisplay(string, 17, displayWidth/8, 50 +
                                           (displayHeight/3), blue, False, 0)
                            if (i > 0):
                                i -= 1
                        # Adds the typed character to the string for the
                        # virtual assistants new name and displays the
                        # typed character in the pygame window
                        else:
                            string += character
                            textDisp(character, 17, i*12 + (displayWidth/8),
                                     50 + (displayHeight/3), blue)
                            i += 1
                    pygame.display.update()

                # Enters this if the user wants to add an alias
                elif selection == 2:
                    if event.type == pygame.KEYDOWN:
                        # After the user has entered a word to
                        # create an alias for and pressed enter
                        # settings is called recursively in order
                        # for the user to enter a word to associate
                        # with the alias
                        character = event.unicode
                        if character == '\r':
                            newWord = string
                            string = ""
                            character = ""
                            selection = 3
                            refreshSettings(selection, 0)
                        # Backspace functionality
                        if character == '\x08':
                            string = string[:-1]
                            refreshSettings(selection)
                            messageDisplay(string, 17, displayWidth/8, 50 +
                                           (displayHeight/3), blue, False, 0)
                            if (i > 0):
                                i -= 1
                        # Adds the typed character to the string for the
                        # word to create an alias for and displays the
                        # typed character in the pygame window
                        else:
                            string += character
                            textDisp(character, 17, i*12 + (displayWidth/8),
                                     50 + (displayHeight/3), blue)
                            i += 1
                    pygame.display.update()

                # Second part of when the user wants to add an alias
                elif selection == 3:
                    if event.type == pygame.KEYDOWN:
                        # After the user has entered a word to
                        # associate with the previously entered word
                        # and pressed enter, the program will add
                        # the word to the alias dictionary from
                        # our other file setup.py
                        character = event.unicode
                        if character == '\r':
                            # Adds the alias to the dictionary which the
                            alias = setup.getAlias(0, newWord, string)
                            mainDisplay.fill(blue)
                            textDisp("Success, association learned.", 18,
                                     displayWidth/2, displayHeight/2, white)
                            pygame.display.update()
                            time.sleep(3)
                            main()
                        # Backspace functionality
                        if character == '\x08':
                            string = string[:-1]
                            refreshSettings(selection)
                            messageDisplay(string, 17, displayWidth/8, 50 +
                                           (displayHeight/3), blue, False, 0)
                            if (x > 0):
                                x -= 1
                        # Adds the typed character to the string for the
                        # word to associate with the previously entered word
                        # and displays the typed character in the pygame
                        # window
                        else:
                            string += character
                            textDisp(character, 17, x*12 + (displayWidth/8),
                                     50 + (displayHeight/3), blue)
                            x += 1
                    pygame.display.update()


def main():
    """
    This function runs the program (virtual assistant)
    """
    # Sets the name of the pygame window based on the current value
    # associated with the string name
    pygame.display.set_caption(name)
    # Opens the main menu and gets the mode that the user wants to run
    option = mainMenu()
    # Runs the desired functionality based on the users selection
    if (option == 1):
        # Initializes the new event sequence by setting iteration to
        # 0 and running the newEvent mode
        iteration = 0
        newEvent(iteration)
    if (option == 2):
        todaysSchedule()
    if (option == 3):
        weeklySchedule()
    if (option == 4):
        settings()


main()
