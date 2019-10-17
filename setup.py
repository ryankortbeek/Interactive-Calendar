# ------------------------------------------------
#   Name: Ryan Kortbeek / Justin Boileau
#   Project: Virtual Assistant
#
#   Project: Virtual Assistant
#   File: setup.py
#
# ------------------------------------------------

import os


def checkFiles():
    """
    checkFiles checks for the three directories our program stores
    information in, and if they are not found it will create them.
    """
    path = os.getcwd()
    initial = 0

    if not os.path.exists(path + "/userevents"):
        os.mkdir(path + "/userevents")

    if not os.path.exists(path + "/config"):
        os.mkdir(path + "/config")
        initial = 1

    return initial


def getSettings(initial, newname = None):
    """
    getSetting takes 2 input, one of which is optional. If it is the first
    time our program has been run, the function will create the settings.

    Within the setting file we store what the user wants the name of their
    personal assistant to be.

    getSettings will also determine the current name of the assitant by
    reading from the settings file.
    """

    path = os.getcwd() + "/config" + "/settings.txt"

    if initial == 1:
        # Write fresh file
        with open(path, "w+") as fid:
            fid.write("name:\n")
            fid.write("CARL")
            return "CARL"

    if (newname == None) or (newname == ""):
        with open(path, "r") as fid:
            for line in fid:
                if line == "name:\n":
                    foundname = 1
                    continue
                if foundname == 1:
                    name = line
                    return name
    else:
        with open(path, "w+") as fid:
            fid.write("name:\n")
            fid.write(newname)
            return newname


def getAlias(initial, newword = None, newwordalias = None):
    """
    getAlias is another version of readAlias which is able to write
    the initial basic alias dictionary if it is the users first time
    running our program. It is also able to add new words to the existing
    alias file.
    """

    path = os.getcwd() + "/config" + "/alias.txt"

    words = []

    # If this is the first time running our program, creates the basic
    # alias list and writes it to the alias file
    if initial == 1:
        wordAlias = {"Monday": ["monday", "mon"], "Tuesday":
                     ["tuesday","tue","tues"],
            "Wednesday": ["wednesday", "wed"], "Thursday":
            ["thursday","thurs"],
            "Friday": ["friday","fri"], "Saturday": ["saturday", "sat"],
            "Sunday": ["sunday","sun"] , "January":
            ["January", "january", "jan"] ,
            "February" : ["February", "february", "feb"] , "March":
            ["March", "march", "mar"] ,
            "April" : ["April", "april", "apr"] , "May" :
            ["May", "may", "ma"] ,
            "June" : ["June", "june", "jun"] , "July" :
            ["July", "july", "jul"] ,
            "August" : ["August", "august", "aug"] , "September" :
            ["September", "september", "sept"] ,
            "October" : ["October", "october", "oct"], "November" :
            ["November", "november", "nov"] ,
            "December" : ["December", "december", "dec"] ,
            "PM" : ["pm", "afternoon"] , "AM" : ["am", "morning"] }

        writeAlias(wordAlias)
        return wordAlias

    else:
        wordAlias = readAlias()

        if newword != None:
            if newword in wordAlias.keys():
                if newwordalias.lower() not in wordAlias[newword]:
                    wordAlias[newword].append(newwordalias.lower())
                    wordAlias[newword].append(newwordalias.upper())
                    wordAlias[newword].append(newwordalias)
            else:
                wordAlias[newword] = []
                wordAlias[newword].append(newwordalias.lower())
                wordAlias[newword].append(newwordalias.upper())
                wordAlias[newword].append(newwordalias)
            writeAlias(wordAlias)
    return wordAlias


def readAlias():
    """
    readAlias navigates to the path where the alias dictionary and is stored
    and reads it line by line. readAlias then returns the alias dictionary.
    """

    path = os.getcwd() + "/config" + "/alias.txt"
    wordAlias = {}

    with open(path) as fid:
        for line in fid:
            if line == "$\n":
                newword = 1
                continue
            if newword == 1:
                word = line.strip("\n")
                wordAlias[word] = []
                newword = 0
                continue
            else:
                wordAlias[word].append(line.strip("\n"))

    return wordAlias


def writeAlias(wordAlias):
    """
    writeAlias takes the word alias dictionary and writes it to the specified
    file where it is to be stored and then accessed by the readAlias
    function
    """
    path = os.getcwd() + "/config" + "/alias.txt"

    with open(path, "w+") as fid:
        for key in wordAlias.keys():
            fid.write("$\n")
            fid.write(key + "\n")
            for alias in wordAlias[key]:
                fid.write(alias + "\n")
    return
