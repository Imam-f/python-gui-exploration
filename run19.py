import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GL.shaders import compileShader, compileProgram

import imgui
from imgui.integrations.glfw import GlfwRenderer



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


def main():

    imgui.create_context()
    # ctx1 = imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    
    pic_x, pic_y = 200, 200
    pic = (pic_x, pic_y)

    vertex_shader_source = """
    #version 330

    layout (location = 0) in vec3 pos;

    void main()
    {
        gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
    }
    """


    fragment_shader_source = """
    #version 330

    out vec4 color;

    void main()
    {
        color = vec4(0.0, 1.0, 0.0, 1.0);
    }
    """


    gl.glViewport(0, 0, pic_x, pic_y)
    vertices = [
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ]

    vbo = gl.glGenBuffers(1)
    vao = gl.glGenVertexArrays(1)

    gl.glBindVertexArray(vao)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

    gl.glBufferData(gl.GL_ARRAY_BUFFER, (gl.GLfloat * len(vertices))(*vertices), gl.GL_STATIC_DRAW)


    # Specify the vertex attribute pointers
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
    gl.glEnableVertexAttribArray(0)

    # Unbind the VAO
    gl.glBindVertexArray(0)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)



    vertex_shader = compileShader(vertex_shader_source, gl.GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_shader_source, gl.GL_FRAGMENT_SHADER)
    shader_program = compileProgram(vertex_shader, fragment_shader)


    framebuffer = gl.glGenFramebuffers(1)
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)

    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, pic_x, pic_y, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, texture, 0); 

    
    # rbo = gl.glGenRenderbuffers(1)
    # gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, rbo)
    # gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH24_STENCIL8, pic_x, pic_y)
    # gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)

    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    # gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)

    glu.gluPerspective(45, (1280/720), 0.1, 50.0)
    gl.glTranslatef(0, 0, -5)


    show_custom_window = True
    
    try:
        while not glfw.window_should_close(window):
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            if imgui.begin_main_menu_bar():
                if imgui.begin_menu("File", True):

                    clicked_quit, selected_quit = imgui.menu_item(
                        "Quit", 'Cmd+Q', False, True
                    )

                    if clicked_quit:
                        exit(1)

                    imgui.end_menu()
                imgui.end_main_menu_bar()

            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
            gl.glLoadIdentity()
            gl.glViewport(0, 0, pic_x, pic_y)
            gl.glClearColor(1, 0.5, 0.5, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            
            gl.glUseProgram(shader_program)
            gl.glBindVertexArray(vao)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
            gl.glBindVertexArray(0)
            gl.glUseProgram(0)
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
            
            if show_custom_window:
                is_expand, show_custom_window = imgui.begin("Custom window", True)
                if is_expand:
                    imgui.text("Bar")
                    imgui.text_ansi("B\033[31marA\033[mnsi ")
                    imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)
                    imgui.extra.text_ansi_colored("Eggs", 0.2, 1., 0.)
                    imgui.image(texture, pic_x, pic_y)
                imgui.end()

            # show_test_window()
            # imgui.show_test_window()
            imgui.render()

            # io = imgui.get_io()
            # x, y = io.display_size

            # gl.glLoadIdentity()
            # gl.glViewport(0, 0, int(x), int(y))
            # gl.gluPerspective(45, (int(x)/int(y)), 0.1, 50.0)
            # gl.glTranslatef(0.0, 0.0, -5)
            # gl.glClearColor(0.5, 0.5, 1., 1)
            # gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            # gl.glRotatef(1, 7, 1, 15)
            # Cube()
            # glPopMatrix()
            
            
            gl.glClearColor(0.5, 0.5, 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            
            # gl.glUseProgram(shader_program)
            # gl.glBindVertexArray(vao)
            # gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
            # gl.glBindVertexArray(0)
            # gl.glUseProgram(0)

            gl.glLoadIdentity()

            gl.glViewport(0, 0, 1280, 720)
            glu.gluPerspective(45, (1280/720), 0.1, 50.0)
            gl.glTranslatef(0, 0, -5)

            gl.glRotatef(45, 2, 2, 1)
            Cube()

            impl.render(imgui.get_draw_data())
            
            glfw.swap_buffers(window)
    except Exception as e:
        print(e, e.__traceback__.tb_lineno)
    finally:
        impl.shutdown()
        glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    # glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    # glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window

if __name__ == "__main__":
    main()
