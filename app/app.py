from tkinter import Tk, Label, Button, Entry, Text, W
from tkinter.ttk import Combobox, Checkbutton
import yaml


class MainApp(Tk):
    def __init__(self):
        super().__init__()
        g, available_cities = self.read_config()
        self.geometry(f'{g["width"]}x{g["height"]}')

        self.label_car = Label(self, text="Write name of car", justify='right')
        self.label_city = Label(self, text="Type city where search a car")
        self.vehicle_name = Entry(self)
        self.cities = Combobox(self)
        self.field_to_results = Text()

        # TODO: add functionality to get info for some cars at some time
        self.make_one_df = Checkbutton(self, text='Make one frame for cars')

        self.confirm_button = Button(self, text='Confirm', command=self.clicked)

        self.create_widgets(available_cities)

    def create_widgets(self, available_cities):
        
        self.cities['values'] = available_cities
        self.cities.current(0)

        ### grid settings
        # TODO: replace method grid to place
        self.label_car.grid(column=0, row=0)
        self.vehicle_name.grid(column=1, row=0)
        self.label_city.grid(column=2, row=0)
        self.cities.grid(column=3, row=0)
        self.field_to_results.grid(column=1, row=3)
        self.confirm_button.grid(column=3, row=5)

    @staticmethod
    def read_config():
        with open('../configs/CONFIG.yaml') as cfg:
            data = yaml.safe_load(cfg)
            available_cities = data['available_cities']
            main_geometry = data['win_geometry']
        return main_geometry, available_cities

    def clicked(self):
        """
        Checks are all fields for text including text
        if not returns Error, else None
        """
        ...
        # self.label_city.config(text="GG")


root = MainApp()

if __name__ == '__main__':
    root.mainloop()
