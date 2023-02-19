from tkinter import *
from tkinter.ttk import *
from tk_models import *
from scrollable_frame import ScrolledFrame
from experiment_pages.summary_ui import SummaryUI
from experiment_pages.experiment import Experiment

class GroupConfigUI(MouserPage):
    def __init__(self, input: Experiment, parent:Tk, prev_page: Frame, menu_page: Frame):
        super().__init__(parent, "New Experiment - Group Configuration", prev_page)

        self.input = input

        self.next_page = SummaryUI(self.input, parent, self, menu_page)
        self.set_next_button(self.next_page)

        scroll_canvas = ScrolledFrame(self, width=410, height=400)
        scroll_canvas.place(relx=0.27, rely=0.25)

        self.main_frame = Frame(scroll_canvas)
        self.main_frame.grid(row=2, column=1, sticky='NESW')

        self.group_frame = Frame(self.main_frame)
        self.item_frame = Frame(self.main_frame)

        self.group_frame.grid(row=0, column=0, sticky='NESW')
        self.item_frame.grid(row=1, column=0, sticky='NESW')

        self.create_group_entries(int(self.input.get_num_groups()))
        self.create_item_frame(self.input.get_measurement_items())

        for i in range(0,2):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)


    def set_next_button(self, next_page):
        if self.next_button:
            self.next_button.destroy()
        self.next_button = ChangePageButton(self, next_page, False)
        self.next_button.configure(command= lambda: [self.save_input(), self.next_button.navigate()])
        self.next_button.place(relx=0.85, rely=0.15)


    def create_group_entries(self, num):
        Label(self.group_frame, text="Group Name").grid(row=0, column=0, padx=10, pady=10)
        self.group_input = []
        for i in range(0, num):
            name = Entry(self.group_frame, width = 40)
            name.grid(row=i+1, column=0, padx=10, pady=10)
            self.group_input.append(name)

    
    def create_item_frame(self, items):
        self.button_vars = [] 
        self.item_auto_buttons = []
        self.item_man_buttons = []
        for i in range(0, len(items)):
            self.type = BooleanVar()
            self.button_vars.append(self.type)
            
            Label(self.item_frame, text=items[i]).grid(row=i, column=0, padx=10, pady=10, sticky=W)
            auto = Radiobutton(self.item_frame, text='Automatic', variable=self.type, val=True)
            man = Radiobutton(self.item_frame, text='Manual', variable=self.type, val=False)
            
            auto.grid(row=i, column=1, padx=10, pady=10)
            man.grid(row=i, column=2, padx=10, pady=10)

            self.item_auto_buttons.append(auto)
            self.item_man_buttons.append(man)


    def update_page(self):
        for widget in self.group_frame.winfo_children():
            widget.destroy()
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        self.create_group_entries(int(self.input.get_num_groups()))
        self.create_item_frame(self.input.get_measurement_items())


    def save_input(self):
        group_names = []
        for entry in self.group_input:
            group_names.append(entry.get())
            self.input.group_names = group_names
            
        items = self.input.get_measurement_items()
        measurment_collect_type = []
        for i in range(0, len(items)):
            measurment_collect_type.append((items[i], self.button_vars[i].get()))

        self.input.data_collect_type = measurment_collect_type
        self.next_page.update_page()

        