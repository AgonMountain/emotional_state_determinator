import json


class Pose:

    def __init__(self, pose_id, label, img_name, pose_angels, pose_crossings, distances):
        self.pose_id = pose_id
        self.label = label
        self.img_name = img_name
        self.pose_angels = pose_angels
        self.pose_crossings = pose_crossings
        self.distances = distances

    def to_json(self):
        return {"pose": {"id": self.pose_id,
                         "label": self.label,
                         "img_name": self.img_name,
                         "pose_angels": self.pose_angels,
                         "pose_crossings": self.pose_crossings,
                         "distances_between_keypoints": self.distances}}


class PoseManager:

    def __init__(self, poses_json_file_path):
        self.poses_json_file_path = poses_json_file_path
        self.poses = {}
        self.__read(poses_json_file_path)

    def remove(self, pose_id):
        with open(self.poses_json_file_path, 'r') as f:
            json_data = json.load(f)

        for d in json_data['poses']:
            if d['pose']['id'] == id:
                i = json_data['poses'].index(d)
                del json_data['poses'][i]

        with open(self.poses_json_file_path, 'w') as f:
            json.dump(json_data, f)

    def add(self, pose):
        with open(self.poses_json_file_path, 'r') as f:
            json_data = json.load(f)

        json_data['poses'].append(pose.to_json())

        with open(self.poses_json_file_path, 'w') as f:
            json.dump(json_data, f)

    def update(self, pose):
        self.remove(pose.pose_id)
        self.add(pose)

    def __read(self, poses_json_file_path):
        with open(poses_json_file_path, "r") as f:
            json_data = json.load(f)
            for d in json_data['poses']:
                self.poses[d['pose']['id']] = Pose(d['pose']['id'],
                                                   d['pose']['label'],
                                                   d['pose']['img_name'],
                                                   d['pose']['pose_angels'],
                                                   d['pose']['pose_crossings'],
                                                   d['pose']['distances_between_keypoints'])

    def get(self, id):
        return self.poses.get(id)

    def ids(self):
        return [pose_id for pose_id in self.poses]


# p = PoseManager()
# o = p.get(2)
# o.img_name = "5555"
# print(p.remove(2))