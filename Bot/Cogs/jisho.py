import requests
import bs4
import random
from discord.ext import commands
import json

link = "https://jisho.org/api/v1/search/words?keyword=yes"


def jisho_scrapper(link):
    r = requests.get(link)
    jisho_data = r.text
    jisho_parser = json.loads(jisho_data)
    print(jisho_parser)


jisho_scrapper(link)
