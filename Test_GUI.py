import tkinter
from tkinter import *
from tkinter import filedialog
from Mylib.PTUT import Fastaboy
import TargetP
import tm_hmm
import deltaG_interaction
import HMMTOP
import Mylib.PTUT.charge as charge


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

            print("ori", len(seq_dict.keys()))
            seq_dict = TargetP.parse_targetp(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\scere_summary.targetp2", seq_dict)
            #seq_dict = TargetP.parse_targetp(r"D:\Bureau\Cours\M1\pythonProject\Mylib\PTUT\scere_summary.targetp2",
            #                                 seq_dict)
            seq_dict = tm_hmm.tmhmm_read(seq_dict)
            #print(seq_dict)
            print("before HMMTOP", len(seq_dict.keys()))
            seq_dict = HMMTOP.hmmtop_search(seq_dict)
            print("before HMMTOP", len(seq_dict.keys()))
            seq_dict = tm_hmm.sort_dict(seq_dict)

            seq_dict = deltaG_interaction.deltaG(seq_dict)
            seq_dict = charge.dict_parser(seq_dict)
            print("after dict parser", len(seq_dict.keys()))
            print(seq_dict)
            print("before charge sort")
            seq_dict = charge.charge_sort(seq_dict)
            print(seq_dict)
            print("after charge sort")

            seq_dict = tm_hmm.orientation_sort(seq_dict)
            print(seq_dict)
            print("kekw", len(seq_dict.keys()))

            '''data_size = int(len(seq_dict.keys())/2)
            progress = 0

            for residue_number in range(0, int(data_size)):
                progress_bar(residue_number, data_size)

                progress = residue_number
            progress_label = Label(root, text="finished")
            progress_label.grid(row=5, column=0, sticky=W+E)'''

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
