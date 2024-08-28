import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import yaml

def open_project():
    folder_path = filedialog.askdirectory(title="Select a Project Folder")
    if folder_path:
        messagebox.showinfo("Project Opened", f"Opened project at: {folder_path}")

def save_convention(convention_name_entry,convention_entry,separator_entry):
    name=convention_name_entry.get()
    convention=convention_entry.get()
    separator=separator_entry.get()
    if not name:
        messagebox.showwarning("Input Error", "Convention name cannot be empty.")
        return

    if not convention:
        messagebox.showwarning("Input Error", "Convention entry cannot be empty.")
        return

    if not separator:
        messagebox.showwarning("Input Error", "Separator entry cannot be empty.")
        return
'''    with open('MarCell_data.yaml', 'r') as f:
        data_convention = yaml.safe_load(f)
        data_convention['convention'] = 1 
        print(data) '''

def add_naming_convention():

    convention_window = tk.Toplevel(root)
    convention_window.geometry('700x150')
    convention_window.title("Add a naming convention")
    convention_window.columnconfigure([0,1,2], weight=1, minsize=50)
    convention_window.rowconfigure([0,1,2,3], weight=1)

    tk.Label(convention_window, text="Convention name: ").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    convention_name_entry = tk.Entry(convention_window, width=30)
    convention_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(convention_window, text="Example:  ").grid(row=3, column=0, padx=10, pady=10)
    tk.Label(convention_window, text="Convention:  ").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(convention_window, text="Exp_Date, Condition, Age, Sex, Marker").grid(row=3, column=1, padx=10, pady=10)
    tk.Label(convention_window, text="Separator: ").grid(row=1, column=2, padx=10, pady=10, sticky='w')
    separator_entry = tk.Entry(convention_window, width=3)
    separator_entry.grid(row=1, column=3, padx=10, pady=10,sticky='e')
    

    convention_entry = tk.Entry(convention_window, width=60)
    convention_entry.grid(row=1, column=1, padx=10, pady=10)

    save_convention_button = tk.Button(convention_window, text="Save", command=lambda:save_convention(convention_name_entry,convention_entry, separator_entry))
    save_convention_button.grid(row=3, column=3, padx=10, pady=10)

def create_project():
    create_window = tk.Toplevel(root)
    create_window.geometry('700x700')
    create_window.title("Create New Project")
    create_window.columnconfigure([0,1,2], weight=1, minsize=50)
    create_window.rowconfigure([0,1,2,3,4,5,6,8,9,10,11], weight=1)

    tk.Label(create_window, text="Project Name:").grid(row=0, column=0, padx=10, pady=10)
    project_name_entry = tk.Entry(create_window, width=50)
    project_name_entry.grid(row=0, column=1, padx=10, pady=10)



    def browse_folder():
        folder_path = filedialog.askdirectory(title="Select a Folder to Save Project")
        if folder_path:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder_path)

    tk.Label(create_window, text="Save Location:").grid(row=1, column=0, padx=10, pady=10)
    folder_entry = tk.Entry(create_window, width=50)
    folder_entry.grid(row=1, column=1, padx=10, pady=10)
    tk.Label(create_window, text= 'Select a convention: ').grid(row=3, column=0, padx=10, pady=10)
    keysList = list(data['convention'].keys())
    temporary_list = ['No convention registered']
    if not keysList:
        options = temporary_list
    else:
        options = keysList

    # Tkinter variable to store the selected option
    selected_convention = tk.StringVar(create_window)
    selected_convention.set('Select')  # Set default value

    # Create an OptionMenu with the initially empty list
    convention_menu = tk.OptionMenu(create_window, selected_convention, *options)
    convention_menu.config(width=50)
    convention_menu.grid(row=3, column=1, padx=10, pady=10)

    
    add_convention_button = tk.Button(create_window, text="Add a convention", command=add_naming_convention)
    add_convention_button.grid(row=3, column=3, padx=10, pady=10)



    tk.Label(create_window, text="Path to TAPAS scripts: ").grid(row=5, column=0, padx=10, pady=10, sticky='w')
    tapas_path_entry = tk.Entry(create_window, width=50)
    tapas_path_entry.grid(row=5, column=1, padx=10, pady=10,sticky='e')
    tapas_path_entry.insert(0,tapas_path)

    
    browse_button = tk.Button(create_window, text="Browse", command=browse_folder)
    browse_button.grid(row=1, column=2, padx=10, pady=10)

    def save_project():
        project_name = project_name_entry.get().strip()
        folder_path = folder_entry.get().strip()

        if not project_name:
            messagebox.showerror("Error", "Project name cannot be empty.")
            return

        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        # Create project folder
        project_path = os.path.join(folder_path, project_name)
        try:
            os.makedirs(project_path)
            messagebox.showinfo("Success", f"Project '{project_name}' created at: {project_path}")
            create_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create project folder: {e}")
    
    tk.Label(create_window, text="Cellpose model name: ").grid(row=6, column=0, padx=10, pady=10, sticky='w')
    cellpose_name_entry = tk.Entry(create_window, width=50)
    cellpose_name_entry.grid(row=6, column=1, padx=10, pady=10,sticky='e')
    cellpose_name_entry.insert(0,cellpose_model)

    frame = tk.Frame(master=create_window, relief=tk.RAISED, borderwidth=1)
    frame.grid(row=7, rowspan = 4, columnspan=3 )
    tk.Label(frame, text='Preprocessing').grid(row=7, column=1, padx=10, pady=10, sticky='w')
    tk.Label(frame, text='Channel to process: ').grid(row=8, column=0, padx=10, pady=10, sticky='w')
    image_channel_entry=tk.Entry(frame, width=10)
    image_channel_entry.grid(row=8, column=1, padx=10, pady=10,sticky='e')

    tk.Label(frame, text='Z crop: ').grid(row=9, column=0, padx=10, pady=10, sticky='w')
    z_cropmin_entry=tk.Entry(frame, width=10)
    z_cropmin_entry.grid(row=9, column=1, padx=10, pady=10,sticky='e')
    z_cropmin_entry.insert(0,0)
    z_cropmax_entry=tk.Entry(frame, width=10)
    z_cropmax_entry.grid(row=9, column=2, padx=10, pady=10,sticky='e')
    z_cropmax_entry.insert(0,18)

    tk.Label(frame, text='Scale XY ').grid(row=10, column=0, padx=10, pady=10, sticky='w')
    scale_min_entry=tk.Entry(frame, width=10)
    scale_min_entry.grid(row=10, column=1, padx=10, pady=10,sticky='e')
    scale_min_entry.insert(0,1)
    scale_max_entry=tk.Entry(frame, width=10)
    scale_max_entry.grid(row=10, column=2, padx=10, pady=10,sticky='e')
    scale_max_entry.insert(0,1)

    save_button = tk.Button(create_window, text="Create Project", command=save_project)
    save_button.grid(row=11, columnspan=3, pady=10)


script_directory = os.path.dirname(os.path.abspath(__file__))

def load_project_data(filename="MarCell_data.yaml"):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

data=load_project_data(filename="MarCell_data.yaml")
tapas_path = data["tapas_path"]
convention = data["convention"]
cellpose_model = data["cellpose_model"]

root = tk.Tk()
root.title("Project Manager")

create_button = ttk.Button(root, text="Create Project", command=create_project)
create_button.pack(padx=20, pady=10)

open_button = ttk.Button(root, text="Open Project", command=open_project)
open_button.pack(padx=20, pady=10)

root.mainloop()
