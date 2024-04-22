import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
import time

from pyopengltk import OpenGLFrame
verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

counter = 0

class frame(OpenGLFrame):

    def initgl(self):
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.5, 0.5, 0.0)
        # gluPerspective(45, (self.width/self.height), 0.1, 50.0)

        # setup projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width/self.height), 0.1, 50.0)
        glTranslatef(0, 0, -5)
        # glOrtho(0, self.width, self.height, 0, -10, 10)

        # setup identity model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        print("B")

        
    def redraw(self):
        global counter
        # glViewport(0, 0, self.width, self.height)
        # glViewport(0, 0, self.width, self.height)

        glClearColor(0.0, 0.5, 0.5, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glLoadIdentity()
        # glBegin(GL_LINES)
        # glColor3f(1.0,0.0,3.0)
        # glVertex2f(200,100)
        # glVertex2f(100,100)
        # glEnd()
        # glFlush()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        counter += 1
        glRotatef(counter, 3, 1, 1)
        
        # glTranslatef(0.0, 0.0, 1)
        glBegin(GL_QUADS)
        for surface in surfaces:
            x = 0
            for vertex in surface:
                x+=1
                glColor3fv(colors[x])
                glVertex3fv(verticies[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(verticies[vertex])
        glEnd()
        glFlush()

        print("A")

    def on_resize(self, event, arg=None):
        if event:
            w = event.width
            h = event.height
        else:
            if arg:
                w = arg['w']
                h = arg['h']
            else:
                raise Exception

        dx = w/h
        glViewport(0, 0, w, h)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width/self.height), 0.1, 50.0)
        glLoadIdentity()


def keydown(event):
    global counter
    print(event)
    counter += 1

if __name__=='__main__':

    root = tk.Tk()
    app = frame(root, width=500, height=500)
    app.pack(fill=tk.BOTH, expand=tk.YES)
    app.animate = 1
    # app.after(100, app.printContext)
    root.bind("<KeyPress>", keydown)
    app.mainloop()