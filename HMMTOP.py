from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import tm_hmm as tm
import re
import time


def hmmtop_reformat(results):
    """takes the results from the HMMTOP_search function, and reformat it to a same form as the pytmhmm.predict
    function."""

    annotation = ''
    for res in results:
        if res == 'i' or res == 'I':
            annotation += 'i'
        elif res == 'H' or res == 'h':
            annotation += 'M'
        elif res == 'o' or res == 'O':
            annotation += 'O'
    return annotation


def hmmtop_search(seq_dict):
    """takes the dictionary, and if the sequence has not been predicted with a TM segment, it tries to predict it with
    HMMTOP"""

    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # allows the window to ot be seen
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1)
    url = "http://www.enzim.hu/hmmtop/html/submit.html"
    text_id = '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr[2]/td/font/textarea'
    button_id = '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input'
    cpt = 1
    max_length = len(seq_dict.keys())

    #temporary
    temp_seq_dict = {}
    for current_id in seq_dict.keys():
        try:
            if seq_dict[current_id]['targetp_pred'][0] != 'MT' and seq_dict[current_id]['TMsegment_pred'].count(
                    'M') <= 1:
                temp_seq_dict[current_id] = seq_dict[current_id]
        except:
            pass

    seq_dict = temp_seq_dict

    for current_id in seq_dict.keys():
        print(cpt, "/", max_length)
        cpt += 1
        if seq_dict[current_id]['TMsegment_pred'].count('M') == 0:  # finds sequence without TM predicted
            print(current_id)
            driver.get(url)  # refreshes the page to the menu
            text_area = driver.find_element(By.XPATH, text_id)  # find the text area to paste the sequence in
            button_area = driver.find_element(By.XPATH, button_id)
            text_area.send_keys(seq_dict[current_id]['seq'])
            time.sleep(0.25)
            button_area.click()
            time.sleep(0.75)
            page = driver.page_source  # gets html code taht contains the results after the button press
            soup = BeautifulSoup(page, features="html.parser")
            other_res = re.compile(r'(pred )(\D*)')  # regular expression that finds the string of results
            results = ''
            for line in soup:
                hmmtop_result = re.search(other_res, str(line))
                if hmmtop_result is not None:
                    results += hmmtop_result.group(2)
                    annotation = hmmtop_reformat(results)
                    """Reformat the results to be used by the str_to_pos function 
                    that allows the string to be included in the dictionary as a list"""
                    pos_list = tm.str_to_pos(annotation)
                    seq_dict[current_id]['TMsegment_pred'] = pos_list

    return seq_dict


if __name__ == "__main__":
    seq_dict = {'sp|Q07914|TIM14_YEAST': {'seq': "MVQRWLYSTNAKDIAVLYFMLAIFSGMAGTAMSLIIRLELAAPGSQYLHGNSQLVQS"}}
    seq_dict = hmmtop_search(seq_dict)
    print(seq_dict)
