import re
import requests
from bs4 import BeautifulSoup


def deltaG(seq_dict):
    for current_id in seq_dict.keys():
        seq = seq_dict[current_id]['seq']
        tmhmm_pred = seq_dict[current_id]['tmhmm_pred']

        tm_segment = ""
        for i in range(0, len(tmhmm_pred), 3):
            if tmhmm_pred[i] == 'M':
                for l in range(tmhmm_pred[i+1], tmhmm_pred[i+2]):
                    tm_segment += seq[l]
        link = "https://dgpred.cbr.su.se/analyze.php?with_length=on&seq=" + tm_segment

        requete = requests.get(link)
        page = requete.content
        soup = BeautifulSoup(page, 'html.parser')

        data = soup.table


        res = re.compile(r'(green|red)\">(.*)</span></b></big></td></tr>')
        for all in data:
            pred = re.search(res, str(all))
            if pred is not None:
                # print("line:", str(all))
                deltaG_pred = pred.group(2)
                seq_dict[current_id]['deltaG_pred'] = deltaG_pred
        try:
            seq_dict[current_id]['deltaG_pred'] = seq_dict[current_id]['deltaG_pred']
        except:
            seq_dict[current_id]['deltaG_pred'] = "tm segment too long"

    return seq_dict

if __name__ == "__main__":
    seq = "ATEYIGYAWAMVVVIIGAWWGIKLFKK"
    pred = deltaG(seq)
    print(pred)


