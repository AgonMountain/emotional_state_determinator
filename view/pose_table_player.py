from PIL import ImageTk, Image
from tkinter import ttk
import tkinter as tk


class PoseTablePlayer:

    def __init__(self, app, window, player_height, player_width):
        self.app = app
        self.window = window
        self.player_height = player_height
        self.player_width = player_width
        self.selected_row = None
        self.pose_id = None

        self.__frame_control_panel = tk.Frame(self.window, height=self.player_height, width=self.player_width)
        self.__bt_create = tk.Button(self.__frame_control_panel, text="Добавить", state='normal')
        self.__bt_update = tk.Button(self.__frame_control_panel, text="Обновить", state='disabled',
                                     command=self.__update_pose)
        self.__bt_delete = tk.Button(self.__frame_control_panel, text="Удалить", state='disabled')

        self.__frame_table = tk.Frame(self.window, height=self.player_height, width=self.player_width)
        self.table = ttk.Treeview(self.__frame_table, selectmode='browse')
        self.table.pack(side=tk.LEFT)
        vertical_scrollbar = ttk.Scrollbar(self.__frame_table, orient="vertical", command=self.table.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.config(yscrollcommand=vertical_scrollbar.set, height=4)
        self.table.bind('<ButtonRelease-1>', self.__select_table_item)

        self.style = ttk.Style(self.__frame_table)
        self.style.theme_use("winnative")
        self.style.configure(".", font=("Helvetica", 11))
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        self.style.configure("Treeview", rowheight=130)

        self.table['columns'] = ("#1", "#2", "#3")
        self.table.column("#0", width=220, stretch='NO')
        self.table.column("#1", width=200, anchor='w')
        self.table.column("#2", width=200, anchor='w')
        self.table.column("#3", width=300, anchor='w')

        self.table.heading("#0", anchor='w', text='Изображение')
        self.table.heading("#1", anchor='w', text="Оценка")
        self.table.heading("#2", anchor='w', text="Описание")
        self.table.heading("#3", anchor='w', text="Дата последнего изменения")

        self.img_list = {}
        for pose in self.app.get_poses():
            p = pose.get_img_path()
            img = Image.open(p)
            img.thumbnail((180, 180))
            self.img_list[pose.get_id()] = ImageTk.PhotoImage(img)
            self.table.insert(parent='', index='end', text="", image=self.img_list[pose.get_id()],
                              values=(pose.get_state(), pose.get_id(), pose.get_recent_change_date_time(), pose.get_id()))

        self.__pack_and_place()

    def __pack_and_place(self):
        self.__frame_control_panel.place(x=0, y=10)
        self.__bt_create.place(x=200, y=0)
        self.__bt_update.place(x=400, y=0)
        self.__bt_delete.place(x=600, y=0)
        self.__frame_table.place(x=0, y=50)

    def __activate_deactivate_buttons(self):
        self.__bt_create.configure(state='disabled' if self.selected_row is not None else 'normal')
        self.__bt_delete.configure(state='normal' if self.selected_row is not None else 'disabled')
        self.__bt_update.configure(state='normal' if self.selected_row is not None else 'disabled')

    def __select_table_item(self, e):
        self.selected_row = self.table.focus() if self.selected_row != self.table.focus() else None
        self.pose_id = self.table.item(self.table.focus())['values'][3] if self.selected_row is not None else None

        if self.selected_row is None and len(self.table.selection()) > 0:
            self.table.selection_remove(self.table.selection()[0])

        self.__activate_deactivate_buttons()

    def __update_pose(self):
        self.app.update_pose(self.pose_id)
