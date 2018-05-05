import random
import argparse
from threading import Thread
from urllib import request

from bs4 import BeautifulSoup, NavigableString



class SpoilerCore:

    # Braking bad tv trops pages
    tropepages = [
        "http://tvtropes.org/pmwiki/pmwiki.php/BreakingBad/TropesAToB",
        "http://tvtropes.org/pmwiki/pmwiki.php/BreakingBad/TropesCToD",
        "http://tvtropes.org/pmwiki/pmwiki.php/BreakingBad/TropesEToL",
        "http://tvtropes.org/pmwiki/pmwiki.php/BreakingBad/TropesMToR",
        "http://tvtropes.org/pmwiki/pmwiki.php/BreakingBad/TropesSToZ"
    ]

    def __init__(self, maxwords=0):
        self.maxwords = maxwords
        self._crawlers = []
        self.reload_all_spoilers()

    def getRandomSpoiler(self):
        return random.choice(self.spoilers)

    def save_spoilers(self, filename='spoilers.txt'):
        with open(filename, 'w+') as f:
            for item in self.spoilers:
                f.write("%s\n" % item)

    def handleNewSpoiler(self, result):
        self.spoilers.append(result)

    def genReq(self, url):
        return request.Request(url)

    def reload_all_spoilers(self):
        self.spoilers = []
        self.completion = 0
        for link in self.tropepages:
            self.parse_tvtropes_link(link)
        for t in self._crawlers:
            t.join()

    def parse_tvtropes_link(self, url):
        t = Thread(target=self._parse_tvtropes_link, args=(url,))
        self._crawlers.append(t)
        t.start()

    def _parse_tvtropes_link(self, url):
        req = request.Request(url)
        with request.urlopen(req) as page:
            raw = page.read()
            self.htmlparser(raw)

    def htmlparser(self, code):
        def hasSpoiler(tag):
            return tag.find("span", class_="spoiler") is not None

        def recursivePrintout(tag):
            ret = ""
            for child in tag.descendants:
                if isinstance(child, NavigableString):
                    ret += child.string
            return ret.strip()

        soup = BeautifulSoup(code, "html.parser")
        bullets = soup.find_all("li")
        for bullet in bullets:
            if hasSpoiler(bullet):
                spoilertxt = recursivePrintout(bullet)
                if len(spoilertxt.split(" ")) < self.maxwords or self.maxwords == 0:
                    self.spoilers.append(spoilertxt)


if __name__ == "__main__":
    core = SpoilerCore()
    print('Scraped %d Spoilers for BreakingBad' % len(core.spoilers))
    print('Here\'s a random spoiler:\n %s'  % core.getRandomSpoiler())
    core.save_spoilers(filename='bb_spoilers.txt')
