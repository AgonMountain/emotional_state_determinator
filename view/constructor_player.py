import re
import tkinter as tk
from tkinter import ttk
from config.config import *
from view.img_player import ImgPlayer
from view.pose_table_player import PoseTablePlayer
from view.editor_player import EditorPlayer


class ConstructorPlayer:

    def __init__(self, app, window, constructor_player_height, constructor_player_width):
        self.app = app
        self.constructor_player_height = constructor_player_height
        self.constructor_player_width = constructor_player_width

        self.frame_pose_table_player = tk.Frame(window,
                                                height=self.constructor_player_height,
                                                width=self.constructor_player_width)

        self.pose_table_player = PoseTablePlayer(self,
                                                 self.frame_pose_table_player,
                                                 constructor_player_height,
                                                 constructor_player_width)

        self.frame_editor = tk.Frame(window,
                                     height=self.constructor_player_height,
                                     width=self.constructor_player_width)

        self.editor = EditorPlayer(self,
                                   self.frame_editor,
                                   height=self.constructor_player_height,
                                   width=self.constructor_player_width,
                                   states=list(self.app.get_states().keys()),
                                   inaccuracy=list(self.app.get_inaccuracy().keys()))

        self.active_frame = self.frame_pose_table_player
        self.pack_and_place()

    def pack_and_place(self):
        self.active_frame.place(x=0, y=0)

    def switch_to_table(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_pose_table_player
        self.active_frame.place(x=0, y=0)

    def __switch_to_editor(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_editor
        self.active_frame.place(x=0, y=0)

    def get_poses(self):
        return self.app.get_poses()

    def load_img(self, img):
        self.editor.load_image_for_new_pose(img)

    def go_to_update_pose(self, pose_id):
        self.__switch_to_editor()
        pose_image, pose_data = self.get_pose(pose_id)

        inaccuracy = self.app.get_inaccuracy()
        inaccuracy = list(inaccuracy.keys())[list(inaccuracy.values()).index(pose_data.inaccuracy)]
        self.editor.set_active_exists_pose(id=pose_id,
                                           pil_image=pose_image,
                                           state=pose_data.state,
                                           description=pose_data.pose_description,
                                           inaccuracy=inaccuracy)

    def go_to_create_pose(self):
        self.__switch_to_editor()

    def cancel_edit_pose(self):
        self.switch_to_table()

    def create_pose(self, image, state, inaccuracy, pose_description):

        self.app.create_pose(image=image,
                             state=state,
                             inaccuracy=inaccuracy,
                             pose_description=pose_description)

        self.pose_table_player.reload_table()
        self.switch_to_table()

    def update_pose(self, id, image, state, inaccuracy, pose_description):

        self.app.update_pose(id=id,
                             image=image,
                             state=state,
                             inaccuracy=inaccuracy,
                             description=pose_description)

        self.pose_table_player.reload_table()
        self.switch_to_table()

    def delete_pose(self, pose_id):
        self.app.delete_pose(pose_id)
        self.pose_table_player.reload_table()

    def classify_pose(self, image):
        return self.app.classify_pose(image)

    def get_pose(self, pose_id):
        return self.app.get_pose(pose_id)
