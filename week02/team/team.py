"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    # constructor
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.response = {}
        
    # run method
    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.response = response.json()
        else:
            print("Request failed:", self.url)
            self.data = False


class Deck:
    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52
        # self.deck = {}
        self.suit_map = {
            "SPADES": "💩",
            "DIAMONDS": "👌",
            "CLUBS": "🍀",
            "HEARTS": "💖",
        }
        self.number_map = {
            "2"    : "🅱 ",
            "3"    : "😎",
            "4"    : "😇",
            "5"    : "🤢",
            "6"    : "👻",
            "7"    : "🎶",
            "8"    : "(╯°□°）╯︵ ┻━┻)",
            "9"    : "🎂",
            "10"   : "🍰",
            "JACK" : "🎉",
            "QUEEN": "💋",
            "KING" : "🤴",
            "ACE"  : "🅰 ",
        }


    def reshuffle(self):
        # TODO - add call to reshuffle
        request = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        request.start()
        request.join()

    def draw_card(self):
        # TODO add call to get a card
        request = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/draw/')
        request.start()
        request.join()
        if request.response:
            self.remaining = request.response["remaining"]
            return self.number_map[request.response["cards"][0]["value"]] + " of " + self.suit_map[request.response["cards"][0]["suit"]]
        else:
            return "ERROR ಠ_ಠ"

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.cards_remaining() <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'rbrt6diczrvr'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<