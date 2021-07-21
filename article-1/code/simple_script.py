actions = {'A': print, 'B': print, 'C': print}
choice = None
while not choice in actions.keys():
    choice = input('Choose one of [A, B, C] > ').upper()
result = actions[choice](f'You chose {choice}')
