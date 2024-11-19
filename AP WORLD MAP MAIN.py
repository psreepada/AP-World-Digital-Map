import pandas as pd
from tabulate import tabulate as tb
import time
from colorama import Fore, Back, Style
import searoute as sr
import random

dataset = pd.read_csv('AP_WORLD_MAP_DATA.csv')
loc = dataset.iloc[:, 0].values
long = dataset.iloc[:, 3].values
lat = dataset.iloc[:, 2].values
header = ["Location", "Port Name", "Port Latitude", "Port Longitude"]
locats = []
val = False
shipDat = pd.read_csv('Ship_Data.csv')
head = ["Name", "Avg speed (km/h)", "Max Payload (tons)"]
shipType = shipDat.iloc[:, 0].values
curlist = [0,0] # index 0 - latitude, index 1 - longitude
cho = [True, False]
maxload = shipDat.iloc[:, 2].values
allLoads = []
allTypes = []
ammunition = [] #Even though it is a list it must contain only 1 value

def color(val, num):
    if num == 0:
        var = input(Fore.YELLOW + val + Fore.GREEN).capitalize()
    if num == 1:
        var = input(Fore.YELLOW + val + Fore.GREEN).lower()
    return var

for x in shipType:
    allTypes.append(x)
    
for x in maxload:
    allLoads.append(x)

def PirateShip():
    ship = random.choice(allTypes)
    shipind = allTypes.index(ship)
    pirates = random.choice(cho)
    pirload = allLoads[shipind]
    piramo = random.randint(0, pirload)
    if pirates == True:
        print("Oh no!")
        print("Pirates are attacking your ship!")
        dec = color("Would you like to defend? (yes/no)\n", 1)
        if dec == "yes":
            if ammunition[0] > 0:
                print(Fore.WHITE + "Using your ammunition to defend...")
                time.sleep(3)
                if ammunition[0] > piramo:
                    print("Congratulations! You won.")
                else:
                    print("Oh no!")
                    print("The pirates won. Your ship is sabotaged.")
                    exit()
        else:
            print("The pirates sabotaged your ship.")
            exit()

def nav(long1, lat1, long2, lat2):
    org = (long1, lat1)
    des = (long2, lat2)
    route = sr.searoute(org, des)
    response = "{:.1f} {}".format(route.properties['length'], route.properties['units'])
    return response

def main(val):
    if val == True:
        in_loc = color("Please re-enter the name of the empire that you would like to visit from the list above: ", 0)
    if val == False:
        print(Fore.WHITE + f"Current Longitude: {curlist[1]}")
        print(Fore.WHITE + f"Current Latitude: {curlist[0]}")
        in_loc = color("Please enter the name of the empire that you would like to visit from the list above: ", 0)
    for x in loc:
        locats.append(x)
    while in_loc not in loc:
        print(Fore.RED + "Please try again. That empire is not in the map.")
        in_loc = color("Please enter the name of the empire that you would like to visit from the list above: ", 0)
    ind = locats.index(in_loc)
    tar_des = loc[ind]
    tar_lat = lat[ind]
    tar_long = long[ind]
    print(Fore.WHITE + f"Destination Longitude: {tar_long}")
    print(Fore.WHITE + f"Destination Latitude: {tar_lat}")
    confirm = color(f"Please confirm your targeted destination (yes/no): {tar_des.capitalize()} Empire\n", 1)
    choice(confirm, ind)

def choice(confirm, ind):
    if confirm == "yes":
        distance = nav(curlist[1], curlist[0], long[ind], lat[ind])
        print(Fore.LIGHTBLUE_EX + tb(shipDat.iloc[:, :].values, headers=head, tablefmt="fancy_grid"))
        Type = color("Choose which sail you want to sail in: ", 0)
        while Type not in shipType:
            print(Fore.RED + "Please select a valid option")
            Type = color("Choose which sail you want to sail in: ", 0)
        load = int(input(Fore.YELLOW + "Enter your total payload in tons (Please just enter the integer value only): " + Fore.GREEN))
        mainInd = allTypes.index(Type)
        Cont = True
        while allLoads[mainInd] < load and Cont:
            print(Fore.RED + "Your choosen ship type cannot withstand that amount of cargo.")
            print(f"Your choosen ship type: {Type}")
            print(f"The max payload of your ship: {allLoads[mainInd]}")
            print(f"The amount of payload you want in your ship: {load}")
            extra = abs(allLoads[mainInd] - load)
            print(f"The amount of extra cargo you want in your ship is: {extra} tons")
            print("The extra amount will automatically removed and is prevented to be on this ship. The only way you can take this extra cargo with you is if you decide to choose another type of ship.")
            dec = color("Do you want to choose another ship? (yes/no)\n", 1)
            if dec == "yes":
                Type = color("Choose which sail you want to sail in: ", 0)
                while Type not in shipType:
                    print(Fore.RED + "Please select a valid option")
                    Type = color("Choose which sail you want to sail in: ", 0)
                load = int(input(Fore.YELLOW + "Enter your total payload in tons (Please just enter the integer value only): " + Fore.GREEN))
                mainInd = allTypes.index(Type)
            if dec == "no":
                print(Fore.WHITE + "Ok then. The excess cargo is removed.")
                print(f"Your current amount of cargo in the ship: {allLoads[mainInd]} tons")
                load = load - extra
                Cont = False
        amo = int(input(Fore.YELLOW + f"How much of the {load} tons is ammunition or gunpowder? (Enter the integer value only)\n" + Fore.GREEN))
        while amo > load:
            print(Fore.RED + f"The total amount of cargo you are bringing is {load} tons, while the total ammunition your bringing is {amo} tons")
            print("Your total amount of ammunition must be lower than your total amount of cargo.")
            print("Please try again.")
            amo = int(input(Fore.YELLOW + f"How much of the {load} tons is ammunition or gunpowder? (Enter the integer value only)\n" + Fore.GREEN))
        ammunition.append(amo)
        print(Fore.WHITE + f"Travel distance: {distance}")
        print(Fore.WHITE + "Travelling to your destination...")
        time.sleep(3)
        PirateShip()
        curlist[0] = lat[ind]
        curlist[1] = long[ind]
        print(Fore.YELLOW + "You have arrived at your destination!")
        print(Fore.WHITE + f"Current longitude: {curlist[1]}")
        print(Fore.WHITE + f"Current latitude: {curlist[0]}")
        
    if confirm == "no":
        val = True
        main(val)

print(Fore.GREEN + "Hello there merchant! Welcome to the world map!")
print(Fore.CYAN + tb(dataset.iloc[:, :].values, headers=header, tablefmt="fancy_grid"))
main(val)

while True:
    again = color("Would you like to travel to another destination? (yes/no)\n", 1)
    if again == "yes":
        print(Fore.CYAN + tb(dataset.iloc[:, :].values, headers=header, tablefmt="fancy_grid"))
        main(val)
    else:
        exit()