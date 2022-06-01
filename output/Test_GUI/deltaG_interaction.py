import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def deltaG(seq_dict):

    """Takes a dictionary and adds the predicted hydrophobicity score of the TM segment"""
    for current_id in seq_dict.keys():
        seq = seq_dict[current_id]['seq']
        tmhmm_pred = seq_dict[current_id]['DeltaG+HMMTOP_TM_pred']

        tm_segment = ""
        for i in range(0, len(tmhmm_pred), 3):
            if tmhmm_pred[i] == 'M': #when M is found in tmhmm results, we take first two coordinates an we reconstruct TM sequence
                for l in range(tmhmm_pred[i+1], tmhmm_pred[i+2]):
                    tm_segment += seq[l]
        link = "https://dgpred.cbr.su.se/analyze.php?with_length=on&seq=" + tm_segment #base URL + sequence = link creation

        requete = requests.get(link)
        page = requete.content
        soup = BeautifulSoup(page, 'html.parser')

        data = soup.table


        res = re.compile(r'(green|red)\">(.*)</span></b></big></td></tr>') #RE of searched value on Wen page
        for all in data:
            pred = re.search(res, str(all))
            if pred is not None:
                deltaG_pred = pred.group(2)
                seq_dict[current_id]['deltaG_pred_score'] = deltaG_pred #saving Web scraping results in main dictionnary
        try:
            seq_dict[current_id]['deltaG_pred_score'] = seq_dict[current_id]['deltaG_pred_score']
        except:
            seq_dict[current_id]['deltaG_pred_score'] = "tm segment too long" #dgpred has a limited sequence input length

    return seq_dict


def deltaG_TM(seq_dict):
    """Takes a dictionary and adds the predicted transmembrane location"""
    WINDOW_SIZE = "1920,1080"
    #initialization of Chrome web driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # allows the window to not be seen in console
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1) #time of web page charging
    url = "https://dgpred.cbr.su.se/index.php?p=fullscan"
    text_id = '/html/body/table[2]/tbody/tr[5]/td/form/textarea' #XPATH adress pointing to the zone of sequence input
    button_id = '/html/body/table[2]/tbody/tr[5]/td/form/input[1]' #XPATH adress pointing to the button we need to click to start the research
    cpt = 1
    max_length = len(seq_dict.keys())
    for current_id in seq_dict.keys():
        print(cpt, "/", max_length)
        cpt += 1
        print(current_id) #shows the progress

        driver.get(url)  # refreshes the page to the menu
        text_area = driver.find_element(By.XPATH, text_id)  # find the text area to paste the sequence in
        button_area = driver.find_element(By.XPATH, button_id)
        text_to_send = seq_dict[current_id]['seq'] #paste the used part of the sequence in main dictionnary
        text_area.send_keys(text_to_send)
        time.sleep(0.75)
        button_area.click()
        time.sleep(1.75)
        pos_list = ['x', 1] #list initialization containing predicted TM positions and prediction score
        try: #if tm segment is found
            text = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody').text

            pattern = re.compile(r'(\d{1,3})(-)(\d{1,3})\s*(\d{2})\s*(.{6})\s*')  # regular expression that finds the string of results

            tm_results = []
            score_result = []

            for line in text.splitlines(): #iterate on the deltaG results
                deltaG_result = re.search(pattern, str(line))

                if deltaG_result is not None:

                    tm_start = int(deltaG_result.group(1)) #coordinates of first TM aminoacid
                    tm_end = int(deltaG_result.group(3)) #coordinates of last TM aminoacid
                    deltaG_score = float(deltaG_result.group(5)) #score of prediction of the presence of TM segment
                    score_result.append(deltaG_score)
                    tm_results.append(tm_start)
                    tm_results.append(tm_end)
                    if pos_list[-1] == 1:
                        pos_list.append(tm_results[0]-1)
                        pos_list.append('M')
                        pos_list.append(tm_results[0])
                        pos_list.append(tm_results[1])

            for i in range(1, len(tm_results), 2):  # iterate on the tm_result
                if pos_list[-3:][0] == 'M':
                    pos_list.append('x')
                    pos_list.append(pos_list[-2:][0]+1)
                    try:
                        pos_list.append(tm_results[i+1]-1)

                    except IndexError:
                        pos_list.append(len(text_to_send))

                    if i != len(tm_results) - 1:
                        pos_list.append('M')
                        pos_list.append(tm_results[i+1])
                        pos_list.append(tm_results[i+2])

            seq_dict[current_id]['DeltaG_TM_pred'] = pos_list
            seq_dict[current_id]['deltaG_pred_score'] = score_result
        except:
            pos_list.append(len(text_to_send))
            seq_dict[current_id]['DeltaG_TM_pred'] = pos_list
            seq_dict[current_id]['deltaG_pred_score'] = 'No tm'

    return seq_dict
if __name__ == "__main__":
    seq = "ATEYIGYAWAMVVVIIGAWWGIKLFKK"
    pred = deltaG(seq)
    print(pred)


