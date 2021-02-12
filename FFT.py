from tkinter import *
import numpy as np
import pandas as pd
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import spectrogram, hanning
from scipy import signal
from tkinter.filedialog import asksaveasfile 
import csv
from tkinter import messagebox

root = Tk()
root.geometry('400x200')
root.title("FFT_Hesaplama v0.1")

mylabel = Label(root,text="Time Interval")
mylabel.pack()
e = Entry(root,width=20)
e.pack()

def opentxt():
    global main_df
    try:
        main_df = pd.DataFrame()
        global column
        text_file = filedialog.askopenfilename(initialdir="C:/Users/Unknown/Desktop",title="Open Text Files",filetypes=[("Text Files","*.txt")],)
        text_file = open(text_file,"r")
        stuff = text_file.readlines()

    
        main_df[text_file] = stuff
    
        text_file.close()
    
        c = len(stuff)
    except FileNotFoundError:
        messagebox.showerror("Error", "Lütfen bir text dosyası seçiniz.")

    try :
        
        a = float(e.get())

        b = np.arange(0,c/(1/a),a)
        main_df["time"] = b

        column = main_df.columns
        column = list(column)
    
        time = list(main_df["time"].values) 
        lan = list(main_df[column[0]].values)
        ivj = [float(i) for i in lan]
    except ValueError:
        messagebox.showerror("Error", "Lütfen zaman adımı şeçiniz.")
def PlotPage():
    global main_df
    global column
    global time
    global lan
    global ivj
    newWindow = Toplevel(root)
    newWindow.geometry('1000x600')

    
    mylabel2 = Label(newWindow,text="Data and Plot Page")
    mylabel2.pack()
    
    time = list(main_df["time"].values) 
    lan = list(main_df[column[0]].values)
    ivj = [float(i) for i in lan]
    my_tree = ttk.Treeview(newWindow)
    my_tree["columns"] = column
    
    
    my_tree.column("#0")
    my_tree.column(column[1])
    my_tree.column(column[0])
    
    my_tree.heading("#0",text="Label")
    my_tree.heading(column[1],text=column[0])
    my_tree.heading(column[0],text=column[1])
    
    vsb = ttk.Scrollbar(newWindow, orient="vertical", command=my_tree.yview)
    vsb.place(x=1000, y=50, height=200)

    my_tree.configure(yscrollcommand=vsb.set)
    for i in range(len(time)):
        my_tree.insert(parent="",index='end',iid=i,text=i,values=(time[i],lan[i]))
    
    
    my_tree.pack()
    
    def Plot_Data():

        figure = plt.Figure(figsize=(6,5), dpi=100)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, newWindow)
        chart_type.get_tk_widget().pack()
        ax.grid()
        ax.set_title("Plot")
        ax.set_xlabel("Time(s)")
        ax.set_ylabel("Acceleration (g)")
        ax.plot(time,ivj)
    
    mybutton3 = Button(newWindow,text="Plot Data",command=Plot_Data)
    mybutton3.pack(pady=10)
    
def FftWindow():
    global Samples
    global Overlap
    fftWindow = Toplevel(root)
    fftWindow.geometry('1000x400')

    options = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16348]
    mylabel6 = Label(fftWindow,text="Enter Samples")
    mylabel6.pack(pady=10)
    def M_selected():
        global Samples
        Samples = int(mycombo.get())
        
    def Overlap_selected():
        global Overlap
        Overlap = float(E_overlap.get())

        

    mycombo = ttk.Combobox(fftWindow,value=options)
    mycombo.current(12)
    mycombo.bind('<Return>', M_selected)
    mycombo.pack(pady=10)
    
    
    mybutton3 = Button(fftWindow,text="Select M",command=M_selected)
    mybutton3.pack(pady=10)
    
    mylabel5 = Label(fftWindow,text="Enter Overlap")
    mylabel5.pack()
    E_overlap = Entry(fftWindow,width=20)
    E_overlap.pack(pady=10)
    
    
    mybutton4 = Button(fftWindow,text="Select Overlap",command=Overlap_selected)
    mybutton4.pack()
    
    def FFT_Calculation():
        data_df = pd.DataFrame()
        global Samples
        global Overlap
        global column
        global lan
        global ivjj
        global mean_S
        lan = list(main_df[column[0]].values)
        a = float(e.get())
        fs = 1/a
        ivjj = [float(i) for i in lan]
        data_df[column[0]] = ivjj
        try:
            
            M = Samples
            NFFT = M
            win = signal.windows.hamming(M)
            overlap = Overlap
            overlap_samples = int(round(M*overlap)) # overlap in samples
            t, f, S = spectrogram(data_df[column[0]],fs=fs,window=win,nperseg=M,noverlap=overlap_samples,nfft=NFFT)
        
            avg_S = np.mean(S,axis=1)
            mean_S = pd.DataFrame()
            mean_S["xf"] = t
            mean_S[column[0]] = avg_S
        except ValueError:
            messagebox.showerror("Error", "Window Fonksiyonunuz Girdiğiniz Veriden Büyük Samples küçültünüz.")
        
    mybutton5 = Button(fftWindow,text="Calculate FFT-Window",command=FFT_Calculation)
    mybutton5.pack(pady = 5)
    

    def FFT_Plot_Data():
        global mean_S
        global chart_type
        figure = plt.Figure(figsize=(5,6), dpi=100)
        ax1 = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, fftWindow)
        chart_type.get_tk_widget().pack(padx=20)
        ax1.grid()
        ax1.set_title("Samples {}, Overlap {}".format(str(mycombo.get()), str(E_overlap.get())))
        ax1.set_xlabel("Freqeuncy(Hz)")
        ax1.set_ylabel("Amplitude (u)")
        ax1.plot(mean_S["xf"],mean_S[column[0]])
        
    def delete_plot():
        global chart_type
        chart_type.get_tk_widget().destroy()            
            
        
        
    mybutton6 = Button(fftWindow,text="Plot FFT-Window",command=FFT_Plot_Data)
    mybutton6.pack(pady = 5)


    
    def Save_Excel():
        global mean_S
        files = [('Excel Files', '*.csv')] 
        file = asksaveasfile(filetypes = files, defaultextension = files)
        mean_S.to_csv(file)
        
        
    mybutton10 = Button(fftWindow,text="Delete Plot FFT-Window",command=delete_plot)
    mybutton10.pack(pady = 5)

    mybutton7 = Button(fftWindow,text="Export Excel",command=lambda: Save_Excel())
    mybutton7.pack(pady = 5)
    
mybutton1 = Button(root,text="Open txt",command=opentxt)    
mybutton1.pack(pady=10)   

mybutton2 = Button(root,text="Data and Plot",command=PlotPage)    
mybutton2.pack()

mybutton2 = Button(root,text="Windowing FFT",command=FftWindow)    
mybutton2.pack(pady=10)



root.mainloop()
