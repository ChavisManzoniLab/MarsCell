import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import yaml
import time
from MarsCell.functions_script import *
from shutil import copy2

def run_gui():
    ROI_list=['No ROI','Line']

    def initialise_project(path_to_tapas_scripts, specify_channel, scale_x, scale_y,zMin,zMax, path_to_folder, name_extraction, cellpose_name):
        try:
            initialisation(path_to_folder, name_extraction)
        except FileExistsError as fe:
            print("The folder \"%s\" already exists"%name_extraction)
        except Exception: pass

        change_channel(path_to_tapas_scripts, specify_channel)
        tapas_file = '01_tapas-preprocess.txt'
        pattern = 'process:scale'
        text_replacement = 'scalex:'+str(scale_x)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = '01_tapas-preprocess.txt'
        pattern = 'scalex:'+str(scale_x)
        text_replacement = 'scaley:'+str(scale_y)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)
    
        tapas_file = '01_tapas-preprocess.txt'
        pattern = 'process:cropZ'
        text_replacement = 'zMin:'+str(zMin)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = '01_tapas-preprocess.txt'
        pattern = 'zMin:'
        text_replacement = 'zMax:'+str(zMax)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


        tapas_file = '02a_tapas-cellpose.txt'
        pattern = "process:calibration"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\calibration\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = '02a_tapas-cellpose.txt'
        pattern = "process:exe"
        text_replacement = 'dir:'+path_to_tapas_scripts+'/../Models' + " \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = "//name"
        text_replacement = 'file:'+cellpose_name + " \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = 'all_measures_local.txt'
        pattern = "process:distanceLine"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\distance\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = 'all_measures_local.txt'
        pattern = "//coord"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\coordinates\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = 'all_measures_local.txt'
        pattern = "//volume"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\volume\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = 'all_measures_local.txt'
        pattern = "\\intensity"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\intensity\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = 'all_measures_local.txt'
        pattern = "process:calibrationSave"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\calibration\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)
    
    def open_project():
        file_path = filedialog.askopenfilename(title='Open a file',
            filetypes=[('YAML files', '*.yaml')]
            )
        with open(file_path, 'r') as file:
            project_data = yaml.safe_load(file)
        project_name=project_data['name']
        project_window = tk.Toplevel(root)
        project_window.geometry('700x700')
        project_window.title(f"Project {project_name}")
        project_window.columnconfigure([0,1,2], weight=1, minsize=50)
        project_window.rowconfigure([0,1,2,3,4,5,6,8,9,10,11], weight=1)

        #change paths in tapas files when  project is opened
        path_to_tapas_scripts=project_data["tapas_path"]
        specify_channel=project_data["image_channel"]
        scale_x=project_data["scale_x"]
        scale_y=project_data["scale_y"]
        zMin=project_data["z_cropmin"]
        zMax=project_data["z_cropmax"]
        path_to_folder=file_path.replace(project_name+'.yaml', '')
        name_extraction=project_name
        cellpose_name=project_data["cellpose_model"]
        initialise_project(path_to_tapas_scripts, specify_channel, scale_x, scale_y,zMin,zMax, path_to_folder, name_extraction+'extraction', cellpose_name)

        tk.Label(project_window, text="Project Name:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(project_window, text= project_name).grid(row=0, column=1, padx=10, pady=10)

        
        tk.Label(project_window, text="Save Location:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(project_window, text=path_to_folder).grid(row=1, column=1, padx=10, pady=10)


        tk.Label(project_window, text='Selected convention: ').grid(row=3, column=0, padx=10, pady=10)

        # Initialize the OptionMenu
        global convention_menu, selected_convention
        selected_convention = tk.StringVar(project_window)
        selected_convention.set(list(project_data['convention'].keys())[0])  # Set default value
        convention_menu = tk.OptionMenu(project_window, selected_convention, '')
        convention_menu.config(width=50)
        convention_menu.grid(row=3, column=1, padx=10, pady=10)

        add_convention_button = tk.Button(project_window, text="Add a convention", command=add_naming_convention)
        add_convention_button.grid(row=3, column=2, padx=10, pady=10)

        
        display_convention_label = tk.Label(project_window, text='')
        display_convention_label.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

        def on_option_change(*args):
            selected_value = selected_convention.get()
            if selected_value in data['convention']:
                conv = data['convention'][selected_value]['convention']
                sep = data['convention'][selected_value]['separator']
                display_convention_label.config(text=f"Selected convention: {conv}      separator: '{sep}'")
            else:
                display_convention_label.config(text='')

        selected_convention.trace("w", on_option_change)

        selected_ROI = tk.StringVar(project_window)
        selected_ROI.set('Select')
        
        ROI_menu=tk.OptionMenu(project_window, selected_ROI, *ROI_list)
        ROI_menu.grid(row=5, column=1, padx=10, pady=10)
        tk.Label(project_window, text="ROI: ").grid(row=5, column=0, padx=10, pady=10)

        tk.Label(project_window, text="Path to TAPAS scripts: ").grid(row=6, column=0, padx=10, pady=10, sticky='w')
        tapas_path_entry = tk.Entry(project_window, width=50)
        tapas_path_entry.grid(row=6, column=1, padx=10, pady=10)
        tapas_path_entry.insert(0, project_data['tapas_path'])

        def extract_project(path_to_folder, name_extraction, separator, structure, ID, ROI='line'):
            extract(path_to_folder, name_extraction, separator, structure, ID, ROI='line')

        def save_project():
            try:
                data = load_project_data(filename=file_path)
                project_data["tapas_path"]=tapas_path_entry.get()
                project_data["cellpose_model"]=cellpose_name_entry.get()
                project_data["image_channel"]=image_channel_entry.get()
                project_data["z_cropmin"]=z_cropmin_entry.get()
                project_data["z_cropmax"]=z_cropmax_entry.get()
                project_data["scale_x"]=scale_x_entry.get()
                project_data["scale_y"]=scale_y_entry.get()
                project_data["convention"]={selected_convention.get():
                                {'convention': data['convention'][selected_convention.get()]['convention'], 'separator': data['convention'][selected_convention.get()]['separator'], 'ID':data['convention'][selected_convention.get()]['ID']}}
                project_data['ROI']=selected_ROI.get()

                with open(file_path, 'w') as file:
                    yaml.safe_dump(project_data, file, default_flow_style=False)
                messagebox.showinfo("Success", f"Project {project_name} saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save project because of the following exception: {e}")

            
            #project_window.destroy()
        tk.Label(project_window, text="Cellpose model name: ").grid(row=7, column=0, padx=10, pady=10, sticky='w')
        cellpose_name_entry = tk.Entry(project_window, width=50)
        cellpose_name_entry.grid(row=7, column=1, padx=10, pady=10)
        cellpose_name_entry.insert(0, project_data['cellpose_model'])

        frame = tk.Frame(master=project_window, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=8, rowspan=4, columnspan=3)
        tk.Label(frame, text='Preprocessing').grid(row=8, column=1, padx=10, pady=10, sticky='w')
        tk.Label(frame, text='Channel to process: ').grid(row=9, column=0, padx=10, pady=10, sticky='w')
        image_channel_entry = tk.Entry(frame, width=10)
        image_channel_entry.grid(row=9, column=1, padx=10, pady=10, sticky='e')
        image_channel_entry.insert(0, project_data['image_channel'])

        tk.Label(frame, text='Z crop: ').grid(row=10, column=0, padx=10, pady=10, sticky='w')
        z_cropmin_entry = tk.Entry(frame, width=10)
        z_cropmin_entry.grid(row=10, column=1, padx=10, pady=10, sticky='e')
        z_cropmin_entry.insert(0, project_data['z_cropmin'])
        z_cropmax_entry = tk.Entry(frame, width=10)
        z_cropmax_entry.grid(row=10, column=2, padx=10, pady=10, sticky='e')
        z_cropmax_entry.insert(0, project_data['z_cropmax'])

        tk.Label(frame, text='Scale XY ').grid(row=11, column=0, padx=10, pady=10, sticky='w')
        scale_x_entry = tk.Entry(frame, width=10)
        scale_x_entry.grid(row=11, column=1, padx=10, pady=10, sticky='e')
        scale_x_entry.insert(0, project_data['scale_x'])
        scale_y_entry = tk.Entry(frame, width=10)
        scale_y_entry.grid(row=11, column=2, padx=10, pady=10, sticky='e')
        scale_y_entry.insert(0, project_data['scale_y'])

        save_button = tk.Button(project_window, text="Save Project", command=save_project)
        save_button.grid(row=12, column=1, pady=10)
        
        data = load_project_data(filename=data_path)
        extract_button = tk.Button(project_window, text="Extract data", command=lambda:extract_project(path_to_folder, project_name+'extraction', data['convention'][selected_convention.get()]['separator'], data['convention'][selected_convention.get()]['convention'], data['convention'][selected_convention.get()]['ID'], ROI=None))
        extract_button.grid(row=11, column=2, pady=10)
        # Initial load of options
        refresh_options()


        

    def save_convention(convention_name_entry, convention_entry, separator_entry, ID_entry):
        name = convention_name_entry.get()
        convention = convention_entry.get()
        separator = separator_entry.get()
        ID_txt = ID_entry.get()

        if not name:
            messagebox.showwarning("Input Error", "Convention name cannot be empty.")
            return

        if not convention:
            messagebox.showwarning("Input Error", "Convention entry cannot be empty.")
            return

        if not separator:
            messagebox.showwarning("Input Error", "Separator entry cannot be empty.")
            return
        
        if not ID_txt:
            messagebox.showwarning("Input Error", "ID entry cannot be empty.")
            return

        try:
            convention_list = convention.split(',')
            ID_list = ID_txt.split(',')
            with open(data_path, 'r') as f:
                data = yaml.safe_load(f)
            if 'convention' not in data:
                data['convention'] = {}
            data['convention'][name] = {'convention': convention_list, 'separator': separator, 'ID': ID_list}

            # Save the updated data back to the YAML file
            with open(data_path, 'w') as f:
                yaml.safe_dump(data, f)

            # Refresh the options in the OptionMenu
            refresh_options()

            messagebox.showinfo("Success", "Convention saved successfully!")
            convention_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")

    def add_naming_convention():
        global convention_window
        convention_window = tk.Toplevel(root)
        convention_window.geometry('700x150')
        convention_window.title("Add a naming convention")
        convention_window.columnconfigure([0,1,2,3], weight=1, minsize=50)
        convention_window.rowconfigure([0,1,2,3], weight=1)

        tk.Label(convention_window, text="Convention name: ").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        convention_name_entry = tk.Entry(convention_window, width=30)
        convention_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(convention_window, text="Convention:  ").grid(row=1, column=0, padx=10, pady=10)
        convention_entry = tk.Entry(convention_window, width=60)
        convention_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(convention_window, text="Separator: ").grid(row=1, column=2, padx=10, pady=10)
        separator_entry = tk.Entry(convention_window, width=3)
        separator_entry.grid(row=1, column=3, padx=10, pady=10, sticky='e')

        tk.Label(convention_window, text="ID: ").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        ID_entry = tk.Entry(convention_window, width=10)
        ID_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        save_convention_button = tk.Button(convention_window, text="Save", command=lambda: save_convention(convention_name_entry, convention_entry, separator_entry, ID_entry))
        save_convention_button.grid(row=2, column=3, padx=10, pady=10)

    def create_project():
        create_window = tk.Toplevel(root)
        create_window.geometry('700x700')
        create_window.title("Create New Project")
        create_window.columnconfigure([0,1,2], weight=1, minsize=50)
        create_window.rowconfigure([0,1,2,3,4,5,6,8,9,10,11], weight=1)

        tk.Label(create_window, text="Project Name:").grid(row=0, column=0, padx=10, pady=10)
        project_name_entry = tk.Entry(create_window, width=50)
        project_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(create_window, text="Save Location:").grid(row=1, column=0, padx=10, pady=10)
        folder_entry = tk.Entry(create_window, width=50)
        folder_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(create_window, text='Select a convention: ').grid(row=3, column=0, padx=10, pady=10)

        # Initialize the OptionMenu
        global convention_menu, selected_convention
        selected_convention = tk.StringVar(create_window)
        selected_convention.set('Select')  # Set default value
        convention_menu = tk.OptionMenu(create_window, selected_convention, '')
        convention_menu.config(width=50)
        convention_menu.grid(row=3, column=1, padx=10, pady=10)

        add_convention_button = tk.Button(create_window, text="Add a convention", command=add_naming_convention)
        add_convention_button.grid(row=3, column=2, padx=10, pady=10)

        
        display_convention_label = tk.Label(create_window, text='')
        display_convention_label.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

        def on_option_change(*args):
            data = load_project_data(filename=data_path)
            selected_value = selected_convention.get()
            if selected_value in data['convention']:
                conv = data['convention'][selected_value]['convention']
                sep = data['convention'][selected_value]['separator']
                display_convention_label.config(text=f"Selected convention: {conv}      separator: '{sep}'")
            else:
                display_convention_label.config(text='')

        selected_convention.trace("w", on_option_change)

        selected_ROI = tk.StringVar(create_window)
        selected_ROI.set('Select')

        ROI_menu=tk.OptionMenu(create_window, selected_ROI, *ROI_list)

        ROI_menu.grid(row=5, column=1, padx=10, pady=10)
        tk.Label(create_window, text="ROI: ").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(create_window, text="Path to TAPAS scripts: ").grid(row=6, column=0, padx=10, pady=10, sticky='w')
        tapas_path_entry = tk.Entry(create_window, width=50)
        tapas_path_entry.grid(row=6, column=1, padx=10, pady=10)
        tapas_path_entry.insert(0, tapas_path)

        browse_button = tk.Button(create_window, text="Browse", command=lambda: folder_entry.insert(0, filedialog.askdirectory(title="Select a Folder to Save Project")))
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
                data = load_project_data(filename=data_path)
                project_info = {
                    "name": project_name,
                    "date created":time.strftime("%A %d %B %Y %H:%M:%S"),
                    
                    "convention": {selected_convention.get():
                                {'convention': data['convention'][selected_convention.get()]['convention'], 'separator': data['convention'][selected_convention.get()]['separator'], 'ID':data['convention'][selected_convention.get()]['ID']}
                    },
                    "tapas_path": tapas_path_entry.get(),
                    "cellpose_model": cellpose_name_entry.get(),
                    "image_channel": image_channel_entry.get(),
                    "z_cropmin": z_cropmin_entry.get(),
                    "z_cropmax": z_cropmax_entry.get(),
                    "scale_x":scale_x_entry.get(),
                    "scale_y":scale_y_entry.get(),
                    "ROI":selected_ROI.get()

                }
                with open(os.path.join(project_path, f"{project_name}.yaml"), 'w') as file:
                    yaml.dump(project_info, file, default_flow_style=False)

                project_tapas_path=os.path.join(project_path, "TAPAS")
                os.makedirs(project_tapas_path)
                for file in os.listdir(data['tapas_path']):
                    copy2(os.path.join(data['tapas_path'], file), project_tapas_path)

                initialise_project(project_tapas_path, image_channel_entry.get(), scale_x_entry.get(), scale_y_entry.get(),z_cropmin_entry.get(),z_cropmax_entry.get(), project_path, project_name+'extraction', cellpose_name_entry.get())
                messagebox.showinfo("Success", f"Project '{project_name}' created at: {project_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create project because of the following exception: {e}")

            #create_window.destroy()
        tk.Label(create_window, text="Cellpose model name: ").grid(row=7, column=0, padx=10, pady=10, sticky='w')
        cellpose_name_entry = tk.Entry(create_window, width=50)
        cellpose_name_entry.grid(row=7, column=1, padx=10, pady=10)
        cellpose_name_entry.insert(0, cellpose_model)

        frame = tk.Frame(master=create_window, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=8, rowspan=4, columnspan=3)
        tk.Label(frame, text='Preprocessing').grid(row=8, column=1, padx=10, pady=10, sticky='w')
        tk.Label(frame, text='Channel to process: ').grid(row=9, column=0, padx=10, pady=10, sticky='w')
        image_channel_entry = tk.Entry(frame, width=10)
        image_channel_entry.grid(row=9, column=1, padx=10, pady=10, sticky='e')
        image_channel_entry.insert(0, 1)

        tk.Label(frame, text='Z crop: ').grid(row=10, column=0, padx=10, pady=10, sticky='w')
        z_cropmin_entry = tk.Entry(frame, width=10)
        z_cropmin_entry.grid(row=10, column=1, padx=10, pady=10, sticky='e')
        z_cropmin_entry.insert(0, 0)
        z_cropmax_entry = tk.Entry(frame, width=10)
        z_cropmax_entry.grid(row=10, column=2, padx=10, pady=10, sticky='e')
        z_cropmax_entry.insert(0, 18)

        tk.Label(frame, text='Scale XY ').grid(row=11, column=0, padx=10, pady=10, sticky='w')
        scale_x_entry = tk.Entry(frame, width=10)
        scale_x_entry.grid(row=11, column=1, padx=10, pady=10, sticky='e')
        scale_x_entry.insert(0, 1)
        scale_y_entry = tk.Entry(frame, width=10)
        scale_y_entry.grid(row=11, column=2, padx=10, pady=10, sticky='e')
        scale_y_entry.insert(0, 1)

        save_button = tk.Button(create_window, text="Create Project", command=save_project)
        save_button.grid(row=12, columnspan=3, pady=10)

        # Initial load of options
        refresh_options()

    def load_project_data(filename):
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def load_options_from_yaml():
        """Load options from a YAML file."""
        with open(data_path, 'r') as f:
            data = yaml.safe_load(f)
        return list(data['convention'].keys())

    def update_option_menu(new_options):
        """Update the OptionMenu with new options."""
        # Clear the current options
        convention_menu['menu'].delete(0, 'end')
        for option in new_options:
            convention_menu['menu'].add_command(label=option, command=tk._setit(selected_convention, option))
    """    if new_options:
            selected_convention.set(new_options[0])  # Set default value"""

    def refresh_options():
        """Refresh options from the YAML file."""
        new_options = load_options_from_yaml()
        update_option_menu(new_options)

    # Initialize global data and path
    global data
    root = os.path.dirname(__file__)
    created_path=os.path.join(root,'data', 'created.yaml')#access the path of the MarsCell folder
    try:
        created = load_project_data(filename=created_path)
        data_path=created['file_path']
        data=load_project_data(filename=data_path)

        
    except Exception as e:
        print('Error while loading data file because of the following exception: ', e)



    tapas_path = data.get("tapas_path", "")
    cellpose_model = data.get("cellpose_model", "")

    # Create main window
    root = tk.Tk()
    root.title("MarCell")
    root_width = 400
    root_height = 200 

    # Get the screen's width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width // 2) - (root_width // 2)
    y = (screen_height // 2) - (root_height // 2)

    # Set the geometry of the window
    root.geometry(f"{root_width}x{root_height}+{x}+{y}")

    # Create a label for the welcome message
    welcome_label = tk.Label(root, text="Welcome to MarCell", font=("ComicSansMS", 24))
    welcome_label.pack(pady=20)
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)  # Add some padding above the frame


    # Pack the buttons in the frame, aligned to the left and right


    # Prevent the frame from resizing itself to fit the widgets
    create_button = ttk.Button(button_frame, text="Create Project", command=create_project)


    open_button = ttk.Button(button_frame, text="Open Project", command=open_project)


    create_button.pack(side=tk.LEFT, padx=20)  # Add some padding to the sides
    open_button.pack(side=tk.RIGHT, padx=20)
    copyright_label = tk.Label(root, text="☕ 2024 MarCell", font=("Arial", 10))
    copyright_label.pack(side=tk.BOTTOM, pady=5)

    root.mainloop()
