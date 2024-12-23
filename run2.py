from __future__ import absolute_import
from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import OpenGL.GLU as glu
import imgui
import pygame
import sys


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

def Cube():
    gl.glBegin(gl.GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            gl.glColor3fv(colors[x])
            gl.glVertex3fv(verticies[vertex])
    gl.glEnd()

    gl.glBegin(gl.GL_LINES)
    for edge in edges:
        for vertex in edge:
            gl.glVertex3fv(verticies[vertex])
    gl.glEnd()

def loadImage():
    img = pygame.image.load("firefly.jpg")
    textureData = pygame.image.tostring(img, "RGB", 1)
    width = img.get_width()
    height = img.get_height()

    bgImgGL = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, bgImgGL)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, textureData)
    
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    return bgImgGL


def main():
    pygame.init()
    size = 800, 600

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size

    show_custom_window = True

    sizex = 400
    sizey = 400

    imagetexture = loadImage()

    framebuffer = gl.glGenFramebuffers(1)
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)

    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, sizex, sizey, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, texture, 0); 

#     rbo = gl.glGenRenderbuffers(1)
#     gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, rbo)
#     gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH24_STENCIL8, sizex, sizey)
#     gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)
# 
#     gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_STENCIL_ATTACHMENT, gl.GL_RENDERBUFFER, rbo)
#     if(gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE):
#         print("Error")
#     gl.glEnable(gl.GL_DEPTH_TEST)
#     gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
    # gl.glBindTexture(gl.GL_TEXTURE_2D, imagetexture)
    gl.glViewport(0, 0, sizex, sizey)
    gl.glClearColor(0.2, 0.3, 0.3, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    
    glu.gluPerspective(45, (sizex/sizey), 0.1, 50.0)
    # gl.glTranslatef(-1, -1, -5)
    gl.glTranslatef(0, 0, -5)
    Cube()
    # gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Read the pixel at position (x, y)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
                # gl.glBindTexture(gl.GL_TEXTURE_2D, imagetexture)

                # gl.glReadBuffer(gl.GL_FRONT)
                pixels = gl.glReadPixels(0, 0, sizex, sizey, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)


                # Save pixel data to JPEG using Pygame
                image = pygame.image.fromstring(pixels, (sizex, sizey), 'RGB')
                image = pygame.transform.flip(image, False, True) # Flip the image vertically
                pygame.image.save(image, 'output3.jpg')

                print(pixels)

                sys.exit(0)
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
        # gl.glBindTexture(gl.GL_TEXTURE_2D, imagetexture)

        gl.glViewport(0, 0, sizex, sizey)
        gl.glRotatef(1, 3, 1, 1)
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        Cube()

        # gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.show_test_window()

        if show_custom_window:
            is_expand, show_custom_window = imgui.begin("Custom window", True)
            if is_expand:
                imgui.text("Bar")
                imgui.text_colored("Eggs", 0.2, 1.0, 0.0)
                imgui.image(texture, sizex, sizey)
                
            imgui.end()

        # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
        #       does not support fill() on OpenGL sufraces
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()
        pygame.time.wait(1000//144)


if __name__ == "__main__":
    main()
