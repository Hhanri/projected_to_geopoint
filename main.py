from pyproj import Transformer
import tkinter as tk # from tkinter import Tk for Python 3.x
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import csv

window = tk.Tk()
window.minsize(200, 100)
file_path_sv = tk.StringVar()
inEPSG_sv = tk.StringVar(value= "3857")
outEPSG_sv = tk.StringVar(value= "4326")
output_file_path_sv = tk.StringVar()
output_file_name_sv = tk.StringVar()

def get_output_file_path():
    return f"{output_file_path_sv.get()}/{output_file_name_sv.get()}.xyz"

def read_and_output_data() -> list[list[int | float]]:
    if (file_path_sv.get() == "" or output_file_path_sv.get() == ""):
        messagebox.showerror(title="Missing fields", message="Select input file and output directory")
        return

    #output
    if (output_file_name_sv.get() == ""):
	    output_file_name_sv.set(value="output")
		
    output_f = open(get_output_file_path(), 'w', newline='', encoding='utf-8')
    writer = csv.writer(output_f)

    #input
    f = open(file_path_sv.get(), "r")

    for line in f:
        line_data = line.strip().split(',')
        if (len(line_data) == 6):
            row_data = [
                float(line_data[0]),
                float(line_data[1]),
                float(line_data[2]),
                int(line_data[3]),
                int(line_data[4]),
                int(line_data[5]),
            ]

            row_data[1], row_data[0] =  projected_to_geographic(row_data[1], row_data[0])
            writer.writerow(row_data)

    f.close()
    output_f.close()
    messagebox.showinfo(title="STATUS COMPLETE", message="Computation is done !")
    return

def select_file() -> None:
    tempFile = askopenfilename()
    extension = tempFile[len(tempFile) - 3:]
    if (extension != "xyz"):
        messagebox.showwarning(title="ERROR", message="This file is not a .xyz")
        print("WRONG FILE EXTENSION")
        return
    file_path_sv.set(value=tempFile)
    return

def select_output_directory() -> None:
    tempDirectory = askdirectory()
    output_file_path_sv.set(value=tempDirectory)
    return

def projected_to_geographic(x: float, y: float) -> tuple[float, float]:
    transformer = Transformer.from_crs(f"EPSG:{inEPSG_sv.get()}", f"EPSG:{outEPSG_sv.get()}")
    return transformer.transform(x,y)


select_file_button = tk.Button(text="Select a file", command= lambda: select_file())
select_file_button.pack()

select_output_directory_button = tk.Button(text="Select your output directory", command= lambda: select_output_directory())
select_output_directory_button.pack()

outpout_file_name_text = tk.Label(text='output file name (no extension)')
outpout_file_name_text.pack()

output_file_name_entry = tk.Entry(window, textvariable=output_file_name_sv)
output_file_name_entry.pack()

in_epsg_text = tk.Label(text='input EPSG')
in_epsg_text.pack()
in_epsg_text_field = tk.Entry(window, textvariable= inEPSG_sv)
in_epsg_text_field.pack()

out_epsg_text = tk.Label(text='output EPSG')
out_epsg_text.pack()
out_epsg_text_field = tk.Entry(window, textvariable= outEPSG_sv)
out_epsg_text_field.pack()

file_path_label = tk.Label(textvariable=file_path_sv)
file_path_label.pack()

file_path_label = tk.Label(textvariable=output_file_path_sv)
file_path_label.pack()

output_button = tk.Button(text="Output file", command=lambda: read_and_output_data())
output_button.pack()

window.mainloop()
