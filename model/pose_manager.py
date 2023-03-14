import json
import os
import numpy
from PIL import Image
from config.config import poses_img_folder_path
import datetime


class Pose:

    def __init__(self,
                 id,
                 state,
                 img_name,
                 pose_angels,
                 kp_distances,
                 pose_crossings,
                 pose_description,
                 recent_change_date_time):

        self.id = id
        self.state = state
        self.img_name = img_name
        self.pose_angels = pose_angels
        self.kp_distances = kp_distances
        self.pose_crossings = pose_crossings
        self.pose_description = pose_description
        self.recent_change_date_time = recent_change_date_time

    def get_id(self):
        return self.id

    def get_state(self):
        return self.state

    def get_img_path(self):
        return poses_img_folder_path + '\\' + self.img_name

    def get_recent_change_date_time(self):
        return self.recent_change_date_time

    def to_json(self):
        return {"pose": {"id": self.id,
                         "state": self.state,
                         "img_name": self.img_name,
                         "pose_angels": self.pose_angels,
                         "kp_distances": self.kp_distances,
                         "pose_crossings": self.pose_crossings,
                         "pose_description": self.pose_description,
                         "recent_change_date_time": self.recent_change_date_time,}}


class PoseManager:

    def __init__(self, poses_json_file_path):
        self.__poses_json_file_path = poses_json_file_path
        self.__poses = self.__read_from_json(self.__poses_json_file_path)

    def __read_from_json(self, poses_json_file_path):
        poses = {}
        with open(poses_json_file_path, "r") as f:
            json_data = json.load(f)
            for d in json_data['poses']:
                poses[d['pose']['id']] = Pose(d['pose']['id'],
                                              d['pose']['state'],
                                              d['pose']['img_name'],
                                              d['pose']['pose_angels'],
                                              d['pose']['kp_distances'],
                                              d['pose']['pose_crossings'],
                                              d['pose']['pose_description'],
                                              d['pose']['recent_change_date_time'])
        return poses

    def __remove_from_json(self, pose_id):
        with open(self.__poses_json_file_path, 'r') as f:
            json_data = json.load(f)

        for d in json_data['poses']:
            if d['pose']['id'] == pose_id:
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
        self.__remove_from_json(pose.id)
        self.__add_to_json(pose)

    def __reload_poses(self):
        self.__poses = self.__read_from_json(self.__poses_json_file_path)

    def __create_id(self):
        id = 1
        for k in self.__poses:
            if k == id:
                id += 1
        return id

    def __get_actual_date_time(self):
        return '{date:%d-%m-%Y %H:%M:%S}'.format(date=datetime.datetime.now())

    def create_pose(self, image, state, pose_angels, kp_distances, pose_crossings, pose_description):
        id = self.__create_id()
        img_name = str(id) + '.png'
        recent_change_date_time = "Создано: " + self.__get_actual_date_time()

        img_file = Image.fromarray(numpy.array(image))
        img_file.save(poses_img_folder_path + '\\' + img_name)

        self.__add_to_json(Pose(id,
                                state,
                                img_name,
                                pose_angels,
                                kp_distances,
                                pose_crossings,
                                pose_description,
                                recent_change_date_time))

        self.__reload_poses()
        return self.get_all_id()

    def delete_pose(self, pose_id):
        pose = self.get_pose(pose_id)
        os.remove(pose.get_img_path())

        self.__remove_from_json(pose_id)
        self.__reload_poses()
        return self.get_all_id()

    def update_pose(self, pose):
        pose.recent_change_date_time = "Обновлено: " + self.__get_actual_date_time()
        self.__update_in_json(pose)
        self.__reload_poses()
        return self.get_all_id()

    def get_pose(self, pose_id):
        return self.__poses.get(pose_id)

    def get_pose_image(self, pose_id):
        pose = self.__poses.get(pose_id)
        if pose is not None:
            return Image.open(poses_img_folder_path + '\\' + pose.img_name)
        else:
            return None

    def get_all_id(self):
        return [pose_id for pose_id in self.__poses]
