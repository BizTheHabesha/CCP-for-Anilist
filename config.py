"""
A way to edit settings for the application. Config IDs are as follows: \n
1 - Items per page:
    Any valid integer
2 - Query Return Format:
    1 - Raw JSON \n
    2 - Formatted JSON \n
    3 - Formatted page \n
    4 - Spreadsheet format
3 - Output:
    1 - Spreadsheet (include file extension)
        10 - .xls (only extension planned for support) \n
        11 - .xlt \n
        12 - .xlm
    2 - Text file (.txt)
        20 - PDF of the query page \n
        21 - Raw JSON
4 - File location
    
"""

import sys
import os
import utils
import get

DEFAULTCONFIGFILE = 'config\\preferences.config'
currConfigFile = DEFAULTCONFIGFILE

def pull(configId):
    line = 1
    configFile = open(DEFAULTCONFIGFILE, 'r')
    configstr = configFile.read()
    for char in configstr:
        if char == '\n': line = line+1
        if line == configId and char.isnumeric():
            configFile.close()
            return char
    configFile.close()
    return '-1'

def push(configId:int, new:int):
    configId = str(configId)
    new = str(new)
    cppReturn = os.system("start config\push.exe config\preferences.config "+configId+" "+new)
    returnCODEX = {
        0 : 'OK',
        1 : 'Invalid Integer',
        2 : 'Invalid File Location',
        3 : 'The Configuration Does Not Exist',
        4 : 'The Configuaration File is at a Different Location',
        5 : 'Access Denied'
    }
    print("push returned", cppReturn)

def formatJSON(json:str) -> str:
    if json == None: return '{\nAn error occured}'
    final = ''
    fromPull = pull(2)

    if fromPull == 1:
        return str

    # TODO format into a multi-line JSON
    elif fromPull == 2 or fromPull == '2':
        #print('got json: ', json)
        indent = 0
        rmindent = False
        for char in json:
            final+=char
            if char == '{':
                indent = indent+1
                final+='\n'
                for i in range(indent): final+='  '
            if char == '}':
                rmindent == True
            if char == ',':
                final+='\n'
                for i in range(indent): final+='  '
                if rmindent:
                    indent = indent-1
                    rmindent = False
        return final

    # TODO format into a multi-line text-based format
    elif fromPull == 3:
        pass

if __name__ == "__main__":
    print('getting configs...')
    print('Default file location: '+DEFAULTCONFIGFILE)
    print('Formatted text from formatJSON():\n  ')
    print(formatJSON(get.getAnimeOBJ()))
    
