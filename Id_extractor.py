import requests as r
from Bio import SeqIO
from io import StringIO
import pandas

def write_to_file(seq_dict):
    with open("Yeast_proteome.txt", "w") as f :

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
    for cID in id_file["UniProt ID"] :
        print(cID, i)
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
    return(seq_dict)
seq_dict = read_table(r"C:\Users\Martin\Desktop\Cours\M1\S8\Projet_Tut\Seq_Ids.xlsx")
write_to_file(seq_dict)







