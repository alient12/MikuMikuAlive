import csv
import numpy as np
from nuthouse01_core import MyBezier
import pymeshio.pmx.reader
import matplotlib.pyplot as plt

bone_frames = {}

with open('./Shadow Motion/shadow_motion.txt', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile)
    bone_frames_flag = False
    for row in spamreader:
        if row[0].startswith("bone_name"):
            bone_frames_flag = True
            continue
        elif row[0].startswith("morphframe_ct"):
            bone_frames_flag = False
            break
        else:
            if bone_frames_flag:
                if row[0] not in bone_frames:
                    bone_frames[row[0]] = []
                bone_frames[row[0]].append(row)

class Bone_frame_data:
    def __init__(self, bone_frames_list) -> None:
        self.name = bone_frames_list[0][0]
        self.phys = bone_frames_list[0][8]
        self.frames_data = {}
        self.interps_data = {}
        self.farthest_frame_num = None
        for bf in bone_frames_list:
            frame_num = int(bf[1])
            data = [eval(i) for i in bf[2:8]] # pos and rot data
            interps = [eval(i) for i in bf[9:]]
            self.frames_data[frame_num] = data
            self.interps_data[frame_num] = interps
        self.farthest_frame_num = frame_num
    
    def compute_all_frames(self):
        res = 0
        prev_frame_num = None
        for t in range(1, self.farthest_frame_num + 1):
            if t in self.frames_data:
                frame_data = self.frames_data[t]
                interp_data = self.interps_data[t]
                self.bezier(frame_data, interp_data, t, prev_frame_num, res)
                prev_frame_num = t
                res = 0
            else:
                res += 1
    def bezier(self, frame_data, interp_data, current_frame_num, prev_frame_num, res):
        if prev_frame_num == None:
            prev_frame_num = 0
            x0, y0, z0, rx0, ry0, rz0 = 0, 0, 0, 0, 0, 0
        else:
            x0 = self.frames_data[prev_frame_num][0]
            y0 = self.frames_data[prev_frame_num][1]
            z0 = self.frames_data[prev_frame_num][2]
            rx0 = self.frames_data[prev_frame_num][3]
            ry0 = self.frames_data[prev_frame_num][4]
            rz0 = self.frames_data[prev_frame_num][5]
        
        bezi_x = MyBezier((interp_data[0], interp_data[1]), (interp_data[2], interp_data[3]), res)
        bezi_y = MyBezier((interp_data[4], interp_data[5]), (interp_data[6], interp_data[7]), res)
        bezi_z = MyBezier((interp_data[8], interp_data[9]), (interp_data[10], interp_data[11]), res)
        bezi_r = MyBezier((interp_data[12], interp_data[13]), (interp_data[14], interp_data[15]), res)
        
        x1 = self.frames_data[current_frame_num][0]
        y1 = self.frames_data[current_frame_num][1]
        z1 = self.frames_data[current_frame_num][2]
        rx1 = self.frames_data[current_frame_num][3]
        ry1 = self.frames_data[current_frame_num][4]
        rz1 = self.frames_data[current_frame_num][5]
        
        for i in range(1, res + 1):
            t = i / res
            x = x0 + bezi_x.approximate(t) * (x1 - x0)
            y = y0 + bezi_y.approximate(t) * (y1 - y0)
            z = z0 + bezi_z.approximate(t) * (z1 - z0)
            r = bezi_r.approximate(t)
            rx = rx0 + r * (rx1 - rx0)
            ry = ry0 + r * (ry1 - ry0)
            rz = rz0 + r * (rz1 - rz0)
            self.frames_data[prev_frame_num + i] = (x, y, z, rx, ry, rz)

# bone_frame_data = Bone_frame_data(bone_frames['首'])
bone_frame_arr = [Bone_frame_data(bone) for key, bone in bone_frames.items()]
for bone in bone_frame_arr:
    bone.compute_all_frames()
bone_frame_dict = {}
for bone in bone_frame_arr:
    bone_frame_dict[bone.name] = bone

path = 'Arcane Caitlyn/Caitlyn.pmx'
model=pymeshio.pmx.reader.read_from_file(path)

bones = model.bones
abs_pos_bones = {}
for i, bone in enumerate(bones):
    parent_index = bone.parent_index
    
    # check if bone is root
    if parent_index == -1:
        pos = bone.position
        abs_pos_bones[i] = [pos, bone.name]
    else:
        pos_p = bones[parent_index].position
        pos = bone.position + pos_p
        abs_pos_bones[i] = [pos, bone.name]
t = 50
for i, bone in abs_pos_bones.items():
    name = bone[1]
    x_pos = bone[0][0] + bone_frame_dict[name].frames_data[t][0]
    y_pos = bone[0][1] + bone_frame_dict[name].frames_data[t][1]
    z_pos = bone[0][2] + bone_frame_dict[name].frames_data[t][2]
    abs_pos_bones[i] = [x_pos, y_pos, z_pos]

x = [val[0] for key, val in abs_pos_bones.items()]
y = [val[1] for key, val in abs_pos_bones.items()]
z = [val[2] for key, val in abs_pos_bones.items()]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(x, y, z, marker="o")
plt.show()