import json
import os
import numpy
import datetime
from PIL import Image

from config.config import POSE_IMAGES_FOLDER


class Pose:

    def __init__(self, pose_id, state, image_name, pose_angels, pose_crossings, inaccuracy,
                 pose_description, recent_change_date_time):
        self.pose_id = pose_id
        self.state = state
        self.image_name = image_name
        self.pose_angels = pose_angels
        self.pose_crossings = pose_crossings
        self.inaccuracy = inaccuracy
        self.pose_description = pose_description
        self.recent_change_date_time = recent_change_date_time

    def get_pose_id(self):
        return self.pose_id

    def get_state(self):
        return self.state

    def get_img_path(self):
        return POSE_IMAGES_FOLDER + '\\' + self.image_name

    def get_recent_change_date_time(self):
        return self.recent_change_date_time

    def get_pose_angels(self):
        return self.pose_angels

    def get_pose_crossings(self):
        return self.pose_crossings

    def get_inaccuracy(self):
        return self.inaccuracy

    def get_pose_description(self):
        return self.pose_description

    def set_recent_change_date_time(self, date_time):
        self.recent_change_date_time = date_time

    def to_json(self):
        return {"pose": {"pose_id": self.pose_id,
                         "state": self.state,
                         "img_name": self.image_name,
                         "pose_angels": self.pose_angels,
                         "pose_crossings": self.pose_crossings,
                         "inaccuracy": self.inaccuracy,
                         "pose_description": self.pose_description,
                         "recent_change_date_time": self.recent_change_date_time}}


class PoseManager:

    def __init__(self, poses_json_file_path):
        self.__poses_json_file_path = poses_json_file_path
        self.__poses = self.__read_from_json(self.__poses_json_file_path)

    def __get_actual_date_time(self):
        return '{date:%d-%m-%Y %H:%M:%S}'.format(date=datetime.datetime.now())

    def __read_from_json(self, poses_json_file_path):
        poses = {}
        with open(poses_json_file_path, "r") as f:
            json_data = json.load(f)
            for d in json_data['poses']:
                poses[d['pose']['pose_id']] = Pose(pose_id= d['pose']['pose_id'],
                                                      state= d['pose']['state'],
                                                      image_name= d['pose']['img_name'],
                                                      pose_angels= d['pose']['pose_angels'],
                                                      pose_crossings= d['pose']['pose_crossings'],
                                                      inaccuracy= d['pose']['inaccuracy'],
                                                      pose_description= d['pose']['pose_description'],
                                                      recent_change_date_time= d['pose']['recent_change_date_time'])
        return poses

    def __remove_from_json(self, pose_id):
        with open(self.__poses_json_file_path, 'r') as f:
            json_data = json.load(f)

        for d in json_data['poses']:
            if d['pose']['pose_id'] == pose_id:
                i = json_data['poses'].index(d)
                del json_data['poses'][i]

        with open(self.__poses_json_file_path, 'w') as f:
            json.dump(json_data, f)

    def __add_to_json(self, pose):
        with open(self.__poses_json_file_path, 'r') as f:
            json_data = json.load(f)

        json_data['poses'].append(pose.to_json())

        with open(self.__poses_json_file_path, 'w') as f:
            json.dump(json_data, f, ensure_ascii=False)

    def __update_in_json(self, pose):
        self.__remove_from_json(pose.pose_id)
        self.__add_to_json(pose)

    def __reload_poses(self):
        self.__poses = self.__read_from_json(self.__poses_json_file_path)

    def __create_id(self):
        id = 1
        for k in self.__poses:
            if k == id:
                id += 1
        return id

    def __save_img(self, image_name, image):
        img_file = Image.fromarray(numpy.array(image))
        img_file.save(POSE_IMAGES_FOLDER + '\\' + image_name)

    def create_pose(self, image, state, pose_angels, pose_crossings, inaccuracy, pose_description):
        pose_id = self.__create_id()
        image_name = str(pose_id) + '.png'

        self.__add_to_json(Pose(pose_id= pose_id, state= state, image_name= image_name, pose_angels= pose_angels,
                                pose_crossings= pose_crossings, pose_description= pose_description,
                                inaccuracy=inaccuracy,
                                recent_change_date_time= "Создано: "+self.__get_actual_date_time()))
        self.__save_img(image_name, image)

        self.__reload_poses()
        return self.get_all_id()

    def update_pose(self, pose_data, image):
        pose_data.set_recent_change_date_time("Обновлено: " + self.__get_actual_date_time())
        self.__save_img(pose_data.image_name, image)
        self.__update_in_json(pose_data)
        self.__reload_poses()
        return self.get_all_id()

    def delete_pose(self, pose_id):
        pose = self.get_pose(pose_id)
        os.remove(pose.get_img_path())
        self.__remove_from_json(pose_id)
        self.__reload_poses()
        return self.get_all_id()

    def get_pose(self, pose_id):
        return self.__poses.get(pose_id)

    def get_pose_image(self, pose_id):
        pose = self.__poses.get(pose_id)
        if pose is not None:
            return Image.open(pose.get_img_path())
        else:
            return None

    def get_all_id(self):
        return [pose_id for pose_id in self.__poses]
