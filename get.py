""" 
A series of bite sized functions to wrap query posts to the AniList API 
 * postQuery(q, v): Post to the API with the given query and variables. Has built in response handling. Will return the json if posssible, otherwise will return the server
 reponse. Called upon by other functions
 * getAnimeOBJ(id): get the anime object with the given ID
 * getCharacterPAGE(id, search, page, perPage): get the character of a given id or return a list of characters corresponding to the search term. 
 * getUser(search, name, id, sort): get the user of a given id or retrun a list of users correspoding to the search term. sort is limited to the UserSort enums
 * writeToSpreadSheet(info): log info [deprecated]
 """

import os
import subprocess
import sys
from enum import Enum
import unittest
import requests
from requests.api import request

faultyQuery = '{syntaxError}'

class UserSort(Enum):
    ID = 'ID'
    ID_DESC = 'ID_DESC'
    USERNAME = 'USERNAME'
    USERNAME_DESC = 'USERNAME_DESC'
    WATCHED_TIME = 'WATCHED_TIME'
    WATCHED_TIME_DESC = 'WATCHED_TIME_DESC'
    CHAPTERS_READ = 'CHAPTERS_READ'
    CHAPTERS_READ_DESC = 'CHAPTERS_READ_DESC'
    SEARCH_MATCH = 'SEARCH_MATCH'
    DEFAULT = 'ID'

def postQuery(q:str = None, 
    v:dict = {
        'id' : 15125,
        'type' : 'ANIME' # 'ANIME' is hard coded into the query in every other scope.
    }) -> str:
    """ Universal post function with built in Response handling. Will return a json if available, otherwise will return the server's response. Default params are a 
    a get anime object query that returns Cowboy Bebop"""
    if q == None:
        q = '''query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: $type) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
                romaji
                english
                native
            }
        }
    }'''
    url = 'https://graphql.anilist.co'
    print('\npost initiated')
    # make the HTTP API request
    serverResponse = requests.post(url, json={'query':q, 'variables':v})
    try:
        serverResponse.raise_for_status()
    except requests.HTTPError:
        print('AniList raised an error')
    
    responseDict = {
        '<Response [200]>' : 'OK',
        '<Response [400]>' : 'BAD REQUEST',
        '<Response [404]>' : 'NOT FOUND',
        '<Response [405]>' : 'BAD METHOD',
        '<Response [500]>' : 'INTERNAL SERVER ERROR',
        '<Response [408]>' : 'REQUEST TIME OUT',
        '<Response [401]>' : 'UNAUTHORIZED'
    }
    if str(serverResponse) in responseDict:
        print(responseDict[str(serverResponse)])
        if str(serverResponse) == '<Response [200]>': return serverResponse.text
    else:
        print('The server returned an unexpected response:', str(serverResponse))
        return str(serverResponse)

def headQuery():
    pass

def optionsQuery():
    pass

def putQuery():
    pass

def getAnimeOBJ(id:int = 15125) -> str:
    #documented at https://anilist.gitbook.io/anilist-apiv2-docs/overview/graphql/getting-started
    print('formatting anime object query with ID:', id)
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
                romaji
                english
                native
            }
        }
    }'''
    variables = {
        'id' : id
    }
    return postQuery(query, variables)

def getCharacterPAGE(id:int = None, search:str = None, page:int = 1, perPage:int = 3) -> str:
    print('formatting character page query with ID:', id, ', search:', search, ', page:', page, ', and perPage:', perPage)
    query = '''
    query($id: Int, $page: Int, $perPage: Int, $search: String){
        Page(page: $page, perPage: $perPage){
            pageInfo{
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media(id: $id, search: $search){
                id
                title{
                    romaji
                    english
                }
            }
        }
    }
    '''
    variables = {
        'search': search,
        'page': page,
        'perPage': perPage
    }
    if id: variables['id'] = id
    if search: variables['search'] = search

    try:
        if not id and not search: raise SyntaxError
    except SyntaxError:
        print('at least one field, aside from \"page\" and \"perPage\", must be given')
        return faultyQuery
    return postQuery(query, variables)

def getUserPAGE(search:str = None, name:str = None, id:int = None, sort:str = 'DEFAULT') -> str:
    try:
        sort = UserSort[sort]
    except KeyError:
        print(sort, 'is not a valid member of UserSort, defaulted to',UserSort['DEFAULT'])
        sort = UserSort['DEFAULT']
    print('formating user query with search:', search, ', name:', name, ', id:', id, ', sort:', sort)
    query = '''
    query($id:Int, $name:String, $search:String, $sort:UserSort){
        User(id:$id, name:$name, search:$search, sort:$sort){
            id
            name
            about
            favourites
        }
    }
    '''
    variables = {
        'sort':str(sort)
    }
    if id:
        variables['id'] = id
    if name:
        variables['name'] = name
    if search:
        variables['search'] = search
    try:
        if not id and not name and not search: raise SyntaxError
    except SyntaxError:
        print('at least one attribute aside from \"sort\" must be given.')
        return faultyQuery
    else: return postQuery(query, variables)

class TestQuery(unittest.TestCase):
    def testGet(self):
        self.assertEqual(1,1)

if __name__ == "__main__":
    #print(getAnimeOBJ())
    #print(getCharacterPAGE(None, 'Dragon Ball Z Kai'))
    #print(postQuery())
    #print(getUserPAGE('Biz',))
    print(getAnimeOBJ(3972))
    
    
