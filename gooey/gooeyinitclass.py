#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 29 15:05:28 2025

@author: annax
WEEKLY SALE initializer (GOOEY)

in the main gooey we create an instance of this app class to start the app
"""


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GRAPHIC ASSISTANT")
        self.geometry("1000x600")

        # app state
        self.state = AppState(IMAGES_DIR)

        # container holds current frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}  # keeps all pages

        for F in (StartPage, ProcessImagesPage, CreateFlyerPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # all frames are stacked but only one is shown
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Raise the frame by name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Welcome!", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(self, text="Process Images",
                  command=lambda: controller.show_frame("ProcessImagesPage")).pack(pady=10)

        tk.Button(self, text="Create Graphic Flyer",
                  command=lambda: controller.show_frame("CreateFlyerPage")).pack(pady=10)

class ProcessImagesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Images Root Folder")
        if folder:
            self.controller.state.images_dir = folder
            messagebox.showinfo("Done", f"Set images directory to:\n{folder}")

class CreateFlyerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Create Graphic Flyer", font=("Helvetica", 14)).pack(pady=10)

        #tk.Button(self, text="Select Excel File", command=self.select_excel).pack(pady=10)

        tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage")).pack(pady=10)
        
        self.controller = controller

"""    def select_excel(self):
        excel_file = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if excel_file:
            basename = os.path.basename(excel_file)
            collage = make_collage(basename)
            if collage:
                u_choose_images(collage, self.controller.state)
                make_n_save_graphic(collage)
                messagebox.showinfo("Success", "Flyer created and saved!")
            else:
                messagebox.showerror("Error", "Failed to create flyer.")"""