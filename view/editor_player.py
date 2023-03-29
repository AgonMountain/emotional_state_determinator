import tkinter as tk
from tkinter import ttk
from view.img_player import ImgPlayer


class EditorPlayer:

    def __init__(self, constructor_app, window, height, width, states):
        self.__constructor_app = constructor_app
        self.__editor_player_height = height
        self.__editor_player_width = width
        self.__states = states

        size = 0.8
        self.img_player_height = height * size
        self.img_player_width = width * size

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

        self.frame_body_inaccuracy = tk.Frame(self.frame_editor, height=100, width=175)
        self.label_body_inaccuracy = tk.Label(self.frame_body_inaccuracy, text='Погрешность углов тела:"')
        self.field_body_inaccuracy = tk.Entry(self.frame_body_inaccuracy, justify='right', width=15)
        self.label_body_inaccuracy_px = tk.Label(self.frame_body_inaccuracy, text='гр.')
        self.bt_show_body_inaccuracy = tk.Button(self.frame_body_inaccuracy, text='Показать погрешность')

        self.frame_right_hand_inaccuracy = tk.Frame(self.frame_editor, height=130, width=175)
        self.label_right_hand_inaccuracy = tk.Label(self.frame_right_hand_inaccuracy,
                                                    text="Погрешность точек\nправой руки:")
        self.field_right_hand_inaccuracy = tk.Entry(self.frame_right_hand_inaccuracy, justify="right", width=15)
        self.label_right_hand_inaccuracy_px = tk.Label(self.frame_right_hand_inaccuracy, text="px")
        self.bt_right_hand_inaccuracy = tk.Button(self.frame_right_hand_inaccuracy, text="Показать погрешность")

        self.frame_left_hand_inaccuracy = tk.Frame(self.frame_editor, height=130, width=175)
        self.label_left_hand_inaccuracy = tk.Label(self.frame_left_hand_inaccuracy,
                                                   text="Погрешность точек\nлевой руки:")
        self.field_left_hand_inaccuracy = tk.Entry(self.frame_left_hand_inaccuracy, justify="right", width=15)
        self.label_left_hand_inaccuracy_px = tk.Label(self.frame_left_hand_inaccuracy, text="px")
        self.bt_left_hand_inaccuracy = tk.Button(self.frame_left_hand_inaccuracy, text="Показать погрешность")

        self.bt_save = tk.Button(self.frame_editor, text='Сохранить', command=self.__save)
        self.bt_cancel = tk.Button(self.frame_editor, text='Отменить', command=self.__undo_fields_changes)
        self.bt_exit = tk.Button(self.frame_editor, text='Выйти из редактора', command=self.__exit_from_editor)

        self.__pack_and_place()

        self.pose_pil_image, self.pose_data = None, None
        self.__update_pose_fields()

    def __pack_and_place(self):
        self.frame_editor.place(x=0, y=0)

        self.frame_description.place(x=0, y=0)
        self.label_description.place(x=0, y=0)
        self.text_description.place(x=0, y=30)

        self.frame_image_player.place(x=0, y=self.frame_description['height'])
        self.frame_emotional_state.place(x=self.frame_image_player['width'], y=self.frame_description['height'])
        self.frame_body_inaccuracy.place(x=self.frame_image_player['width'], y=self.frame_description['height']+70)
        self.frame_right_hand_inaccuracy.place(x=self.frame_image_player['width'], y=self.frame_description['height']+170)
        self.frame_left_hand_inaccuracy.place(x=self.frame_image_player['width'], y=self.frame_description['height']+290)

        self.img_canvas.place(x=0, y=0)

        self.label_emotional_state.place(x=0, y=0)
        self.field_emotional_state.place(x=0, y=30)

        self.label_description.place(x=0, y=0)
        self.text_description.place(x=0, y=30)

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

        self.bt_save.place(x=self.frame_image_player['width'], y=self.__editor_player_height - 100)
        self.bt_cancel.place(x=self.frame_image_player['width']+90, y=self.__editor_player_height - 100)
        self.bt_exit.place(x=self.frame_image_player['width'], y=self.__editor_player_height - 50)

    def __set_editor_fields(self, field_emotional_state, field_body_inaccuracy, field_left_hand_inaccuracy,
                            field_right_hand_inaccuracy, pose_description):
        self.field_emotional_state.set(field_emotional_state)
        self.field_body_inaccuracy.delete(0, 'end')
        self.field_left_hand_inaccuracy.delete(0, 'end')
        self.field_right_hand_inaccuracy.delete(0, 'end')
        self.text_description.delete("1.0", 'end')
        self.field_body_inaccuracy.insert(0, field_body_inaccuracy)
        self.field_left_hand_inaccuracy.insert(0, field_left_hand_inaccuracy)
        self.field_right_hand_inaccuracy.insert(0, field_right_hand_inaccuracy)
        self.text_description.insert("1.0", pose_description)

    def __update_pose_fields(self):
        self.img_player.load_img(self.pose_pil_image)

        if self.pose_data is not None:
            self.__set_editor_fields(self.pose_data.get_state(),
                                     self.pose_data.get_pose_angels_inaccuracy(),
                                     self.pose_data.get_kp_distances_inaccuracy()['left'],
                                     self.pose_data.get_kp_distances_inaccuracy()['right'],
                                     self.pose_data.get_pose_description())
        else:
            self.__set_editor_fields(self.__states[0], "0", "0", "0", "")

    def __exit_from_editor(self):
        self.pose_pil_image, self.pose_data = None, None    # clear editor before it close
        self.__update_pose_fields() # clear editor before it close
        self.__constructor_app.switch_to_table()

    def __undo_fields_changes(self):
        self.__update_pose_fields()

    def __save(self):
        image, state, data = self.__constructor_app.classify_pose(self.img_player.get_img())
        image = self.img_player.get_img()
        state = self.field_emotional_state.get()
        pose_description = self.text_description.get("1.0", tk.END)

        inaccuracies = {}
        d = self.field_body_inaccuracy.get()
        inaccuracies['pose_angels_inaccuracy'] = int(d.replace('\n', '') if d != '' else '0')
        inaccuracies['kp_distances_inaccuracy'] = {}
        r = self.field_right_hand_inaccuracy.get()
        inaccuracies['kp_distances_inaccuracy']['right'] = int(r if r != '' else '0')
        l = self.field_left_hand_inaccuracy.get()
        inaccuracies['kp_distances_inaccuracy']['left'] = int(l if l != '' else '0')

        # if its create new pose
        if self.pose_data is None:
            self.__constructor_app.create_pose(image=image, state=state, pose_angels=data['angels'],
                                               kp_distances=data['distances'], pose_crossings=data['crossings'],
                                               inaccuracies=inaccuracies, pose_description=pose_description)
        # else its update pose
        else:
            self.pose_data.state = state
            self.pose_data.inaccuracies = inaccuracies
            self.pose_data.pose_description = pose_description
            self.pose_data.pose_angels = data['angels']
            self.pose_data.kp_distances = data['distances']
            self.pose_data.pose_crossings = data['crossings']
            self.__constructor_app.update_pose(pose_data=self.pose_data, image=image)

    def load_image_for_new_pose(self, pil_image):
        self.img_player.load_img(pil_image)

    def set_active_exists_pose(self, pose_pil_image, pose_data):
        self.pose_pil_image, self.pose_data = pose_pil_image, pose_data
        self.__update_pose_fields()
