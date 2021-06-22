import sys
from tkinter import *
import get
import config

if __name__ == "__main__":
    print('startup...')
    id:str = '~'
    inp:str
    search:str

    while True:
        print('*'*5,'CCP for AniList', '*'*5)
        print(' [1] Default post query ')
        print(' [2] Get anime with Id')
        print(' [3] Search for characters')
        print(' [4] Search for users')
        print(' [5] Exit')
        inp = input('  > ')
        if inp == '5':
            break
        elif inp == '1':
            print(config.formatJSON(get.postQuery()))
        elif inp == '2':
            while not id.isnumeric() and id != 'EXIT':
                id = input(' Enter a valid id or enter \'EXIT\' to exit\n  > ')
            if id != 'EXIT': print(config.formatJSON(get.getAnimeOBJ(id)))
        elif inp == '3':
            search = input(' Enter your search term\n Type \'EXIT\' to exit\n Type \'ID\' to get a specific character\n  > ' )
            if search == 'ID':
                while not id.isnumeric() and id != 'EXIT':
                    id = input(' Enter a valid id or enter \'EXIT\' to exit\n  > ')
                if id != 'EXIT': print(config.formatJSON(get.getCharacterPAGE(id)))
            if search != 'EXIT':
                page = 1
                while not inp == 'EXIT':
                    print(config.formatJSON(get.getCharacterPAGE(None, search, page, config.pull(1))))
                    inp = input(' \'EXIT\' to exit\n \'>\' for next page\n \'<\' for previous page\n  > ')
                    if inp == '>': page = page + 1
                    elif inp == '<': page = page - 1
        elif inp == '5' or inp == 'EXIT' or id == 'EXIT':
            print('Goodbye!')
            sys.exit(0)
    print('Exit Failure')
    sys.exit(1)
