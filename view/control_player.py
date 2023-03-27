import tkinter as tk


class ControlPlayer:

    def __init__(self, app, window, player_height, player_width):
        self.__app = app

        self.__file_path = ""
        #
        self.__is_img_input = True
        self.__is_web_cam_input = False
        self.__is_constructor_input = False
        self.__is_classified = False

        # filepath frame
        self.__frame_file = tk.Frame(window, height=player_height, width=player_width)
        self.__label_path_to_file = tk.Label(self.__frame_file, text="Путь к файлу")
        self.__entry_path_to_file = tk.Entry(self.__frame_file, justify="left", width=70, state="readonly")
        self.__bt_select_file = tk.Button(self.__frame_file, text="Выбрать", command=self.__open_file)

        # main control panel frame
        self.__frame_controls = tk.Frame(window, height=player_height, width=player_width)
        self.__bt_switch_to_web_cam = tk.Button(self.__frame_controls, text="Включить захват с камеры",
                                                command=self.__switch_to_web_cam)
        self.__bt_classify = tk.Button(self.__frame_controls, text="Выполнить", command=self.__classify, state='disabled')
        self.__bt_save = tk.Button(self.__frame_controls, text="Сохранить", command=self.__save_file, state='disabled')
        self.__bt_switch_to_constructor = tk.Button(self.__frame_controls, text="Переключиться на конструктор",
                                                    command=self.__switch_to_constructor)
        self.__pack_and_place()

    def __pack_and_place(self):
        self.__frame_file.place(x=0, y=0)
        self.__label_path_to_file.place(x=0, y=0)
        self.__entry_path_to_file.place(x=0, y=25)
        self.__bt_select_file.place(x=570, y=25)
        self.__frame_controls.place(x=0, y=60)
        self.__bt_switch_to_web_cam.place(x=0, y=0)
        self.__bt_switch_to_constructor.place(x=250, y=0)
        self.__bt_classify.place(x=740, y=0)
        self.__bt_save.place(x=850, y=0)

    def activate_deactivate_buttons(self):
        self.__bt_classify['state'] = 'normal' if self.__file_path != "" or self.__is_web_cam_input else 'disabled'
        self.__bt_save['state'] = 'normal' if self.__file_path != "" and self.is_classified() else 'disabled'

    def __update_file_path_field(self, file_path):
        self.__entry_path_to_file.config(state="normal")
        self.__entry_path_to_file.delete(0, "end")
        self.__entry_path_to_file.insert(0, file_path if file_path is not None else "")
        self.__entry_path_to_file.config(state="readonly")

    def __open_file(self):
        self.__file_path = self.__app.open_file()
        self.__update_file_path_field(self.__file_path)
        self.__cancel_classify()

    def __save_file(self):
        self.__app.save_file()

    def __switch_to_web_cam(self):
        self.__bt_switch_to_web_cam.config(text="Отключить захват с веб-камеры" if not self.__is_web_cam_input
                                                else "Включить захват с веб-камеры")
        self.__is_web_cam_input = True if not self.__is_web_cam_input else False
        self.__update_file_path_field("Захват с веб-камеры" if self.__is_web_cam_input else self.__file_path)
        self.__app.switch_player()
        self.__cancel_classify()

    def __switch_to_constructor(self):
        self.__bt_switch_to_constructor.config(text="Выйти из конструктора" if not self.__is_constructor_input
                                                    else "Переключиться на конструктор")
        self.__is_constructor_input = True if not self.__is_constructor_input else False
        self.__app.switch_player()
        self.__cancel_classify()

    def __cancel_classify(self):
        self.__bt_classify.config(text="Выполнить")
        self.__is_classified = False
        self.activate_deactivate_buttons()

    def __classify(self):
        self.__bt_classify.config(text="Отменить" if not self.__is_classified else "Выполнить")
        self.__is_classified = True if not self.__is_classified else False
        self.__app.classify()
        self.activate_deactivate_buttons()

    def is_img_input(self):
        return self.__is_img_input

    def is_web_cam_input(self):
        return self.__is_web_cam_input

    def is_constructor_input(self):
        return self.__is_constructor_input

    def is_classified(self):
        return self.__is_classified

    def get_file_path(self):
        return self.__file_path
