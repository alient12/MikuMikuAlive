import pymeshio.pmx.reader

# path = 'Shrek/shrek.pmx'
path = 'Arcane Caitlyn/Caitlyn.pmx'
model=pymeshio.pmx.reader.read_from_file(path)
# print(model.vertices[0].__slots__)
# print(model.indices[0])
# print(model.textures[0])
# print(model.materials[0].__slots__)
# print(model.bones[0].__slots__)
# print(model.morphs[0].__slots__)
# print(model.display_slots[0].__slots__)
# print(model.rigidbodies[0].__slots__)
# print(model.joints[0].__slots__)
# print(len(model.indices))
# print(len(model.vertices))

# v0 = model.vertices[0]
# flag = True
# for v in model.vertices:
#     if flag:
#         flag = False
#         continue
#     if v.position[0] == v0.position[0] and v.position[1] == v0.position[1] and v.position[2] == v0.position[2]:
#         print(v.normal[0], v0.normal[0])

bones = model.bones
abs_pos_bones = {}
for i, bone in enumerate(bones):
    parent_index = bone.parent_index
    
    # check if bone is root
    if parent_index == -1:
        pos = bone.position
        abs_pos_bones[i] = pos
    else:
        pos_p = bones[parent_index].position
        pos = bone.position + pos_p
        abs_pos_bones[i] = pos

joints = model.joints
abs_pos_joints = {}
for i, joint in enumerate(joints):
    pos = joint.position
    abs_pos_joints[i] = pos

import matplotlib.pyplot as plt
import numpy as np

x = [val[0] for key, val in abs_pos_bones.items()]
y = [val[1] for key, val in abs_pos_bones.items()]
z = [val[2] for key, val in abs_pos_bones.items()]

xj = [val[0] for key, val in abs_pos_joints.items()]
yj = [val[1] for key, val in abs_pos_joints.items()]
zj = [val[2] for key, val in abs_pos_joints.items()]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(x, y, z, marker="o")
ax.scatter(xj, yj, zj, marker="o")
plt.show()

# the error is because of japanese-english conflict