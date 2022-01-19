import os
def signalp_search(fasta_path, temp_dir):
    call = "python3 signalp/signalp/predict.py --fastafile "+ str(fasta_path) +" --output " + str(temp_dir) + " --organism eukarya --mode slow-sequential"
    print(call)
    os.system(call)
signalp_search(r"C:\Users\Martin\Desktop\Cours\M1\S8\Projet_Tut\UP000002311_559292.fasta", r"C: \Users\Martin\Desktop\Cours\M1\S8\Projet_Tut")