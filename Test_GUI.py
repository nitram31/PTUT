import tkinter
from tkinter import *
from tkinter import filedialog
from Mylib.PTUT import Fastaboy
from tabulate import tabulate
import TargetP
import pandas as pd
import Id_extractor
import tm_hmm
import deltaG_interaction
import HMMTOP
import Mylib.PTUT.charge as charge
import localizations02
import Class



def main():
    root = Tk()

    def myclick():
        path = mypath.get()
        button_message = "please select a file"
        if path == "":
            mylabel2 = Label(root, text=button_message)
            mylabel2.grid(row=4, column=0)
        else:
            button_message = "scanning " + path + " for proteins"
            mylabel2 = Label(root, text=button_message)
            mylabel2.grid(row=4, column=0)
            seq_dict = Fastaboy.fasta_reader(path)

            seq_dict = TargetP.parse_targetp(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\scere_summary.targetp2", seq_dict)
            #seq_dict = TargetP.parse_targetp(r"D:\Bureau\Cours\M1\pythonProject\Mylib\PTUT\scere_summary.targetp2",
                                             #seq_dict)

            seq_dict = Fastaboy.csv_parser(seq_dict, r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\output.csv", sep=";")

            #seq_dict = Fastaboy.final_parser(r'C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\results.txt', seq_dict)

            #seq_dict = tm_hmm.tmhmm_read(seq_dict)

            #seq_dict = HMMTOP.hmmtop_search(seq_dict)

            #seq_dict = tm_hmm.sort_dict(seq_dict)

            #seq_dict = deltaG_interaction.deltaG_TM(seq_dict)

            seq_dict = charge.dict_parser(seq_dict)

            seq_dict = Id_extractor.get_uniprot_url(seq_dict)

            #seq_dict = charge.charge_sort(seq_dict)


            #seq_dict = tm_hmm.orientation_sort(seq_dict)

            ### colonne localisation

            dict_localisations = localizations02.creertable(r"localisation_S2.csv")
            for keys in seq_dict.keys():
                seq_dict[keys]["localization: "] = []
                for i in dict_localisations.keys(): #iteration of dictionnary in a function localizations02
                    if str(i) in keys:
                        seq_dict[keys]["localization: "] = dict_localisations[i]



            """si on trouve la proteine de seq_dict dans localizations02"""
            seq_dict = Class.class_predictor(seq_dict)


            table_values = []
            col_names = []

            first_prot = list(seq_dict.keys())[0]
            for col in seq_dict[first_prot]:
                col_names.append(col)
            col_names[0] = 'name'


            for key in seq_dict.keys():
                line = []
                key_list = [key]
                for variable_names in seq_dict[key]:
                    if variable_names != 'seq':
                        key_list.append(seq_dict[key][variable_names])
                line.append(key_list)
                table_values += line

            content = pd.DataFrame(table_values, columns=col_names)
            content.to_csv('output.csv', sep=";")
            print(seq_dict)


    def progress_bar(progress, data_size):
        status = str(progress) + " out of " + str(data_size)
        progress_label = Label(root, text=status)
        root.update_idletasks()
        progress_label.grid(row=5, column=0, sticky=W + E)

    def myfile():
        root.fasta_file = filedialog.askopenfilename()
        mypath.delete(first=0, last=tkinter.END)
        mypath.insert(0, root.fasta_file)

    def paste(self):
        self.entry.event_generate('<Control-v>')

    def cut(self):
        self.entry.event_generate('<Control-x>')

    def copy(self):
        self.entry.event_generate('<Control-c>')

    mylabel2 = Label(root, text="")

    frame = LabelFrame(root, text="Fasta file path")
    frame.grid(row=2, column=0, padx=10, pady=50)

    frame2 = LabelFrame(root, text="Select Fasta file")
    frame2.grid(row=2, column=1, padx=10, pady=10)

    mybutton = Button(root, text="Run scan", command=myclick)
    mybutton2 = Button(frame2, text="Select file", command=myfile)

    mypath = Entry(frame, width=50)

    mypath.grid(row=2, column=0)
    mybutton.grid(row=3, column=0)
    mybutton2.grid(row=2, columns=2)

    mylabel2.grid(row=2, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()
