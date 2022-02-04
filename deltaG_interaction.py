import re
import requests
from bs4 import BeautifulSoup

def deltaG(seq):
    link = "https://dgpred.cbr.su.se/analyze.php?with_length=on&seq=" + seq

    requete = requests.get(link)
    page = requete.content
    soup = BeautifulSoup(page, 'html.parser')

    data = soup.table

    res = re.compile(r'green\">(.*)</span></b></big></td></tr>')
    for all in data:
        toto = re.search(res, str(all))
        if toto is not None:
            # print("line:", str(all))
            print(toto.group(1))

    exit(0)

seq = "ATEYIGYAWAMVVVIIGAWWGIKLFKK"
print(deltaG(seq))


