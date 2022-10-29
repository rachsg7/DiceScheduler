import datetime
import csv
import json
from fileinput import filename
from os.path import exists
from re import U
from tkinter import Y
from firebase_admin import db

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("YOUR_JSON_FILE_HERE.JSON")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://YOUR_DATABASE_HERE.firebaseio.com/"
})

ref = db.reference("Database reference")

WRITE_DEMOLD_INDEX = 0
FULL_CURE_INDEX = 1 
KEY_INDEX = 0
NAME_INDEX = 1
DESC_INDEX = 2
DATE_INDEX = 3
RESIN_INDEX = 4
READ_DEMOLD_INDEX = 5
CURE_INDEX = 6
TUMBLER_INDEX = 7
TUMBLER_DATE_INDEX = 8

def main():
    """
    Calls the Menu in a loop until user exits
    """
    while True:
        choose_option()

def compute_full_cure_time(date, cure_time):
    """
    The full cure time for a set of dice varies based on resin type.
    'date' is the variable for the date the dice were first made
    'cure_time' is the amount of days to fully cure the resin used. Usually 24 - 72 hours
    """
    later = date + datetime.timedelta(days = cure_time)
    return later

def compute_demold_time(date, cure_time):
    """
    The demold time for a set of dice varies based on resin type.
    'date' is the variable for the date the dice were first made.
    'cure_time' is the amount of days to demold time based on the resin used. Usually 12-14 hours
    """
    later = date + datetime.timedelta(days = cure_time)
    return later

def compute_tumbler_time(date):
    """
    I tumble my dice for 48 hours, so this is calculating +2 days in the tumbler
    from when they first went in.
    """
    later = date + datetime.timedelta(days = 2)
    return later

def create_dice():
    """
    Creates dice and saves it to file.
    """
    dice = input_dice()

    save_dice(dice)

def input_dice():
    dice = []
    dice_name = input('What is the name of this set? ')
    dice_desc = input('Description: ')

    dice_date = input('Date dice were cast (mm/dd/yy): ')
    dice_date = datetime.datetime.strptime(dice_date, '%m/%d/%y')
    dice_date = dice_date.date()

    dice_resin = input('Resin used (Artnglow, ResinObsession): ')
    if (dice_resin == 'Artnglow') or (dice_resin == 'ResinObsession'):
        error = False
    else:
        error = True
    while error:
        print('Please enter valid input:')
        dice_resin = input('Resin used (Artnglow, ResinObsession): ')
        if dice_resin == 'Artnglow' or dice_resin == 'ResinObsession':
            error = False

    resin = get_resin()
    demold_time = compute_demold_time(dice_date, resin[dice_resin][WRITE_DEMOLD_INDEX])
    full_cure_time = compute_full_cure_time(dice_date, resin[dice_resin][FULL_CURE_INDEX])

    tumbler = input('Ready to put in tumbler? (T/F)? ')
    if tumbler.lower() == 't':
        date = input('What date did they go in the tumbler (mm/dd/yy)? ')
        date = datetime.datetime.strptime(date, '%m/%d/%y')
        date = date.date()
        tumbler = True
        tumbler_date = compute_tumbler_time(date)
    else:
        tumbler_date = 'Not yet ready'
        tumbler = False

    dice.append(0) # This is reserved for the key
    dice.append(dice_name)
    dice.append(dice_desc)
    dice.append(dice_date)
    dice.append(dice_resin)
    dice.append(demold_time)
    dice.append(full_cure_time)
    dice.append(tumbler)
    dice.append(tumbler_date)

    return dice
    
def save_dice(dice, append = True, delete = False):
    """
    Saves dice to database
    """
    x = {
            "name": dice[NAME_INDEX],
            "description": dice[DESC_INDEX],
            "date": dice[DATE_INDEX],
            "resin": dice[RESIN_INDEX],
            "demoldTime": dice[READ_DEMOLD_INDEX],
            "fullCureTime": dice[CURE_INDEX],
            "tumbler": dice[TUMBLER_INDEX],
            "tumblerDate": dice[TUMBLER_DATE_INDEX]
        }

    if(delete):
        key = dice[KEY_INDEX]
        die_ref = ref.child('dice/' + key)
        die_ref.delete()
        print('Die has been deleted.')

    elif(append):
        users_ref = ref.child('dice')
        y = json.dumps(x, default=str)
        users_ref.push(y)
    else:
        key = dice[KEY_INDEX]
        die_ref = ref.child('dice/' + key)
        y = json.dumps(x, default=str)
        die_ref.set(y)


def get_resin():
    resin = {
        # "Resin name" : [demold time, full cure time]
        "Artnglow" : [1, 3],
        "ResinObsession" : [1, 1]
    }

    return resin


def update_dice():
    """
    Update die from list
    """
    dice = read_dice()
    count = 0
    options = ['Name', 'Description', 'Date Created', 'Tumbler Ready?', 'Everything']

    for die in dice:
        print(f'[{count}] : {die[NAME_INDEX]}')
        count += 1

    user_input = int(input('Which die would you like to update? '))
    count = 0

    for option in options:
        print(f'[{count}] : {option}')
        count += 1
    
    print()
    user_input_update = int(input('What would you like to update? '))
    die = dice[user_input]

    # Update Everything
    if user_input_update == 4:
        die = input_dice()

    # Update Name
    elif user_input_update == 0:
        name = input('Name: ')
        die[NAME_INDEX] = name

    # Update Description
    elif user_input_update == 1:
        desc = input('Description: ')
        die[DESC_INDEX] = desc

    # Update Date
    elif user_input_update == 2:
        date = input('Date Created: ')
        dice_date = datetime.datetime.strptime(date, '%m/%d/%y')
        dice_date = dice_date.date()
        die[DATE_INDEX] = dice_date

        resin = get_resin()
        die_resin = die[RESIN_INDEX]
        demold_time = compute_demold_time(dice_date, resin[die_resin][WRITE_DEMOLD_INDEX])
        full_cure_time = compute_full_cure_time(dice_date, resin[die_resin][FULL_CURE_INDEX])

        die[READ_DEMOLD_INDEX] = demold_time
        die[CURE_INDEX] = full_cure_time

    # Update Tumbler Date
    elif user_input_update == 3:
        tumbler = input('Is it in the tumbler? (T/F): ')
        if tumbler.lower() == 't':
            date = input('What date did they go in the tumbler (mm/dd/yy)? ')
            date = datetime.datetime.strptime(date, '%m/%d/%y')
            date = date.date()
            tumbler_date = compute_tumbler_time(date)
            die[TUMBLER_INDEX] = True
            die[TUMBLER_DATE_INDEX] = tumbler_date
            
        else:
            tumbler_date = 'Not yet ready'
            die[TUMBLER_DATE_INDEX] = tumbler_date

    save_dice(die, False)

def delete_dice():
    """
    Delete die from list
    """
    dice = read_dice()
    count = 0

    for die in dice:
        print(f'[{count}] : {die[NAME_INDEX]}')
        count += 1

    user_input = int(input('Which die would you like to delete? '))
    die = dice[user_input]

    print()
    sure = input('Are you sure you want to delete this die? This action cannot be undone. (Y/N): ')
    print()

    if(sure.lower() == 'y'):
        save_dice(die, delete=True)



def print_dice():
    """
    Get dice from database, print them out to console
    """
    dice = read_dice()

    print("{:<40}{:<40}{:<40}{:<40}{:<40}{:<40}{:<40}".format("Dice Name"," | Dice Description"," | Dice Created Date"," | Resin Used"," | Demold Date", " | Full Cure Date", " | Tumbler Date"))
    print("{:<40}{:<40}{:<40}{:<40}{:<40}{:<40}{:<40}".format("-"*15,"-"*25,"-"*25,"-"*15,"-"*15,"-"*15,"-"*15))

    for die in dice:
        dice_name = die[NAME_INDEX]
        dice_desc = die[DESC_INDEX]
        dice_date = die[DATE_INDEX]
        dice_resin = die[RESIN_INDEX]
        dice_demold = die[READ_DEMOLD_INDEX]
        if datetime.datetime.now() > datetime.datetime.strptime(dice_demold, '%Y-%m-%d'):
            dice_demold = "\033[95m" + dice_demold + "\033[0m"
        dice_cure = die[CURE_INDEX]
        dice_tumbler = die[TUMBLER_INDEX]
        if dice_tumbler:
            dice_tumbler_date = die[TUMBLER_DATE_INDEX]
            if datetime.datetime.now() > datetime.datetime.strptime(dice_tumbler_date, '%Y-%m-%d'):
                dice_tumbler_date = "\033[95m" + dice_tumbler_date + "\033[0m"
        else:
            dice_tumbler_date = 'Not yet ready'

        print(f'{dice_name:<40} | {dice_desc:<37} | {dice_date:<37} | {dice_resin:<37} | {dice_demold:<37} | {dice_cure:<45} | {dice_tumbler_date:<45}')

    # To remove clutter from the Menu:
    input('\nPress Enter to continue...')

def read_dice():
    """
    Read dice from the database, return compound list of dice
    """
    dice = []
    diceRef = db.reference('Database reference/dice')
    snapshot = diceRef.order_by_key().get()
    for key, value in snapshot.items():
        jsonDie = json.loads(value)
        die = [key]
        for x in jsonDie:
            die.append(jsonDie[x])
        dice.append(die)
    
    return dice

def choose_option():
    """
    Function to get user input and choose which option they would like to perform.
    """
    print("""Menu:
    'C': Create new dice
    'R': View existing dice
    'U': Update existing dice
    'D': Delete dice
    'E': Exit program""")
    user_input = input(': ')

    # Create new dice
    if(user_input).lower() == 'c':
        create_dice()

    # Read existing dice from file
    elif(user_input).lower() == 'r':
        print_dice()

    # Update dice from the file
    elif(user_input).lower() == 'u':
        update_dice()

    # Delete dice from the file
    elif(user_input).lower() == 'd':
        delete_dice()

    # Exit program
    elif(user_input).lower() == 'e':
        exit()
    else:
        print('Unknown command. Please run program again.')

if __name__ == '__main__':
    main()