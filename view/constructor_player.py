import re
import tkinter as tk
from tkinter import ttk
from config.config import *
from view.img_player import ImgPlayer
from view.pose_table_player import PoseTablePlayer

class ConstructorPlayer:

    def __init__(self, app, window, constructor_player_height, constructor_player_width, emotional_states, poses):
        self.emotional_states = emotional_states

        self.app = app
        self.constructor_player_height = constructor_player_height
        self.constructor_player_width = constructor_player_width

        self.frame_pose_table_player = tk.Frame(window, height=self.constructor_player_height,
                                                width=self.constructor_player_width)
        self.pose_table_player = PoseTablePlayer(self, self.frame_pose_table_player,
                                                 constructor_player_height, constructor_player_width)

        self.active_frame = self.frame_pose_table_player

        size = 0.8
        self.img_player_height = constructor_player_height * size
        self.img_player_width = constructor_player_width * size

        self.frame_editor = tk.Frame(window, height=self.constructor_player_height,
                                       width=self.constructor_player_width)

        self.frame_controls = tk.Frame(self.frame_editor, height=self.constructor_player_height, width=self.constructor_player_width)
        self.img_canvas = tk.Canvas(self.frame_controls, width=self.img_player_width, height=self.img_player_height)
        self.img_canvas.create_rectangle(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, fill='black')
        self.img_player = ImgPlayer(self.app, self.img_canvas, self.img_player_height, self.img_player_width)
        self.bt_save = tk.Button(self.frame_controls, text="Сохранить", command=self.save)
        self.bt_cancel = tk.Button(self.frame_controls, text="Отмена", command=self.__cancel_edit_pose)

        # ==========
        self.frame_emotional_state = tk.Frame(self.frame_editor, height=60, width=175)
        self.label_emotional_state = tk.Label(self.frame_emotional_state, text="Оценка состояния:")
        self.field_emotional_state = ttk.Combobox(self.frame_emotional_state, values=self.emotional_states, width=18, state="readonly")
        self.field_emotional_state.set(self.emotional_states[0])

        # ==========
        self.frame_body_inaccuracy = tk.Frame(self.frame_editor, height=100, width=175)
        self.label_body_inaccuracy = tk.Label(self.frame_body_inaccuracy, text="Погрешность углов тела:")
        self.field_body_inaccuracy = tk.Entry(self.frame_body_inaccuracy, justify="right", width=15)
        self.label_body_inaccuracy_px = tk.Label(self.frame_body_inaccuracy, text="гр.")
        self.bt_show_body_inaccuracy = tk.Button(self.frame_body_inaccuracy, text="Показать погрешность", command=self.show_body_inaccuracy)

        # ==========
        self.frame_right_hand_inaccuracy = tk.Frame(self.frame_editor, height=130, width=175)
        self.label_right_hand_inaccuracy = tk.Label(self.frame_right_hand_inaccuracy, text="Погрешность точек\nправой руки:")
        self.field_right_hand_inaccuracy = tk.Entry(self.frame_right_hand_inaccuracy, justify="right", width=15)
        self.label_right_hand_inaccuracy_px = tk.Label(self.frame_right_hand_inaccuracy, text="px")
        self.bt_right_hand_inaccuracy = tk.Button(self.frame_right_hand_inaccuracy, text="Показать погрешность", command=self.show_body_inaccuracy)

        self.frame_left_hand_inaccuracy = tk.Frame(self.frame_editor, height=130, width=175)
        self.label_left_hand_inaccuracy = tk.Label(self.frame_left_hand_inaccuracy, text="Погрешность точек\nлевой руки:")
        self.field_left_hand_inaccuracy = tk.Entry(self.frame_left_hand_inaccuracy, justify="right", width=15)
        self.label_left_hand_inaccuracy_px = tk.Label(self.frame_left_hand_inaccuracy, text="px")
        self.bt_left_hand_inaccuracy = tk.Button(self.frame_left_hand_inaccuracy, text="Показать погрешность",
                                                  command=self.show_body_inaccuracy)

        self.pack_and_place()

    def pack_and_place(self):
        self.active_frame.place(x=0, y=0)

        self.frame_controls.place(x=0, y=0)
        self.frame_emotional_state.place(x=self.img_player_width + 10, y=10)
        self.frame_body_inaccuracy.place(x=self.img_player_width + 10, y=80)
        self.frame_right_hand_inaccuracy.place(x=self.img_player_width + 10, y=190)
        self.frame_left_hand_inaccuracy.place(x=self.img_player_width + 10, y=320)

        self.img_canvas.place(x=0, y=0)

        self.label_emotional_state.place(x=0, y=0)
        self.field_emotional_state.place(x=0, y=30)

        self.label_body_inaccuracy.place(x=0, y=0)
        self.field_body_inaccuracy.place(x=0, y=30)
        self.label_body_inaccuracy_px.place(x=130, y=30)
        self.bt_show_body_inaccuracy.place(x=0, y=60)

        self.label_right_hand_inaccuracy.place(x=0, y=0)
        self.field_right_hand_inaccuracy.place(x=0, y=50)
        self.label_right_hand_inaccuracy_px.place(x=130, y=50)
        self.bt_right_hand_inaccuracy.place(x=0, y=80)

        self.label_left_hand_inaccuracy.place(x=0, y=0)
        self.field_left_hand_inaccuracy.place(x=0, y=50)
        self.label_left_hand_inaccuracy_px.place(x=130, y=50)
        self.bt_left_hand_inaccuracy.place(x=0, y=80)

        # self.label_poses.place(x=0, y=0)
        # self.field_poses.place(x=0, y=50)

        self.bt_save.place(x=150, y=self.img_player_height + 10)
        self.bt_cancel.place(x=250, y=self.img_player_height + 10)
        # self.bt_update.place(x=300, y=self.img_player_height + 10)
        # self.bt_delete.place(x=450, y=self.img_player_height + 10)

    def __switch_to_table(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_pose_table_player
        self.active_frame.place(x=0, y=0)

    def __switch_to_editor(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_editor
        self.active_frame.place(x=0, y=0)

    def get_poses(self):
        return self.app.get_poses()

    def update_pose(self, pose_id):
        self.__switch_to_editor()
        self.pose_changed(pose_id)

    def __cancel_edit_pose(self):
        self.__switch_to_table()

    def save(self):
        img, label, data = self.app.classify_pose(self.app.get_img())
        for i in data['angels']:
            d = self.field_body_inaccuracy.get()
            if d is '':
                d = '0'
            data['angels'][i] = [data['angels'][i], int(d)]

        for i in data['distances']:
            r = self.field_right_hand_inaccuracy.get()
            if r is '':
                r = '0'
            l = self.field_left_hand_inaccuracy.get()
            if l is '':
                l = '0'
            if "right" in i:
                data['distances'][i] = [data['distances'][i], int(r)]
            else:
                data['distances'][i] = [data['distances'][i], int(l)]

        pose_names = self.app.create_pose(self.img_player.get_img(), self.field_emotional_state.get(),
                                          data['angels'], data['distances'], data['crossings'], '')

        self.field_poses.config(values=pose_names)
        # self.field_poses.set(pose_names[0])

    def update(self):
        return 0

    def delete(self):
        name = self.field_poses.get()

        id = int(re.findall(r'\d+', name)[0])

        pose_names = self.app.delete_pose(id)
        self.field_poses.config(values=pose_names)
        self.field_poses.set(pose_names[0])

    def show_body_inaccuracy(self):
        return 0

    def pose_changed(self, id):
        pose_image, pose_data = self.app.get_pose(id)

        self.img_player.load_img(pose_image)

        if pose_data is not None:
            self.set_fields(pose_data.get_state(), 0, 0, 0)
        else:
            self.set_fields(self.emotional_states[0], "0", "0", "0")

    def load_img(self, image):
        self.img_player.load_img(image)

    def set_fields(self, field_emotional_state, field_body_inaccuracy, field_left_hand_inaccuracy,
                   field_right_hand_inaccuracy):

        self.field_emotional_state.set(field_emotional_state)

        self.field_body_inaccuracy.delete(0, 'end')
        self.field_left_hand_inaccuracy.delete(0, 'end')
        self.field_right_hand_inaccuracy.delete(0, 'end')

        self.field_body_inaccuracy.insert(0, field_body_inaccuracy)
        self.field_left_hand_inaccuracy.insert(0, field_left_hand_inaccuracy)
        self.field_right_hand_inaccuracy.insert(0, field_right_hand_inaccuracy)
