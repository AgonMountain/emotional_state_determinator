from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import io
from tkinter import ttk
import tkinter as tk
from model.pose_manager import PoseManager


class PoseTablePlayer:

    def __init__(self, app, window, player_height, player_width):
        self.app = app
        self.window = window

        self.player_height = player_height
        self.player_width = player_width

        self.row_table_id = None

        vertical_scrollbar = ttk.Scrollbar(window)
        vertical_scrollbar.pack(side=RIGHT, fill=Y)
        self.table = ttk.Treeview(window, yscrollcommand=vertical_scrollbar.set)
        self.table.pack()

        vertical_scrollbar.config(command=self.table.yview)

        style = ttk.Style(root)
        style.theme_use("winnative")
        style.configure(".", font=("Helvetica", 11))
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

        self.table['columns'] = ("id", "data")
        self.table.column("#0", width=0, stretch='NO')
        self.table.column("id", width=50, anchor='w')
        self.table.column("data", width=130, anchor='w')

        self.table.heading("#0", anchor='w', text='Label')
        self.table.heading("id", anchor='w', text="Id")
        self.table.heading("data", anchor='w', text="Image")

        count = 0

        for record in range(50):
            # print(record)
            self.table.insert(parent='', index='end', iid=count, text='Parent',
                           values=(record, count))
            count += 1



if __name__ == '__main__':
    root = tk.Tk()
    img = ImageTk.PhotoImage(Image.open("../model/1.jpg")) # replace with your image
    label_grid = PoseTablePlayer(0, root, 600, 600)

    tk.mainloop()







