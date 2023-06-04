import numpy
import numpy as np
from PIL import ImageTk, Image
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import textwrap

class PoseTablePlayer:

    def __init__(self, constructor_app, window, player_height, player_width):
        self.__constructor_app = constructor_app
        self.selected_row = None
        self.pose_id = None

        self.player_width = player_width
        self.player_height = player_height

        self.__frame_control_panel = tk.Frame(window, height=player_height, width=player_width)
        self.__bt_create = tk.Button(self.__frame_control_panel, text="Добавить новую", state='normal',
                                     command=self.__go_to_create_pose)
        self.__bt_update = tk.Button(self.__frame_control_panel, text="Редактировать выбранную", state='disabled',
                                     command=self.__go_to_update_pose)
        self.__bt_delete = tk.Button(self.__frame_control_panel, text="Удалить выбранную", state='disabled',
                                     command=self.__delete_pose)

        self.__label_all_pose_number = tk.Label(self.__frame_control_panel, text="Количество поз: 0 / 50")

        self.__frame_table = tk.Frame(window, height=player_height, width=player_width)
        self.table = ttk.Treeview(self.__frame_table, selectmode='browse')
        self.table.pack(side=tk.LEFT)
        self.vertical_scrollbar = ttk.Scrollbar(self.__frame_table, orient="vertical", command=self.table.yview)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.config(yscrollcommand=self.vertical_scrollbar.set, height=4)
        self.table.bind('<ButtonRelease-1>', self.__select_table_item)

        self.style = ttk.Style(self.__frame_table)
        self.style.theme_use("winnative")
        self.style.configure(".", font=("Helvetica", 11))
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        self.style.configure("Treeview", rowheight=130)

        self.table['columns'] = ("#1", "#2", "#3", '#4')
        self.table.column("#0", width=200, stretch='NO')
        self.table.column("#1", width=50, anchor='w')
        self.table.column("#2", width=180, anchor='w')
        self.table.column("#3", width=360, anchor='w')
        self.table.column("#4", width=140, anchor='w')

        self.table.heading("#0", anchor='w', text='Изображение')
        self.table.heading("#1", anchor='w', text='id')
        self.table.heading("#2", anchor='w', text="Оценка")
        self.table.heading("#3", anchor='w', text="Описание")
        self.table.heading("#4", anchor='w', text="Изменено")

        self.reload_table()

        self.__pack_and_place()

    def __pack_and_place(self):
        self.__frame_control_panel.place(x=0, y=10)
        self.__label_all_pose_number.place(x=0, y=35)
        self.__bt_create.place(x=self.player_width-555, y=30)
        self.__bt_update.place(x=self.player_width-400, y=30)
        self.__bt_delete.place(x=self.player_width-170, y=30)
        self.__frame_table.place(x=0, y=100)

    def __resize_img(self, image, base_width, base_height):
        width_percent = (base_width / float(image.size[0]))
        height_percent = (base_height / float(image.size[1]))

        height_size = int(float(image.size[1]) * float(width_percent))
        width_size = int(float(image.size[0]) * float(height_percent))

        if width_percent < height_percent:
            img = image.resize((base_width, height_size), Image.Resampling.LANCZOS)
        elif width_percent > height_percent:
            img = image.resize((width_size, base_height), Image.Resampling.LANCZOS)
        elif width_percent == height_percent != 1.0:
            img = image.resize((width_size, height_size), Image.Resampling.LANCZOS)
        else:
            img = image

        return numpy.array(img)

    def reload_table(self):
        self.table.delete(*self.table.get_children())
        self.img_list = {}
        for pose in self.__constructor_app.get_poses():
            p = pose.get_img_path()
            img = Image.open(p)
            img = Image.fromarray(self.__resize_img(img, 180, 100))
            self.img_list[pose.get_pose_id()] = ImageTk.PhotoImage(img)
            self.table.insert(parent='', index='end', text="", image=self.img_list[pose.get_pose_id()],
                              values=(pose.get_pose_id(),
                                      pose.get_state().replace(' ', '\n'),
                                      self.comment(pose.get_pose_description()),
                                      pose.get_recent_change_date_time().replace(' ', '\n'),
                                      pose.get_pose_id()))
        self.__label_all_pose_number.config(text=f'Количество заданных поз: {len(self.img_list)} / 50')

    def comment(self, text):
        str = ''
        str_end = ''
        if len(text) > 0:
            w = textwrap.wrap(text, 35)
            if len(w) > 4:
                w = w[:4]
                str_end = '...'
            for t in w:
                str += t + '\n'
            str = str[:-1]
        else:
            str = 'Отсутствует описание у позы.'
        return str + str_end

    def __activate_deactivate_buttons(self):
        self.__bt_create.configure(state='disabled' if self.selected_row is not None else 'normal')
        self.__bt_delete.configure(state='normal' if self.selected_row is not None else 'disabled')
        self.__bt_update.configure(state='normal' if self.selected_row is not None else 'disabled')

    def __select_table_item(self, e):
        self.selected_row = self.table.focus() if (self.selected_row != self.table.focus() and self.table.focus() != '') else None
        self.pose_id = self.table.item(self.table.focus())['values'][0] if self.selected_row is not None else None

        if self.selected_row is None and len(self.table.selection()) > 0:
            self.table.selection_remove(self.table.selection()[0])

        self.__activate_deactivate_buttons()

    def __go_to_update_pose(self):
        self.__constructor_app.go_to_update_pose(self.pose_id)

    def __go_to_create_pose(self):
        self.__constructor_app.go_to_create_pose()

    def __delete_pose(self):
        delete = messagebox.askquestion("Подтвердите удаление", f"Вы действительно хотите безвозвратно удалить "
                                                                f"позу с id {self.pose_id} ?\n")
        if delete == 'yes':
            self.__constructor_app.delete_pose(self.pose_id)

        self.selected_row = None
        self.pose_id = None
        self.__activate_deactivate_buttons()
