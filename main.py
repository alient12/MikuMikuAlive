import sys
# sys.path.insert(0, ".")
# print(sys.path)
import os
import opengl
import opengl.rokuro
import opengl.shader
import opengl.coord
import pymeshio.pmx.reader
import pmxbuilder

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import win32api
import win32con
import win32gui

from PIL import Image
from PIL import ImageOps

class Scene:
    def __init__(self, *args):
        self.items=[]
        self.coord=opengl.coord.Coord(50)

    def draw(self):
        self.coord.draw()
        for item in self.items: item.draw()


pygame.init()
SCREEN_SIZE = (800, 800)
screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
screen = pygame.display.set_mode(SCREEN_SIZE, NOFRAME|HWSURFACE|OPENGL|DOUBLEBUF)

hwnd = pygame.display.get_wm_info()['window']
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

# allways on top without moving
win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

view = opengl.rokuro.RokuroView()
glworld = opengl.BaseController(view)
scene = Scene()
glworld.setRoot(scene)
# path = 'Arcane Caitlyn/Caitlyn.pmx'
path = 'Shrek/shrek.pmx'
# path = 'Ahri WildRift/Ahri smaller.pmx'
model = pmxbuilder.build(path)
scene.items=[model]

model.draw()
view.shift(1, 1)
view.updateProjection()
view.updateView()
glTranslate(0, -12, 50)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
    
    
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    model.draw()
    glRotatef(0.03, 0, 1, 0)

    pygame.display.flip()
