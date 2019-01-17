Included Files:

    - VA.py
    - displays.py
    - events.py
    - setup.py
    - face.png
    - face1.png
    - README

    The following files are created after the intial running of the program:

    - config and userevents directory
    - alias.txt (in config directory)
    - settings.txt (in config directory)
    - Various event files in the form MonthDayYear (ex. 1222018.txt contains the event information for December 12th, 2018), (in userevents directory)


Acknowledgments:
    - ASCII character face found online at: 
      https://www.dreamstime.com/stock-photos-ascii-face-image1528033
    - Used pygame and datetime modules to implement our program
    - Used the pygame documentation to learn about certain functions:
      https://www.pygame.org/docs/


Running Instructions:

    - Our program is meant to be running on a Ubuntu operating system through the terminal

    - Prior to using our program the user must install pygame, this is most easily done using PIP, instructions to do so are as follows:

        - Within terminal, enter the following two lines separately:
            - "sudo apt-get install python3-pip"
            - "sudo pip3 install pygame"

    - Download all files from the "Included Files" section and place them in the same directory

    - Within terminal, navigate to the directory containing the files and enter:

        "python3 VA.py"

    - This will open the main menu and create the additional files in which user data and settings will be stored

    - From main menu, the user has 4 options which are selected by pressing keys 1-4:

        - (1) New Event : User can enter new events with desired name, date, time, location, and notes. All of these inputs are compared to the standard and user specific alias dictionary for any similarities.

        - (2) Todays's Schedule : User can view their schedule for the current day, up to 4 events.

        - (3) This Week's Schedule : User can view an overview of their schedule for the entire week.

        - (4) Settings : User can navigate to this menu and select either of the following:

            - (1) Name of virtual assistant : Upon selection of this option the user will be promoted to change the name of their virtual assistant

            - (2) Add Alias : Upon selection of this option the user will be prompted to enter a word followed by an alias for their virtual assistant to associate with that word when the user is creating new events

    - The user can press the escape key at any time to return to the main menu

    - The user can click the "X" circle in the top left corner of the window to close their virtual assistant

    - The virtual assistant can be used again anytime by navigating to the same directory and enter "python3 VA.py" the same way as before. Previous events, alias', and the virtual assistant name will still be available assuming the files storing them have not been moved or deleted.


Functionality:

    - Supported input forms:

        - All name and location inputs are also cross referenced with the same standard and user defined alias dictionary that the date and time strings are. This allows the user to create word "shortcuts" that our program will identify and replace with their related word (For example, user can add an alias so that the entry "CCIS" is treated as "Centennial Center for Interdisciplinary Science", our program will identify both CCIS and ccis as being related to this alias.)

        - Our virtual assistant is able to comprehend what the user means when entering the date and time information in a variety of forms. Some examples are as follows:

            For date inputs:

            - Common day and month word Alias' are supported in the base version of the program (they do not have to be added by the user). These include but are not limited to words such as: (Word: December, Alias: dec). Both uppercase and lowercase entries are supported

            - Our program will assume current date values if none are entered, for example if no date information is given the program will assume that the event is happening on the current day

            - Common date suffix's are understood (ex. 1st, 2nd, 3rd, 17th)

            - Punctuation such as "-" does not affect our program's ability to determine the date

            - The user can enter the date as simply "monday" and our program will understand that they mean the upcoming monday and determine the rest of the date information based off of that

            - The user could also preface the above statement with "next monday", and it will adjust the date accordingly (assuming that next monday is exactly a week following the upcoming monday, for example) while accounting for the fact that the "next" occurrence of a weekday could fall in a different month or year

            - Conversely our program can also determine the weekday from information such as dec 14th (with or without a year)

            - Any time a year is not given it is assumed that the user meant the current year

            For time inputs:

            - Our program is able to understand 3/4 digit times with the hours and minutes separated by a ":" character (such as 12:30 or 4:00, as well as 1/2 digit times (such as 5 or 12)

            - Our program understands the difference between AM and PM (uppercase or lowercase), when entered with a time value. It also supports there being a space or no space between the time number and the AM/PM characters

            - Our program assumes the user means AM times unless they are otherwise
            specified for both the start and end time values (i.e. 11:30 - 4:30 PM is taken to mean 11:30 AM - 4:30 PM)


Notes, Assumptions, and Bugs:

    - When the user is entering events, it is assumed that they are typing in English with basic grammatical correctness (spaces between words)

    - Currently our program is capable of storing an infinite number of events for any foreseeable dates/times, however it is slightly limited in its long-term display ability. Within "This Week's Schedule" our program displays the users events for the upcoming week. It can display a maximum of 6 events per day for the next 7 days (including the current day).

    - In Today's Schedule, the program will display the users event info in a different size/section of the screen depending on how many events the user has on the current day (i.e. the display scales). This happens if the user has between 1 and 4 events. If the user has more than 4 events on the current day, the display will show the first 4 events and then the user can press enter in order to view their next 1-4 events. The user can continually press enter until all events for the current day have been displayed.

    - The user can always press the escape key in order to return to the main menu, or if they are currently in the main menu, to exit the window.

    - Certain improper date/time entries currently cause bugs, as it is difficult to account for the large amount of ways in which a user could enter the date or time.

        - Known cases are as follows:

            - If a user enters only the name of a month when asked for the date, the program will not assign any Day to that event. However if the user enters just a weekday (ex. monday), our program is designed to understand and correctly handle this case.

    - Certain keystrokes (ex: the shift or caps lock key) cause errors in the way typing input is displayed in the pygame window, however this is only a visual bug. I.e. an input may appear to have a large space when displayed while the user is typing it on the screen however the string that our program reads will not contain this space.
