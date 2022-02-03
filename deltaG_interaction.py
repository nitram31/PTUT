import re
import requests
from bs4 import BeautifulSoup

seq = "ATEYIGYAWAMVVVIIGATIGIKLFKK"
link = "https://dgpred.cbr.su.se/analyze.php?with_length=on&seq=" + seq

requete = requests.get(link)
page = requete.content
soup = BeautifulSoup(page, 'html.parser')

data = soup.table

#res = re.compile(r'^([\w]*)(<b><span style="color: green">)([+-]\w.\w{3,})(</span></b></big></td></tr>)$')
#res = re.compile(r'([+-])\w.\w{3,}')
#print(res)
for all in data:
    if re.match(res, str(all)) != None:
        print(all)
        #pass
#print(data)

#<span style="color: green">-0.61</span>
#/html/body/table/tbody/tr[3]/td/table/tbody/tr[51]/td/big/b/span


