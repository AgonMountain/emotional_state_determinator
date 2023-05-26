import tkinter as tk
from tkinter import ttk
from view.image_player import ImgPlayer


class EditorPlayer:

    def __init__(self, constructor_app, window, height, width, states, inaccuracy):
        self.__constructor_app = constructor_app
        self.__editor_player_height = height
        self.__editor_player_width = width
        self.__states = states
        self.__inaccuracy = inaccuracy

        self.compression_ratio = 0.8
        self.img_player_height = height * self.compression_ratio
        self.img_player_width = width * self.compression_ratio

        self.frame_editor = tk.Frame(window, height=self.__editor_player_height, width=self.__editor_player_width)

        self.frame_description = tk.Frame(self.frame_editor, height=100, width=width)
        self.label_description = tk.Label(self.frame_description, text='Описание позы:')
        self.text_description = tk.Text(self.frame_description, width=int(width/10), height=3, wrap=tk.WORD)

        self.frame_image_player = tk.Frame(self.frame_editor,
                                           height=self.img_player_height+30, width=self.img_player_width+20)
        self.img_canvas = tk.Canvas(self.frame_image_player, width=self.img_player_width, height=self.img_player_height)
        self.img_canvas.create_rectangle(0, 0, self.img_player_width, self.img_player_height, fill='black')
        self.img_player = ImgPlayer(self.__constructor_app, self.img_canvas, self.img_player_height, self.img_player_width)

        self.frame_emotional_state = tk.Frame(self.frame_editor, height=60, width=175)
        self.label_emotional_state = tk.Label(self.frame_emotional_state, text='Оценка состояния:')
        self.field_emotional_state = ttk.Combobox(self.frame_emotional_state, values=self.__states, width=18,
                                                  state='readonly')
        self.field_emotional_state.set(self.__states[0])

        self.frame_inaccuracy = tk.Frame(self.frame_editor, height=60, width=175)
        self.label_inaccuracy = tk.Label(self.frame_inaccuracy, text='Уровень неточности:')
        self.field_inaccuracy = ttk.Combobox(self.frame_inaccuracy, values=self.__inaccuracy, width=18,
                                                  state='readonly')
        self.field_inaccuracy.set(self.__inaccuracy[0])

        self.bt_save = tk.Button(self.frame_editor, text='Сохранить изменения', command=self.__save)
        self.bt_cancel = tk.Button(self.frame_editor, text='Отменить изменения', command=self.__undo_fields_changes)
        self.bt_exit = tk.Button(self.frame_editor, text='Выйти из редактора', command=self.__exit_from_editor)

        self.__pack_and_place()

        self.pose_pil_image, self.pose_id, self.pose_description, self.pose_inaccuracy = None, None, None, None
        self.__update_pose_fields()

    def __pack_and_place(self):
        self.frame_editor.place(x=0, y=0)
        self.frame_description.place(x=0, y=0)
        self.frame_image_player.place(x=0, y=self.frame_description['height'])
        self.frame_emotional_state.place(x=self.frame_image_player['width'], y=self.frame_description['height'])
        self.frame_inaccuracy.place(x=self.frame_image_player['width'], y=self.frame_description['height']+70)

        self.img_canvas.place(x=0, y=0)

        self.label_description.place(x=0, y=0)
        self.text_description.place(x=0, y=30)

        self.label_emotional_state.place(x=0, y=0)
        self.field_emotional_state.place(x=0, y=30)

        self.label_inaccuracy.place(x=0, y=0)
        self.field_inaccuracy.place(x=0, y=30)

        self.label_description.place(x=0, y=0)
        self.text_description.place(x=0, y=30)

        self.bt_save.place(x=self.frame_image_player['width'], y=self.__editor_player_height - 200)
        self.bt_cancel.place(x=self.frame_image_player['width'], y=self.__editor_player_height - 150)
        self.bt_exit.place(x=self.frame_image_player['width'], y=self.__editor_player_height - 100)

    def __set_editor_fields(self, emotional_state, inaccuracy, pose_description):
        self.field_emotional_state.set(emotional_state)
        self.field_inaccuracy.set(inaccuracy)
        self.text_description.delete("1.0", 'end')
        self.text_description.insert("1.0", pose_description)

    def __exit_from_editor(self):
        # clear editor before it close
        self.pose_pil_image, self.pose_id, self.pose_description, self.pose_inaccuracy = None, None, None, None

        self.__update_pose_fields() # clear editor before it close
        self.__constructor_app.switch_to_table()

    def __undo_fields_changes(self):
        self.__update_pose_fields()

    def load_image_for_new_pose(self, pil_image):
        self.img_player.load_img(pil_image)

    def get_image(self):
        return self.img_player.get_img()

    def __update_pose_fields(self):
        self.img_player.load_img(self.pose_pil_image)

        # if its update pose
        if self.pose_id is not None:
            self.__set_editor_fields(self.pose_state,
                                     self.pose_inaccuracy,
                                     self.pose_description)
        # else its create new pose
        else:
            self.__set_editor_fields(self.__states[0], self.__inaccuracy[0], "")

    def __save(self):

        image = self.img_player.get_img()

        pose_description = self.text_description.get("1.0", tk.END).replace('\n', '')
        state = self.field_emotional_state.get()
        inaccuracy = self.field_inaccuracy.get()

        # if its create new pose
        if self.pose_id is None:
            self.__constructor_app.create_pose(image=image,
                                               state=state,
                                               inaccuracy=inaccuracy,
                                               pose_description=pose_description)
        # else its update pose
        else:
            self.__constructor_app.update_pose(id=self.pose_id,
                                               image=image,
                                               state=state,
                                               inaccuracy=inaccuracy,
                                               pose_description=pose_description)

            self.pose_id = None  # clean after update



    def set_active_exists_pose(self, id, pil_image, state, inaccuracy, description):
        self.pose_id = id
        self.pose_pil_image = pil_image
        self.pose_state = state
        self.pose_inaccuracy = inaccuracy
        self.pose_description = description

        self.__update_pose_fields()
