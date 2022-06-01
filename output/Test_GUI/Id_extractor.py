import requests as r
from Bio import SeqIO
from io import StringIO
import pandas

"""parsing of first input file containing protein names and getting fasta sequences from uniprot"""


def write_to_file(seq_dict):
    with open("Yeast_proteome.txt", "w") as f:
        for current_protein in seq_dict.keys():
            current_id = list(seq_dict[current_protein].keys())[0]
            current_line = str(current_id) \
                           + "\n" \
                           + str(seq_dict[current_protein][current_id].seq) \
                           + "\n"
            f.write(current_line)


def read_table(file):
    id_file = pandas.read_excel(file, index_col=0)
    seq_dict = {}
    i = 0
    for cID in id_file["UniProt ID"]:
        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(cID, i)
        i += 1
        baseUrl = "http://www.uniprot.org/uniprot/"
        currentUrl = baseUrl \
                     + cID \
                     + ".fasta"

        response = r.post(currentUrl)
        cData = ''.join(response.text)
        Seq = StringIO(cData)
        pSeq = SeqIO.to_dict(SeqIO.parse(Seq, 'fasta'))
        seq_dict[cID] = pSeq
    return seq_dict

# adds uniprot link for every protein in main dictionnary

def get_uniprot_url(seq_dict):
    for current_id in seq_dict:
        uniprot_id = current_id.split("|")[1]
        base_url = "http://www.uniprot.org/uniprot/"
        current_url = base_url + uniprot_id
        seq_dict[current_id]["Uniprot_link"] = current_url
    return seq_dict
