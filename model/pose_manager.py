import json

from config import poses_json_file_path


class Pose():

    def __init__(self, id, img_name, pose_angels, pose_crossings, distances_between_keypoints):
        self.id = id
        self.img_name = img_name
        self.pose_angels = pose_angels
        self.pose_crossings = pose_crossings
        self.distances_between_keypoints = distances_between_keypoints

    def to_json(self):
        return {"pose": {"id": self.id, "img_name": self.img_name,
                         "pose_angels": self.pose_angels, "pose_crossings": self.pose_crossings,
                         "distances_between_keypoints": self.distances_between_keypoints}}


class PoseManager():

    def __init__(self):
        self.poses = {}
        self.__read()

    def remove(self, id):
        with open(poses_json_file_path, 'r') as f:
            json_data = json.load(f)

        for d in json_data['poses']:
            if d['pose']['id'] == id:
                i = json_data['poses'].index(d)
                del json_data['poses'][i]

        with open(poses_json_file_path, 'w') as f:
            json.dump(json_data, f)

    def add(self, pose):
        with open(poses_json_file_path, 'r') as f:
            json_data = json.load(f)

        json_data['poses'].append(pose.to_json())

        with open(poses_json_file_path, 'w') as f:
            json.dump(json_data, f)

    def update(self, pose):
        self.remove(pose.id)
        self.add(pose)

    def __read(self):
        with open(poses_json_file_path, "r") as f:
            json_data = json.load(f)
            for d in json_data['poses']:
                self.poses[d['pose']['id']] = Pose(d['pose']['id'],
                                                   d['pose']['img_name'],
                                                   d['pose']['pose_angels'],
                                                   d['pose']['pose_crossings'],
                                                   d['pose']['distances_between_keypoints'])

    def get(self, id):
        return self.poses.get(id)


# p = PoseManager()
# o = p.get(2)
# o.img_name = "5555"
# print(p.remove(2))