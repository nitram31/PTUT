import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re

def parse_targetp(targetp_result, seq_dict):
    pat = re.compile(r'(^\w{6})\t(\w{2,5})\t(.{8})\t(.{8})\t(.{8})')
    with open(targetp_result) as file: #targetp_result is a file containing informations about every protein from official TargetP site
        #this informations were obtained with web scraping in Test_GUI script
        for line in file:
            matched_line = re.match(pat, line) #getting result with regex
            if matched_line != None:

                prot_id = matched_line.group(1) #protein ID
                targetp_pred = matched_line.group(2)  #class of protein (OTHER, SP, TM)
                if targetp_pred == "MT":
                    targetp_pred_score = matched_line.group(5)
                elif targetp_pred == "SP":
                    targetp_pred_score = matched_line.group(4)
                else:   #case for transmembrane proteins so our proteins of interest
                    targetp_pred_score = matched_line.group(3)
                    for current_id in seq_dict.keys():
                        if prot_id in current_id:
                            seq_dict[current_id]['targetp_pred'] = targetp_pred
                            seq_dict[current_id]['targetp_pred_score'] = targetp_pred_score
    return seq_dict


if __name__ == "__main__":
    parse_targetp(r"D:\Bureau\Cours\M1\pythonProject\Mylib\PTUT\scere_summary.targetp2")
