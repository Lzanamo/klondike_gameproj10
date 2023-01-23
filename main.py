from cards import Card, Deck

###########################################################
#  Computer Project #10
#
#  Working on Class
#    Prompts the user for a chioce to make on the board
#   Based on that choice calls the correct function to make the move
#    The functions work by calling methods from the classes in the cards.py
###########################################################

MENU = '''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    TT s d: Move card from end of Tableau pile s to end of pile d.
    TF s d: Move card from end of Tableau pile s to Foundation d.
    WT d: Move card from Waste to Tableau pile d.
    WF d: Move card from Waste to Foundation pile d.
    SW : Move card from Stock to Waste.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''


def initialize():
    '''Inilalizes the stock to Deck class and deals the card to appropriate places'''
    # Makes stock an instance of Deck and shuffle the stock
    stock = Deck()
    stock.shuffle()
    # makes the wast, foundation, and tableau list
    waste = []
    foundation = [[], [], [], []]
    tableau = [[], [], [], [], [], [], []]
    # deals the cards from the stock to the table row by row
    for row in range(0, 7):
        for colume in range(row, 7):
            tableau[colume].append(stock.deal())
    # loops through the tableau and flips any card that are not upside down execpt the last one in each row
    for line in tableau:
        for item in line:
            if item.is_face_up() == True:
                item.flip_card()
            line[-1].flip_card()

    waste.append(stock.deal())
    return tableau, stock, foundation, waste


def display(tableau, stock, foundation, waste):
    """ display the game setup """
    stock_top_card = "empty"
    found_top_cards = ["empty", "empty", "empty", "empty"]
    waste_top_card = "empty"
    if len(waste):
        waste_top_card = waste[-1]
    if len(stock):
        stock_top_card = "XX"  # stock[-1]
    for i in range(4):
        if len(foundation[i]):
            found_top_cards[i] = foundation[i][-1]
    print()
    print("{:5s} {:5s} \t\t\t\t\t {}".format("stock", "waste", "foundation"))
    print("\t\t\t\t     ", end='')
    for i in range(4):
        print(" {:5d} ".format(i + 1), end='')
    print()
    print("{:5s} {:5s} \t\t\t\t".format(str(stock_top_card), str(waste_top_card)), end="")
    for i in found_top_cards:
        print(" {:5s} ".format(str(i)), end="")
    print()
    print()
    print()
    print()
    print("\t\t\t\t\t{}".format("tableau"))
    print("\t\t ", end='')
    for i in range(7):
        print(" {:5d} ".format(i + 1), end='')
    print()
    # calculate length of longest tableau column
    max_length = max([len(stack) for stack in tableau])
    for i in range(max_length):
        print("\t\t    ", end='')
        for tab_list in tableau:
            # print card if it exists, else print blank
            try:
                print(" {:5s} ".format(str(tab_list[i])), end='')
            except IndexError:
                print(" {:5s} ".format(''), end='')
        print()
    print()


def stock_to_waste(stock, waste):
    '''Flips one card from the stock to the waste'''
    if stock.is_empty() == True:  # checks if the stock is empty
        return False
    else:
        # if the stock is not empty, it deals one card to the waste
        waste.append(stock.deal())
        return True


def waste_to_tableau(waste, tableau, t_num):
    ''' Takes the last card from the waste to the tableau if its a rank below and opposite color'''
    card1 = waste[-1]
    if len(tableau[
               t_num]) == 0 and card1.rank() == 13:  # Checks if the tableau colume is empty and if the card being moved it a king with rank 13
        moving = waste.pop()  # gets the card from the was
        tableau[t_num].append(moving)  # adds it to the right colume in the tableau
        return True
    elif len(tableau[t_num]) != 0:
        card2 = tableau[t_num][-1]
        wanted_rank = card2.rank() - 1
        # checks if the card from the waste is black and the tableau card is red with the correct rank
        if card1.suit() in [1, 4] and card2.suit() in [2, 3] and card1.rank() == wanted_rank:
            moving = waste.pop()
            tableau[t_num].append(moving)
            return True
        # checks if the card from the waste is red and the tableau card is black with the correct rank
        elif card1.suit() in [2, 3] and card2.suit() in [1, 4] and card1.rank() == wanted_rank:
            moving = waste.pop()
            tableau[t_num].append(moving)
            return True
        else:
            return False
    else:
        return False


def waste_to_foundation(waste, foundation, f_num):
    '''Adds the last card from the waste to the foundation if they are the same suit and the card from the waste is one rank above the one in the foundation'''
    card = waste[-1]
    if len(foundation[f_num]) != 0:  # Checks if the slot in the foundation is not empty
        fund_card = foundation[f_num][-1]
        wanted_rank = fund_card.rank() + 1  # gets the wanted rank
        if card.rank() == wanted_rank and card.suit() == fund_card.suit():  # checks if the rank is the one we want and if the suits are the same
            # Pops the card and adds it to the foundation slot
            moving = waste.pop()
            foundation[f_num].append(moving)
            return True
        else:
            return False
    elif len(foundation[
                 f_num]) == 0 and card.rank() == 1:  # checks if the slot int he foundation is empty and the card moving is an Ace
        # Pops the card and adds it to the foundation slot
        moving = waste.pop()
        foundation[f_num].append(moving)
        return True
    else:
        return False


def tableau_to_foundation(tableau, foundation, t_num, f_num):
    '''Docstring'''
    card = tableau[t_num][-1]
    # if the foundation slot is not empty checks the rank and suit of both the card in the tableau and foundation
    if len(foundation[f_num]) != 0:
        fund_card = foundation[f_num][-1]
        wanted_rank = fund_card.rank() + 1
        # Checks if the tableau card is the right rank and same suit with the foundation card
        if card.rank() == wanted_rank and card.suit() == fund_card.suit():
            moving = tableau[t_num].pop()
            foundation[f_num].append(moving)
            # check if the last card in tableau is fliped up
            if tableau[t_num]:
                if tableau[t_num][-1].is_face_up() != True:
                    tableau[t_num][-1].flip_card()
            return True
        else:
            return False
    elif len(foundation[f_num]) == 0 and card.rank() == 1:
        moving = tableau[t_num].pop()
        foundation[f_num].append(moving)
        # check if the last card in tableau is fliped up
        if tableau[t_num]:
            if tableau[t_num][-1].is_face_up() != True:
                tableau[t_num][-1].flip_card()
        return True
    else:
        return False


def tableau_to_tableau(tableau, t_num1, t_num2):
    '''Docstring'''
    card1 = tableau[t_num1][-1]
    # Check is the tableau destination is empty and the card being moved is a king
    if len(tableau[t_num2]) == 0 and card1.rank() == 13:
        moving = tableau[t_num1].pop()
        tableau[t_num2].append(moving)
        # check if the last card in tableau is fliped up
        if tableau[t_num1]:
            if tableau[t_num1][-1].is_face_up() != True:
                tableau[t_num1][-1].flip_card()
        return True
    elif len(tableau[t_num2]) != 0:
        card2 = tableau[t_num2][-1]
        wanted_rank = card2.rank() - 1
        # Checks if the card bieng moved is black and the other one is red, also checks the rank
        if card1.suit() in [1, 4] and card2.suit() in [2, 3] and card1.rank() == wanted_rank:
            moving = tableau[t_num1].pop()
            tableau[t_num2].append(moving)
            # check if the last card in tableau is fliped up
            if tableau[t_num1]:
                if tableau[t_num1][-1].is_face_up() != True:
                    tableau[t_num1][-1].flip_card()
            return True
        # Checks if the card bieng moved is red and the other one is black, also checks the rank
        elif card1.suit() in [2, 3] and card2.suit() in [1, 4] and card1.rank() == wanted_rank:
            moving = tableau[t_num1].pop()
            tableau[t_num2].append(moving)
            # check if the last card in tableau is fliped up
            if tableau[t_num1]:
                if tableau[t_num1][-1].is_face_up() != True:
                    tableau[t_num1][-1].flip_card()

            return True
        else:
            return False
    else:
        return False


def check_win(stock, waste, foundation, tableau):
    '''Docstring'''
    # finds out if the the sum of cards int eh foundation
    found_sum = 0
    for line in foundation:
        found_sum += len(line)

    # finds out the sum of the cards in the tableau
    tab_sum = 0
    for item in tableau:
        tab_sum += len(item)

    # if the foundation has all 52 cards and the waste,stock and tableau are empty it returns true
    if found_sum == 52 and len(stock) == 0 and len(waste) == 0 and tab_sum == 0:
        return True
    else:
        return False


def parse_option(in_str):
    '''Prompt the user for an option and check that the input has the
           form requested in the menu, printing an error message, if not.
           Return:
        TT s d: Move card from end of Tableau pile s to end of pile d.
        TF s d: Move card from end of Tableau pile s to Foundation d.
        WT d: Move card from Waste to Tableau pile d.
        WF d: Move card from Waste to Foundation pile d.
        SW : Move card from Stock to Waste.
        R: Restart the game (after shuffling)
        H: Display this menu of choices
        Q: Quit the game
        '''
    option_list = in_str.strip().split()

    opt_char = option_list[0][0].upper()

    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'S' and len(option_list) == 1:
        if option_list[0].upper() == 'SW':
            return ['SW']

    if opt_char == 'W' and len(option_list) == 2:
        if option_list[0].upper() == 'WT' or option_list[0].upper() == 'WF':
            dest = option_list[1]
            if dest.isdigit():
                dest = int(dest)
                if option_list[0].upper() == 'WT' and (dest < 1 or dest > 7):
                    print("\nError in Destination")
                    return None
                if option_list[0].upper() == 'WF' and (dest < 1 or dest > 4):
                    print("\nError in Destination")
                    return None
                opt_str = option_list[0].strip().upper()
                return [opt_str, dest]

    if opt_char == 'T' and len(option_list) == 3 and option_list[1].isdigit() \
            and option_list[2].isdigit():
        opt_str = option_list[0].strip().upper()
        if opt_str in ['TT', 'TF']:
            source = int(option_list[1])
            dest = int(option_list[2])
            # check for valid source values
            if opt_str in ['TT', 'TF'] and (source < 1 or source > 7):
                print("\nError in Source.")
                return None
            # elif opt_str == 'MFT' and (source < 0 or source > 3):
            # print("Error in Source.")
            # return None
            # source values are valid
            # check for valid destination values
            if (opt_str == 'TT' and (dest < 1 or dest > 7)) \
                    or (opt_str == 'TF' and (dest < 1 or dest > 4)):
                print("\nError in Destination")
                return None
            return [opt_str, source, dest]

    print("\nError in option:", in_str)
    return None  # none of the above


def Prompt_check(tableau, stock, foundation, waste):
    '''Prompts the user for a choice and evalutes the choice before returning it'''
    user_ppt = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")  # prompts the user for a choice
    while True:
        checked = parse_option(user_ppt)  # calls parse_option to error check the input
        if checked == None:  # if the result from calling parse_option is None, it re-prompts
            display(tableau, stock, foundation, waste)
            user_ppt = input("\nInput an option (TT,TF,WT,WF,SW,R,H,Q): ")
        else:
            return checked


def main():
    # calls the initialize function
    tableau, stock, foundation, waste = initialize()

    # prints the MENU and desplays the board
    print(MENU)
    display(tableau, stock, foundation, waste)

    # calls the prompt_check to prompt for a choice and check it
    checked = Prompt_check(tableau, stock, foundation, waste)

    while checked:
        if checked[0] == "TT":
            # if the input was TT, calls the tableau_to_tableau function
            result = tableau_to_tableau(tableau, checked[1] - 1, checked[2] - 1)
            if result == True:  # if the return by the function was True then the move was valid
                display(tableau, stock, foundation, waste)  # displays board
            else:
                # prints error message and displays board
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)

            # calls the prompt_check to prompt for a choice and check it
            checked = Prompt_check(tableau, stock, foundation, waste)
        elif checked[0] == "TF":
            # if the input was TF, tableau_to_foundation is called
            result = tableau_to_foundation(tableau, foundation, checked[1] - 1, checked[2] - 1)
            if result == True:
                win_check = check_win(stock, waste, foundation, tableau)
                if win_check == True:
                    print("You won!")
                    display(tableau, stock, foundation, waste)
                    quit()
                else:
                    display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)

            checked = Prompt_check(tableau, stock, foundation, waste)
        elif checked[0] == "WT":
            # if the input was WT, waste_to_tableau is called
            result = waste_to_tableau(waste, tableau, checked[1] - 1)
            if result == True:
                # if move was valid, displays board
                display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)

            checked = Prompt_check(tableau, stock, foundation, waste)
        elif checked[0] == "WF":
            # if input was WF, waste_to_foundation is called
            result = waste_to_foundation(waste, foundation, checked[1] - 1)
            if result == True:
                win_check = check_win(stock, waste, foundation, tableau)  # checks it is a win
                if win_check == True:
                    print("You won!")
                    display(tableau, stock, foundation, waste)
                    quit()
                else:  # if its not a win displays board only
                    display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)

            checked = Prompt_check(tableau, stock, foundation, waste)
        elif checked[0] == "SW":
            # if input is SW, stock_to_waste is called
            result = stock_to_waste(stock, waste)
            if result == True:
                display(tableau, stock, foundation, waste)
            else:
                print("\nInvalid move!\n")
                display(tableau, stock, foundation, waste)

            checked = Prompt_check(tableau, stock, foundation, waste)
        elif checked[0] == "H":  # displays MENU if input is H
            print(MENU)
            checked = Prompt_check(tableau, stock, foundation, waste)
        elif checked[0] == "R":
            stock.shuffle()  # Shuffles the deck
            tableau, stock, foundation, waste = initialize()  # calls the initialize function
            print(MENU)
            display(tableau, stock, foundation, waste)
            checked = Prompt_check(tableau, stock, foundation, waste)
        else:
            break


if __name__ == '__main__':
    main()

