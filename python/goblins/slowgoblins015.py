"""part of http://ThePythonGameBook.com
source code:

https://github.com/horstjens/ThePythonGameBook/blob/master/
python/goblins/slowgoblins015.py

draw, draw-statistic, re-rolls (recursion), better strike

"""
__license__ = 'gpl3'  # see http://www.gnu.org/licenses/gpl.html'

import random


class Goblin(object):
    """generic goblin with randomized stat values"""

    #counter = 0 # this is a class attribute

    def __init__(self, name="anonymous goblin"):
        """creates a new goblin instance"""
        self.name = name
        self.attack = random.gauss(10, 2)  # float value
        self.defense = random.gauss(10, 2)  # float value
        self.hitpoints = random.gauss(20, 3)  # float value
        self.fullhealth = self.hitpoints  # copy
        self.defense_penalty = 0
        #statistics
        self.damage_dealt = 0
        self.damage_received = 0
        self.wins = 0

    def restore_health(self):
        """restore original hitpoints"""
        self.hitpoints = self.fullhealth

    def report(self):
        """returns a string with the actual stats"""
        text = ""
        for stat in filter(lambda x: "__" not in x, dir(self)):
            if "bound method" in str(self.__getattribute__(stat)):
                continue  # ignore methods, only take attributes
            #print(stat)
            attr = self.__getattribute__(stat)
            #testing if attribute is string or int or float
            if isinstance(attr, int) or isinstance(attr, float):
                text += "\n{:>20}: {:5.1f}".format(stat, attr)
            else:
                text += "\n{:>20}: {}".format(stat, attr)

        return text


def reroll(min_eyes, max_eyes, depth=1, max_depth=9999):
    """a die that is allowed to re-roll when the max_eyes is thrown.
       return the sum of all throws minus 1 per max_eyes thrown.
       This allows very high results with a very small propability


    examples:
    standard (1-6) die throws a 5:
       result: 5
    standard (1-6) die throws a 6:
       allowed to re-roll: throws a 1:
       result: (6-1)+1=6
    standard (1-6) die throws a 6:
       allowed to re-roll: throws a 2:
       result: (6-1)+2 ) 7
    standard (1-6) die throws a 6:
       allowed to re-roll: throws another 6:
       allowed to re-roll again: throws a 4:
       result: (6-1) + (6-1) + 4 = 5+5+4 =14
    """
    if depth >= max_depth:
        return max_eyes  # avoid endless loop
    result = random.randint(min_eyes, max_eyes)
    if result == max_eyes:
        result = result - 1 + reroll(min_eyes, max_eyes, depth + 1)  # recursion !
    return result


def sign(a, b):
    """compares a with b and returns a "<","=" or ">" sign """
    if a < b:
        return "<"
    elif a > b:
        return ">"
    else:
        return "="


def integer_input(min_value, max_value, prompt=">", default=-1):
    """ask and returns an integer between min_value and max_value"""
    choice = -1
    while choice < min_value or choice > max_value:
        char = input(prompt)
        if char == "":
            char = str(default)
        if char.isdigit():
            if not (min_value <= int(char) <= max_value):
                print("valid between (incl.) {} and {}".format(min_value, max_value))
            choice = int(char)
        else:
            print("please enter numbers only")
    return choice


def float_input(prompt=">", default=0):
    """ask and returns an float value from the user"""
    answer_ok = False
    while not answer_ok:
        answer = input(prompt)
        if answer == "":
            return default
        try:
            newvalue = float(answer)
            answer_ok = True
        except ValueError:
            print("integer or float with decimal point please")
    return newvalue


def mainmenu(maxnumber=4):
    print("welcome")
    print("1... compare Goblins")
    print("2... modify Stinky")
    print("3... modify Grunty")
    print("4... fight many battles")
    print("0... quit")
    return integer_input(0, 4, "your choice?>")


def compareValues(a, b):
    """returns a string with a table comparing the values of
       hp, attack, defense of a and b"""
    text = "\n          Stinky | vs. | Grunty "
    text += "\n ----------------+-----+-----------"
    text += "\n hitpoints: {:>4.1f} |  {}  | {:>4.1f}".format(a.hitpoints, sign(a.hitpoints, b.hitpoints), b.hitpoints)
    text += "\n attack:    {:>4.1f} |  {}  | {:>4.1f}".format(a.attack, sign(a.attack, b.attack), b.attack)
    text += "\n defense:   {:>4.1f} |  {}  | {:>4.1f}".format(a.defense, sign(a.defense, b.defense), b.defense)
    text += "\n"
    return text


def output(battle, combatround, a, b):
    """returns a string with battle, round and hitpoints"""
    text = "\n---battle {:3d} round {:3d}".format(battle, combatround)
    text += "--- Stinky: {:.0f} Grunty: {:.0f}".format(a.hitpoints, b.hitpoints)
    return text


def strike(attacker, defender, counterstrike=False):
    """attacker strikes at defender. The function changes the new
    hitpoints of the defender and returns a text String with the
    combat report.
    counterstrike (boolean) indicates that this is a counterattack
    or not."""
    if counterstrike:
        t = "counterattack"
    else:
        t = "attack"
    rollAtt = reroll(1, 6)  # allowed to re-roll if a 6 is thrown
    rollDef = reroll(1, 6)
    scoreA = attacker.attack + rollAtt
    scoreD = defender.defense + rollDef
    striketext = "{} rolls {}, {} rolls {}".format(attacker.name, rollAtt, defender.name, rollDef)
    if scoreA > scoreD:
        striketext += "\nSucessfull {0} !  ({1:.2f} > {2:.2f})".format(t, scoreA, scoreD)
        damage = scoreA - scoreD
        defender.hitpoints -= damage
        #statistics
        attacker.damage_dealt += damage
        defender.damage_received += damage
        striketext += "...doing {0:.2f} damage.".format(damage)
    else:
        striketext = "The {0} failed... ({1:.2f} <= {2:.2f})".format(t, scoreA, scoreD)
    return striketext


def game(stinky, grunty):
    """the Goblin Dice Duel game main function"""
    # ask how many battles
    battles = integer_input(1, 1000000, "fight how many battles ? (ENTER = 100)", 100)
    maxrounds = integer_input(1, 1000, "max rounds per battle ? (ENTER = 30)", 30)
    text = ""
    text += "\n --- Goblin Dice Duel ---\n\n"
    text += compareValues(stinky, grunty)
    text += "\n *** TOURNAMENT START ***"
    # reset wins
    stinky.wins = 0
    grunty.wins = 0
    # fight !
    for x in range(1, battles + 1):
        combatround = 0  # reset combatround for this battle
        text += "\n\n\n-BATTLE {} STARTS NOW".format(x)
        text += "\n\n-GET READY\n\n-FIGHT!!\n\n"
        #------------BATTLE------------
        while (stinky.hitpoints > 0 and grunty.hitpoints > 0 and combatround < maxrounds):
            combatround += 1
            text += output(x, combatround, stinky, grunty)
            # find out who strikes first
            (attacker, defender) = random.choice([(stinky, grunty), (grunty, stinky)])
            text += "\n{} strikes first: ".format(attacker.name)
            text += strike(attacker, defender, False)
            if defender.hitpoints > 0:
                text += "\nCounterstrike of {}: ".format(defender.name)
                text += strike(defender, attacker, True)
        # output of final strike
        text += output(x, combatround, stinky, grunty)
        text += "\nThis battle is over"
        if (combatround >= maxrounds and stinky.hitpoints > 0 and grunty.hitpoints > 0):
            text += " because exceeding {} rounds".format(maxrounds)
            text += "\nNobody wins"
        elif stinky.hitpoints > grunty.hitpoints:
            stinky.wins += 1
            text += "\nStinky wins battle {}".format(x)
        elif grunty.hitpoints > stinky.hitpoints:
            grunty.wins += 1
            text += "\nGrunty wins battle {}".format(x)
        # heal to full health after one battle
        #restore original hitpoints
        stinky.restore_health()
        grunty.restore_health()
    # statistic after end of all fights
    text += "\n\n*** statistics: ***\n\n"
    text += "                          ø DMG | ø DMG   "
    text += "\nVictories in %   | Wins | dealt | received"
    text += "\n-----------------+------+-------+--------"
    text += "\n  "
    text += "Stinky  {:5.1f}% | {:4.0f} | {:5.1f} | {:5.1f}".format(stinky.wins / (x / 100), stinky.wins, stinky.damage_dealt / x, stinky.damage_received / x)
    text += "\n  "
    text += "Grunty  {:5.1f}% | {:4.0f} | {:5.1f} | {:5.1f} ".format(grunty.wins / (x / 100), grunty.wins, grunty.damage_dealt / x, grunty.damage_received / x)
    text += "\n-----------------+------+-------+--------"
    text += "\nDraws:    {:5.1f}% | {:4.0f} |       |".format(100 * (battles - stinky.wins - grunty.wins) / battles, battles - stinky.wins - grunty.wins)
    #text += "\n-----------------+------+-------+--------"
    text += "\n" + compareValues(stinky, grunty)
    text += "==============================================="

    print(text)

    # output into logfile
    try:
        with open('combatlog.txt', 'a') as logfile:
            logfile.write(text)
        print("combat results appended into file 'combatlog.txt'")
    except:
        print("problem with file combatlog.txt")


def edit(goblin, modlist):
    """let the user change att, def and hp of a goblin"""
    print("all stats of {}:".format(goblin.name))
    print(goblin.report())
    print("\n edit some stats for {}:".format(goblin.name))

    for mystat in modlist:
        print("The current value of {} is {}".format(mystat, goblin.__getattribute__(mystat)))
        newvalue = float_input("new value ? [Enter=accept]>", goblin.__getattribute__(mystat))
        goblin.__setattr__(mystat, newvalue)  # set new value
        if mystat == "hitpoints":
            goblin.__setattr__("fullhealth", newvalue)  # copy hp
    print("thank you for editing this goblin")


if __name__ == "__main__":
    stinky = Goblin("Stinky")
    grunty = Goblin("Grunty")
    editlist = ["attack", "defense", "hitpoints"]  # moddable stats
    battles = 100
    while True:
        c = mainmenu(battles)
        if c == 0:
            break
        elif c == 1:
            print(compareValues(stinky, grunty))
        elif c == 2:
            edit(stinky, editlist)
        elif c == 3:
            edit(grunty, editlist)
        elif c == 4:
            game(stinky, grunty)
    print("bye-bye")
