import datetime as dt
import re

import requests
from lxml import html, etree
from lxml.html.clean import Cleaner

from ..models.Food import Food, Menu
from ..models.Location import Location

priceI = ["(Stud.)", "(Bed.)", "(Gäste)"]

regexFloat = re.compile(r"[-+]?\d*[,]\d+\s")

regexDate = re.compile(r"\d{1,2}\.\d{1,2}\.\d{2,4}")

regexTagContent = re.compile(r">.+<")
regexHref = re.compile(r"\?id=[^\"]+")

regexFoodBlock = re.compile(r"[AEV][a-z]+\s\d[^>]+>")
regexFoodCaption = re.compile(r"[AEV][a-z]+\s\d")

# funktioniert nicht wie er soll, erleichter dennoch die arbeit
# splittet den link aus gründen in seine bestandteile auf.
# das [-1]. element enhält eine datei also ¯\_(ツ)_/¯
regexLink = re.compile(r"(http(s)?://(([a-z.-]+)/)+([a-z-A-Z.?=0-9]+))")


class MensaWebSite:
    __iconDict = dict(veg="Ⓥ", V="🌱", R="🐮", G="🐓", W="🦌", F="🐟", S="🐖")
    __timeFormat = '%d.%m.%Y'
    __timePath = '//div[3]/h4/text()'

    def __init__(self):
        self.link = "http://www.werkswelt.de/"

    def get_locations(self) -> list:
        locations = []
        page = requests.get(self.link)
        tree = html.fromstring(page.text)
        tag = tree.xpath('//ul[@class="dropdown-menu"]')[7]
        c = Cleaner()
        c.allow_tags = 'a'
        c.remove_unknown_tags = False
        doc = etree.tostring(tag)
        for s in c.clean_html(doc).decode("utf-8").replace("<div>", "").replace("</div>", "").strip().split('\n'):
            locations.append(
                Location(regexTagContent.findall(s)[0].replace("<", "").replace(">", ""), regexHref.findall(s)[0]))

        return locations

    def get_menu(self, location: str) -> Menu:
        food = []
        c = Cleaner()
        c.allow_tags = ['img']
        c.remove_unknown_tags = False
        page = requests.get(self.link + location)
        tree = html.fromstring(page.text)
        f = tree.xpath('//div[@style="background-color:#ecf0f1;border-radius: 4px 4px 0px 0px; padding: 8px;"]')
        doc = etree.tostring(f[0], pretty_print=True)
        t = c.clean_html(doc).decode("utf-8").replace("<div>", "").replace("</div>", "")
        dtime = self.__extract_date(c.clean_html(doc)
                                    .decode("utf-8")
                                    .replace("<div>", "")
                                    .replace("</div>", "")
                                    .strip()
                                    .split("Essen "))
        food += self.__extract_food(regexFoodBlock.findall(t))
        #         foodList.append(f)
        return Menu(dtime, food)

    def __extract_date(self, input: list):
        dtime = None
        for j, g in enumerate(input):
            if j == 0:
                reg = regexDate.findall(g)
                if len(reg) > 0:
                    dtime = dt.datetime.strptime(reg[0], self.__timeFormat)
        return dtime

    def __extract_food(self, input: list) -> list:
        foodlist = []
        for j, g in enumerate(input):
            t = MensaWebSite.__split_prices_and_name(g)
            f = Food()
            f.caption = t[1][:regexFoodCaption.search(t[1]).end()]
            f.name = t[1][regexFoodCaption.search(t[1]).end():]
            try:
                f.priceStudent = t[0][0]
                f.priceStaff = t[0][1]
                f.priceVisitor = t[0][2]
            except IndexError:
                pass
            f.foodIcon = MensaWebSite.__get_food_kind(g, self.__iconDict)
            foodlist.append(f)
        return foodlist

    @staticmethod
    def __get_food_kind(input: str, icondict: dict) -> str:
        strli = ""
        for link in regexLink.findall(input):
            emoji = icondict.get(link[0].split("/")[-1].split(".")[0])
            if emoji is not None:
                strli += emoji
        return strli

    @staticmethod
    def __split_prices_and_name(input: str) -> (list, str):
        __doc__ = "Method tries to extract prices from input."
        fs = []
        for f in regexFloat.findall(input):
            fs.append(float(f.replace(",", ".")))
        if len(fs) > 1:
            reststr = input[:regexFloat.search(input).start()]
        else:
            reststr = input.split("-")[0]
        return fs, reststr


if __name__ == '__main__':
    m = MensaWebSite()
    for i in m.get_menu("?id=mohm").food:
        print(i)
