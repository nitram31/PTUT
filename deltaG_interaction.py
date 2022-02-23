import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def deltaG(seq_dict):
    for current_id in seq_dict.keys():
        seq = seq_dict[current_id]['seq']
        tmhmm_pred = seq_dict[current_id]['TMsegment_pred']

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
                deltaG_pred = pred.group(2)
                seq_dict[current_id]['deltaG_pred'] = deltaG_pred
        try:
            seq_dict[current_id]['deltaG_pred'] = seq_dict[current_id]['deltaG_pred']
        except:
            seq_dict[current_id]['deltaG_pred'] = "tm segment too long"

    return seq_dict


def deltaG_TM(seq_dict):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # allows the window to ot be seen
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1)
    url = "https://dgpred.cbr.su.se/index.php?p=fullscan"
    text_id = '/html/body/table[2]/tbody/tr[5]/td/form/textarea'
    button_id = '/html/body/table[2]/tbody/tr[5]/td/form/input[1]'
    cpt = 1

    # temporary
    temp_seq_dict = {}
    for current_id in seq_dict.keys():
        try:
            if seq_dict[current_id]['targetp_pred'][0] != 'MT':
                temp_seq_dict[current_id] = seq_dict[current_id]
        except:
            print('protein does not exist')
    seq_dict = temp_seq_dict
    max_length = len(seq_dict.keys())

    for current_id in seq_dict.keys():
        print(cpt, "/", max_length)
        cpt += 1
        print(current_id)
        driver.get(url)  # refreshes the page to the menu
        text_area = driver.find_element(By.XPATH, text_id)  # find the text area to paste the sequence in
        button_area = driver.find_element(By.XPATH, button_id)
        text_to_send = seq_dict[current_id]['seq']
        text_area.send_keys(text_to_send)
        time.sleep(0.75)
        button_area.click()
        time.sleep(2)
        pos_list = seq_dict[current_id]['TMsegment_pred']
        try:
            text = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody').text
            pattern = re.compile(r'(\d{1,3})(-)(\d{1,3})\s*(\d{2})\s*(.{6})\s*')  # regular expression that finds the string of results
            first_res_orientation = seq_dict[current_id]['TMsegment_pred'][0]
            if first_res_orientation == 'O' or first_res_orientation == 'o':
                other_orientation = 'i'
            else:
                other_orientation = 'O'
            tm_results = []
            score_result = []
            for line in text.splitlines():
                deltaG_result = re.search(pattern, str(line))
                if deltaG_result is not None:

                    tm_start = int(deltaG_result.group(1))
                    tm_end = int(deltaG_result.group(3))
                    deltaG_score = float(deltaG_result.group(5))
                    score_result.append(deltaG_score)
                    tm_results.append(tm_start)
                    tm_results.append(tm_end)
                    if pos_list[1] == 1:
                        pos_list.append(tm_results[0]-1)
                        pos_list.append('M')
                        pos_list.append(tm_results[0])
                        pos_list.append(tm_results[1])
            for i in range(1, len(tm_results), 2):
                if pos_list[-3:][0] == 'M':
                    if pos_list[-6:][0] == first_res_orientation:
                        pos_list.append(other_orientation)
                    else:
                        pos_list.append(first_res_orientation)
                    pos_list.append(pos_list[-2:][0]+1)
                    try:
                        pos_list.append(tm_results[i+1]-1)
                    except:
                        pos_list.append(len(text_to_send))
                    if i != len(tm_results) - 1:
                        pos_list.append('M')
                        pos_list.append(tm_results[i+1])
                        pos_list.append(tm_results[i+2])
            seq_dict[current_id]['TMsegment_pred'] = pos_list
            seq_dict[current_id]['deltaG_pred'] = score_result
        except:
            pos_list.append(len(text_to_send))
            seq_dict[current_id]['TMsegment_pred'] = pos_list
            seq_dict[current_id]['deltaG_pred'] = 'No tm'

    return seq_dict
if __name__ == "__main__":
    seq = "ATEYIGYAWAMVVVIIGAWWGIKLFKK"
    pred = deltaG(seq)
    print(pred)


