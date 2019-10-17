# ------------------------------------------------
#   Name: Ryan Kortbeek / Justin Boileau
#   Project: Virtual Assistant
#
#   Project: Virtual Assistant
#   File: events.py
#
# ------------------------------------------------

import string, datetime, os, setup
from calendar import monthrange

"""
This program determines what date/time information the user has entered and
creates an event class object to store the data, as well as writing to file.
Assumption is that the user typed in english and there is spaces between
words.
"""


class event:
    """
    The event class is created with 5 arguements, from these 5 arguements
    our program determines the characteristics of an event, these are:
     - name : title of event
     - weekday : (Monday, Tuesday, etc.)
     - daynum : (1, 6, 30, ect.) (as in December 15 where 15 is the daynum)
     - month : (April, May, etc.)
     - year : (1980, 2018, etc.)
     - starttime, endtime : for example, 10:30 AM and 2:45 PM
     - location : where the event takes place
     - additionalNotes : any extra notes the user wants to remember
     - path : location of the file storing any event information
     - attributes : a list containing all event characteristics excluding path,
                    used for writing event to file

    The event class has one method (eventWrite) which is called to write the
    an event to a file
    """
    def __init__(self, namestring, daymonthyear, timestring,
                 location, additionalNotes):
        self.name = aliasCheck(namestring)
        self.weekday, self.daynum, self.month, self.monthNum, self.year = decideDate(daymonthyear)
        self.starttime, self.endtime = decideTime(timestring)
        self.location = aliasCheck(location)
        self.additionalNotes = aliasCheck(additionalNotes)
        self.path = os.getcwd() + "/userevents"
        self.attributes = [self.name, self.weekday, self.month,
                           self.daynum, self.year, self.starttime,
                           self.endtime, self.location,
                           self.additionalNotes, "$"]
        self.validated = validate(self.weekday, self.daynum, self.monthNum,
                                  self.year)
        self.weekday = self.validated

    def eventWrite(self, event1):
        """
        eventWrite creates the event file path and writes event files line
        by line to that path
        """
        ## Order complexity : Constant + 10, can be considered irrelevant to
        ## overall order complexity
        # Checks if the user event directory is present and if not, creates it
        path = event1.path
        if not os.path.exists(path):
            os.mkdir(path)
        # Opens a file that sorts all user events
        fid = open("userevents/" + event1.monthNum + event1.daynum
                   + event1.year + ".txt", "a")
        # Writes all the event information, each attribute is on a new line
        # Attributes list is made so that there is a $ at the beginning
        # and end of the list, makes reading in files easer
        for line in range(len(event1.attributes)):
            ## Let p equal the number of elements in the attributes list,
            ## An event always has 10 attributes therefore p is always 10
            fid.write(event1.attributes[line])
            fid.write("\n")


def validate(weekday, daynum, monthnum, year):
    dayDict = {0 : "Monday" , 1 : "Tuesday" , 2 : "Wednesday" , 3
               : "Thursday" , 4 : "Friday" , 5 : "Saturday" , 6 : "Sunday"}
    dayDictrev = {"Monday" : 0 , "Tuesday" : 1 , "Wednesday" : 2,
                  "Thursday" : 3 , "Friday" : 4 , "Saturday" : 5 ,
                  "Sunday" : 6}
    expected = datetime.date(int(year), int(monthnum), int(daynum)).weekday()
    weekdaynum = dayDictrev[weekday]
    if weekdaynum != expected:
        correctday = dayDict[datetime.date(int(year), int(monthnum),
                                           int(daynum)).weekday()]
        return correctday
    else:
        return weekday


def getDayEvents(monthNum, daynum, year):
    """
    getDayEvents takes a month, day of month, and year integer arguement and
    reads the event file for that day, then returns a list with each event
    (and characteristics for that event) for the given day.
    """
    ## Order complexity : O(x)
    try:
        with open("userevents/" + monthNum + daynum + year + ".txt") as fid:
            day = []
            event = []
            eventnum = 0
            for line in fid:
                ## let x represent the number of lines in a given days event
                ## file
                line = line.strip("\n")
                if line == "$":
                    day.append(event)
                    eventnum += 1
                    event = []
                else:
                    event.append(line)
    # If there is no file for that day (i.e. there is no events that day,
    # return an empty list
    except:
        day = []
    return day


def aliasCheck(somestring):
    """
    aliasCheck takes a string arguement and checks if any of the words are
    part of a premade dictionary of alias', which the user can add to, if any
    are found it replaces them and then returns the new string
    """
    ## Order complexity : O(n*(sum(Vk)) where n is the number of elements in
    ## wordlist where k is from [1,m] where m is the number of keys

    # Calls a getAlias function from setup to get the current alias dictionary
    alias = setup.getAlias(0)

    # Creates a list containing each word from the string
    wordlist = somestring.split()
    copy = []

    # Loops through each word and replaces it if it is an alias
    ## Let n be the number of words in wordlist, m is the number of keys in the
    ## dictionary and Am is the number of values for the m'th key

    for word in wordlist:
        found = 0
        for key in alias.keys():
            for ali in alias[key]:
                if found != 1:
                    if word == ali:
                        copy.append(key)
                        found = 1
        if found == 0:
            copy.append(word)
    # rejoins the list with the replaced words (if any)
    out = " ".join(copy)
    # Returns NONE the arguement string was empty
    if out == "":
        return("NONE")
    return(out)


def decideDate(daymonthyear):
    """
    This takes the users daymonth year input string and attempts to figure
    out what day they mean, also checks if this day makes sense (i.e. if
    user enters tuesday nov 28 2018 the program should ask them if they
    meant wednesday as nov 28 2018 is a wednesday

    Also will set year, month, day to today if none are specified
    """
    ## Order complexity : O(n) + k where (k <= 7), therefore k can be
    ## disregarded so order complexity is O(n)

    # Initial processing of the input string to remove any unimportant
    # characters and find any inforation directly pertaining to day, month, and
    # year.
    weekdaylist, daynum, month, year = preProcess(daymonthyear)

    # Creates a list containing each word from the string in lowercase form
    wordlist = daymonthyear.lower().split()

    # Uses the datetime module to get information about the current date
    today = datetime.date.today()
    todayweekday = today.weekday()

    # Creates 4 dictionaries the are used to convert between the date/month
    # in numeric or word form
    dayDict = {0 : "Monday" , 1 : "Tuesday" , 2 : "Wednesday" , 3
               : "Thursday" , 4 : "Friday" , 5 : "Saturday" , 6 : "Sunday" }
    dayDictrev = {"Monday" : 0 , "Tuesday" : 1 , "Wednesday" : 2,
    "Thursday" : 3 , "Friday" : 4 , "Saturday" : 5 , "Sunday" : 6 }
    monthDict = {1 : "January", 2 : "Febuary" , 3 : "March" , 4 : "April", 5 :
                 "May" , 6 : "June" , 7 : "July" , 8 : "August" , 9 :
                 "September" , 10 : "October" , 11 : "November" ,
                 12 : "December" }
    monthDictrev = {"January" : 1 , "Febuary" : 2 , "March" : 3 , "April" : 4 ,
                    "May" : 5 , "June" : 6 , "July" : 7 , "August" : 8 ,
                    "September" : 9 , "October" : 10 , "November" : 11 ,
                    "December" : 12 }

    # The following if block is used to determine the full date if the user
    # enters just a day (ex. "monday" or "next friday")
    if year == "" and month == "" and len(weekdaylist) == 1:
        # Sets variables for the wanted weekday (0-6 for monday-sunday), day
        # of the month, month (1-12 for December-January), and year
        wantedWDN = dayDictrev[weekdaylist[0]]
        todayWDN = today.weekday()
        todayDAY = today.day
        todayMON = today.month
        daysInMON = monthrange(2018, 12)[1]
        todayYEAR = today.year
        found = False
        # If the word "next" was in the date string, our program understands
        # assumes that the user means the weekday following the one that they
        # entered ( i.e. next monday is taken to mean 7 days from the closest
        # monday )
        for word in wordlist:
            ## Let n be the number of elements in wordlist
            if word == "next":
                todayDAY += 7
                if todayDAY > daysInMON:
                    if todayMON == 12:
                        todayYEAR += 1
                        todayDAY = todayDAY - daysInMON
                        todayMON = 1
                    else:
                        todayDAY = todayDAY - daysInMON
                        todayMON += 1
        # Loops through days starting from the current day until the user
        # entered weekday is found. Accounts for the fact that the date the
        # user requested could fall a different month or year
        while not found:
            ## This loop never happens more than 7 times, so it applies a
            ## constant to the order complexity which can be ignored, let k
            ## represent the  number of times this loop executes
            if todayWDN == wantedWDN:
                date = datetime.date(todayYEAR, todayMON, todayDAY)
                found = True
            else:
                todayWDN += 1
                todayDAY += 1
                if todayDAY > daysInMON:
                    if todayMON == 12:
                        todayYEAR += 1
                        todayDAY = 1
                        todayMON = 1
                    else:
                        todayDAY = 1
                        todayMON += 1
                if todayWDN > 6:
                    todayWDN = 0

        # Assigns return variables based on the above result
        daynum = todayDAY
        month = monthDict[todayMON]
        year = todayYEAR

    # Assumed that if no year was specified that user meant cuurent year
    if year == "":
        year = today.year
    # Assumes that if no month was specified that user meant current month
    if month == "":
        month = monthDict[today.month]
    # Gets the day of the week based on which day, month, year the user entered
    if len(weekdaylist) == 0 and str(daynum) != "":
        weekdaylist.append(dayDict[datetime.date(int(year),
        monthDictrev[month], int(daynum)).weekday()])
    # If no weekday or day of month was entered assumed user meant today
    elif len(weekdaylist) == 0 and str(daynum) == "":
        weekdaylist.append(dayDict[today.weekday()])
        daynum = today.day

    # Sets the month number corresponding to the decided month
    monthNum = str(monthDictrev[month])

    return weekdaylist[0], str(daynum), month, monthNum, str(year)


def decideTime(timestring):
    """
    decide time takes a timestring arguement that the user enters and
    determines that start and end times for the event. Currently our function
    is able to determine the start and end times based on multiple input
    possibilities. We assumed the following about how people enter times:
      - If no AM or PM is attached to a given time, AM will be assumed
      - If a user wants to specify minutes (4:30 as opposed to just 4), they
        must include a ":" serperator
    """
    ## Order complexity: 2*O(n) = O(n) where n is the number of elements in
    ## word list (word list is each word in the time input string), we drop
    ## the constant 2.

    # Basic processing of time string to make it easier for our program to
    # understand
    timestring = timestring.replace("-", " ").replace("pm", " pm")
    timestring = timestring.replace("PM", " pm").replace("am", " am")
    timestring = timestring.replace("AM", " am")
    wordlist = timestring.lower().split()
    # Initializes all the start and end time variables to be 0
    starthour = 0
    startminutes = 0
    endhour = 0
    endminutes = 0
    foundstart = 0
    foundend = 0
    # Initializes the start and end "part" to be AM
    startpart = "AM"
    endpart = "AM"

    # Calls getAlias from the setup function to get the alias dictionary
    timeAlias = setup.getAlias(0)

    # Iterates through the timestring word list
    for word in wordlist:
        ## Let n be the number of words in wordlist
        # If program finds a ":" character, assumes it is reading the start
        # time
        if foundstart != 1 and ":" in word:
            if word[0:2].isdigit() == 1:
                starthour += int(word[0:2])
            else:
                starthour += int(word[0:1])
            startminutes += int(word[3:5])
            foundstart = 1
            continue

        # If the program finds a "am/AM" or "pm/PM", decides which part (start
        # or end) it is being applied to and changes the variables
        # appropriately
        for key in timeAlias.keys():
            if word in timeAlias[key] and key == "AM":
                startpart = "AM"
                endpart = "AM"
            if word in timeAlias[key] and key == "PM" and endpart == "AM":
                endhour += 12
                endpart = "PM"
                continue
            if word in timeAlias[key] and key == "PM" and endpart != "AM":
                starthour += 12
                startpart = "PM"

        # If program finds another ":" character, assumes it is reading the
        # end time
        if foundstart == 1 and ":" in word and foundend != 1:
            if word[0:2].isdigit() == 1:
                endhour += int(word[0:2])
                endminutes += int(word[3:5])
            else:
                endhour += int(word[0:1])
                endminutes += int(word[2:4])
            foundend = 1

        if (foundstart != 1 and len(word) <= 2 and len(word) >= 1 and
        word.isdigit() == 1):
            starthour += int(word)
            foundstart = 1
            continue
        if (foundstart == 1 and foundend != 1 and len(word) <= 2 and
        len(word) >= 1 and word.isdigit() == 1):
            endhour += int(word)
            foundend = 1
            continue

    # Changes int variables to string and adds "0"'s to match output
    # specifications
    if startminutes == 0:
        startminutes = str(startminutes) + "0"
    else:
        startminutes = str(startminutes)
        if len(startminutes) == 1:
            startminutes = "0" + startminutes
    if endminutes == 0:
        endminutes = str(endminutes) + "0"
    else:
        endminutes = str(endminutes)
        if len(endminutes) == 1:
            endminutes = "0" + endminutes

    # Adjusts the time if either start or end is PM, in future we could
    # modify this part to easily allow for 24 hour time.
    if startpart == "PM":
        starthour = str(starthour - 12)
    else:
        starthour = str(starthour)
    if endpart == "PM":
        endhour = str(endhour - 12)
    else:
        endhour = str(endhour)

    # Forms the final start and finish time strings
    starttime = starthour + ":" + startminutes + " " + startpart
    endtime = endhour + ":" + endminutes + " " + endpart

    # If either starttime or endtime were never found, sets them equal to
    # "None"

    if foundstart == 0:
        starttime = "None"
    if foundend == 0:
        endtime = "None"

    return starttime, endtime


def preProcess(somestring):
    """
    This function should take the string and return smaller strings that
    contain information our program thinks it related to specific elements
    of the date
    """
    ## Order complexity : O(n*(sum(Vk)) where n is the number of elements in
    ## wordlist where k is from [1,m] where m is the number of keys
    wordAlias = setup.getAlias(0)
    #print(wordAlias)

    daylist = ["Monday", "Tuesday", "Wednesday", "Thursday",
               "Friday", "Saturday", "Sunday"]
    monthlist = ["January", "Febuary", "March", "April", "May",
                 "June", "July", "August", "September", "October",
                 "November", "December"]
    # makes string lowercase so text is easier to process
    wordlist = somestring.lower().split()
    currentday = datetime.date.today()

    # Initializes the weekdaylist and weekdayinds list
    weekdaylist = []
    weekdayinds = []
    month = ""
    year = ""
    daynum = ""
    found = 0

    # Iterates through the worldlist and compares each word to the alias list,
    # then checks if any of these found words relate to month or day words, if
    # so sets the appropriate variables
    for word in wordlist:
        if (word[0].isdigit() == 1) or (word[0:2].isdigit() == 1):
            if (word[1:3] == "th") or (word[2:4] == "th"):
                word = word.replace("th", "")
                word = word.replace("st", "")
                word = word.replace("nd", "")
                word = word.replace("rd", "")
        ## Let number of words in word list = n
        found = 0
        for key in wordAlias.keys():
            ## Let number of keys in alias dictionary = m
            for ali in wordAlias[key]:
                ## Let Am be the number of alias' in the m'th key in the dict
                ## (Am is meant to be A subscript m)
                if word == ali:
                    if key in daylist:
                        weekdaylist.append(key)
                        weekdayinds.append(wordlist.index(word))
                        found = 1
                    if key in monthlist:
                        month = key
                        found = 1
        # Checks if the current word is potentially a year
        if found != 1 and year == "":
            if ((len(word) == 4) and (word.isdigit() == 1) and
                (int(word) >= 2018)):
                year = word
                found = 1
        # Checks if the current word is potentially a day of month
        if found != 1 and daynum == "" and (len(word) <= 2 and len(word) >= 1):
            daynum = int(word)
    # Returns date information to be further examined in decideDate
    return(weekdaylist, daynum, month, year)
