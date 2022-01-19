import tkinter
from tkinter import *
from tkinter import filedialog
from Mylib import Fastaboy

def main():

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
            Seq_dict = Fastaboy.fasta_reader(path)
            data_size = int(len(Seq_dict.keys())/8)
            for residue_number in range(0, int(data_size)):
                progress_bar(residue_number, data_size)
                progress = residue_number
                print(progress)
            progress_label = Label(root, text="finished")
            progress_label.grid(row=5, column=0, sticky=W+E)


    def progress_bar(progress, data_size):
        status = str(progress) + " out of " + str(data_size)
        progress_label = Label(root, text=status)
        root.update_idletasks()
        progress_label.grid(row=5, column=0, sticky=W+E)

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

    root = Tk()

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