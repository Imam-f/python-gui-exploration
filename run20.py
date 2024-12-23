import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GL.shaders import compileShader, compileProgram

import numpy



def main():

    # ctx1 = imgui.create_context()
    window = impl_glfw_init()
    
    pic_x, pic_y = 1280, 720
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

    vertices = numpy.array(vertices, dtype=numpy.float32)

    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)

    # gl.glBufferData(gl.GL_ARRAY_BUFFER, len(vertices) * 3, (gl.GLfloat * len(vertices))(*vertices), gl.GL_STATIC_DRAW)
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


#     framebuffer = gl.glGenFramebuffers(1)
#     gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
# 
#     texture = gl.glGenTextures(1)
#     gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
#     gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, pic_x, pic_y, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
#     gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
#     gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
# 
# 
#     rbo = gl.glGenRenderbuffers(1)
#     gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, rbo)
#     gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH24_STENCIL8, pic_x, pic_y)
#     gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)
# 
#     gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
#     gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
#     gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)


    show_custom_window = True
    
    try:
        while not glfw.window_should_close(window):
            # imgui.set_current_context(ctx1)
            glfw.poll_events()

            gl.glClearColor(0.5, 0.5, 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            
            
            # gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
            gl.glUseProgram(shader_program)
            gl.glBindVertexArray(vao)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
            gl.glBindVertexArray(0)
            gl.glUseProgram(0)
            # gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
            
            # imgui.new_frame()

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
            
            
            glfw.swap_buffers(window)
    except Exception as e:
        print(e, e.__traceback__.tb_lineno)
    finally:
        glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

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
