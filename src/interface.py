from main import *
from termcolor import colored
import sys
from random import randrange

colors = ["green", "blue", "yellow", "red", "cyan"]

def banner():
    """
    functie voor de banner
    :return
    """
    print(colored('''
        @=====================================================================@

         ██▀███  ▓█████  ▄████▄   ▄████▄   ▒█████   ███▄ ▄███▓▓█████  ███▄    █
        ▓██ ▒ ██▒▓█   ▀ ▒██▀ ▀█  ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀  ██ ▀█   █
        ▓██ ░▄█ ▒▒███   ▒▓█    ▄ ▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▒███   ▓██  ▀█ ██▒
        ▒██▀▀█▄  ▒▓█  ▄ ▒▓▓▄ ▄██▒▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒▓█  ▄ ▓██▒  ▐▌██▒
        ░██▓ ▒██▒░▒████▒▒ ▓███▀ ░▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒░▒████▒▒██░   ▓██░
        ░ ▒▓ ░▒▓░░░ ▒░ ░░ ░▒ ▒  ░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░░ ▒░   ▒ ▒
          ░▒ ░ ▒░ ░ ░  ░  ░  ▒     ░  ▒     ░ ▒ ▒░ ░  ░      ░ ░ ░  ░░ ░░   ░ ▒░
          ░░   ░    ░   ░        ░        ░ ░ ░ ▒  ░      ░      ░      ░   ░ ░
           ░        ░  ░░ ░      ░ ░          ░ ░         ░      ░  ░         ░
                        ░        ░

        @=====================================================================@

        (made by Ceyhun Cakir)
    ''', colors[randrange(5)]))

def interface():
    """
    interface functie waar de gebruiker input kan hebben
    :return
    """

    banner()
    mysql_username = input(colored("\n\t" + "Geef je mysql username op: ", "yellow"))
    mysql_password = input(colored("\n\t" + "Geef je mysql password op: ", "yellow"))
    mysql_database = input(colored("\n\t" + "Geef je mysql database op: ", "yellow"))
    

    recommendation_engine(mysql_username, mysql_password, mysql_database)

interface()
