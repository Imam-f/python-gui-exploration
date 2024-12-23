import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GL.shaders import compileShader, compileProgram

import numpy

import ctypes

import imgui
from imgui.integrations.glfw import GlfwRenderer
from imgui.integrations.base import BaseOpenGLRenderer
# from testwindow import show_test_window

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
    ctx1 = imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    
    pic_x, pic_y = 200, 200
    pic = (pic_x, pic_y)

    ctx2 = imgui.create_context()
    imgui.set_current_context(ctx2)
    io = imgui.get_io()
    io.display_size = pic

    impl_framebuffer = FixedPipelineRenderer()

    # gl.glViewport(0, 0, pic_x, pic_y)
    vertices = [
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ]

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


    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)


    imgui.set_current_context(ctx1)


    show_custom_window = True
    first = True
    pin = False
    focus_pin = False
    pos_elem = (0, 0)
    cpos_elem = (0, 0)
    try:
        while not glfw.window_should_close(window):
            glfw.poll_events()
            imgui.set_current_context(ctx1)
            impl.process_inputs()

            io = imgui.get_io()
            gui_time = impl._gui_time
            delta_time = impl.io.delta_time
            mouse_btn = [impl.io.mouse_down[x] for x in range(3)]
            # is_focused = glfw.get_window_attrib(window, glfw.FOCUSED)
            is_focused = 1
            cursor_pos = tuple([io.mouse_pos[i] - pos_elem[i] for i in range(2)])
            print(mouse_btn, cursor_pos, pos_elem, cpos_elem)

            imgui.set_current_context(ctx2)
            
            impl_framebuffer.process_inputs(
                gui_time,
                delta_time,
                mouse_btn,
                is_focused,
                cursor_pos,
                (pic_x, pic_y),
            )
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
            
            imgui.new_frame()
            # focus_pin = (0 <= cursor_pos[0] < 200) and (0 <= cursor_pos[1] < 200)

            if show_custom_window:
                if first:
                    imgui.set_next_window_size(200, 200)
                    imgui.set_next_window_position(150, 50)
                    first = False
                is_expand, show_custom_window = imgui.begin("Custom window", True)
                if is_expand:
                    # window_position2 = imgui.get_window_position()
                    # focus_pin = imgui.core.is_window_focused()
                    # focus_pin |= imgui.is_item_active()
                    focus_pin = imgui.is_window_hovered()
                    # print(focus_pin, imgui.is_item_activated())
                    print(focus_pin, "             ",  imgui.is_item_hovered(), "          ", imgui.is_window_hovered())
                    imgui.text(f"{focus_pin=}")
                    imgui.text("Bar")
                    imgui.extra.text_ansi_colored("Eggs", 0.2, 1., 0.)
                else:
                    focus_pin = False
                imgui.end()
                
            imgui.render()

            gl.glClearColor(0.0, 0.2, 0.8, 0.5)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            
            gl.glLoadIdentity()
            
            gl.glViewport(0, 0, pic_x, pic_y)
            glu.gluPerspective(45, (1280/720), 0.1, 50.0)
            gl.glScalef(1, -1, 1)

            gl.glUseProgram(shader_program)
            gl.glBindVertexArray(vao)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
            gl.glBindVertexArray(0)
            gl.glUseProgram(0)


            impl_framebuffer.render(imgui.get_draw_data())
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
            
            imgui.set_current_context(ctx1)

            # impl.process_inputs()

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

            if show_custom_window:
                # pos_elem = imgui.get_cursor_pos()
                pin = focus_pin
                print("-- ", pin)
                is_expand, show_custom_window = imgui.begin("Custom window", 
                                                                True, 
                                                                imgui.WINDOW_NO_MOVE if pin else 0
                                                                )
                # window_position = imgui.get_window_position()
                if is_expand:
                    if imgui.button("Pin"):
                        pin = not pin
                    imgui.text("Bar")
                    imgui.text_ansi("B\033[31marA\033[mnsi ")
                    imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)
                    imgui.extra.text_ansi_colored("Eggs", 0.2, 1., 0.)
                    cpos_elem = imgui.get_cursor_position()
                    # pos_elem = imgui.get_cursor_pos()
                    with imgui.extra.styled(imgui.STYLE_WINDOW_PADDING, (0,0)):
                        with imgui.begin_child("Child", 200, 200, False):
                            pos_elem = imgui.get_window_position()
                            imgui.image(texture, pic_x, pic_y, (0, 1), (1, 0))
                imgui.end()

            # show_test_window()
            # imgui.show_test_window()
            imgui.render()

            # io = imgui.get_io()
            # x, y = io.display_size

            gl.glClearColor(0.5, 0.5, 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            gl.glLoadIdentity()
            gl.glViewport(0, 0, 1280, 720)
            glu.gluPerspective(45, (1280/720), 0.1, 50.0)
            gl.glTranslatef(0.0, 0.0, -5)
            gl.glRotatef(1, 7, 1, 15)
            Cube()
            # glPopMatrix()
            impl.render(imgui.get_draw_data())
            
            glfw.swap_buffers(window)
    except Exception as e:
        print(e, e.__traceback__.tb_lineno)
        # imgui.set_current_context(ctx1)
        impl.shutdown()
        
        # gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, framebuffer)
        # gl.glBindTexture(gl.GL_TEXTURE_2D, imagetexture)

        # gl.glReadBuffer(gl.GL_FRONT)
        # pixels = gl.glReadPixels(0, 0, pic_x, pic_y, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)


        # Save pixel data to JPEG using Pygame
        # print(pixels)

        # imgui.set_current_context(ctx2)
        # impl_framebuffer.shutdown()
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

class FixedPipelineRenderer(BaseOpenGLRenderer):
    """Basic OpenGL integration base class."""

    # note: no need to override __init__

    def refresh_font_texture(self):
        # return
        # save texture state
        last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)
        width, height, pixels = self.io.fonts.get_tex_data_as_alpha8()

        print(width, height)

        if self._font_texture is not None:
            gl.glDeleteTextures([self._font_texture])

        self._font_texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._font_texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_ALPHA, width, height, 0, gl.GL_ALPHA, gl.GL_UNSIGNED_BYTE, pixels)

        self.io.fonts.texture_id = self._font_texture
        gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        pass

    def render(self, draw_data):
        # perf: local for faster access
        io = self.io
        # io = IODUMMY()
        # io.display_size = (1280,720)
        # io.display_fb_scale = (1, 1)

        display_width, display_height = io.display_size
        fb_width = int(display_width * io.display_fb_scale[0])
        fb_height = int(display_height * io.display_fb_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        draw_data.scale_clip_rects(*io.display_fb_scale)

        # note: we are using fixed pipeline for cocos2d/pyglet
        # todo: consider porting to programmable pipeline
        # backup gl state
        last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)
        last_viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        last_enable_blend = gl.glIsEnabled(gl.GL_BLEND)
        last_enable_cull_face = gl.glIsEnabled(gl.GL_CULL_FACE)
        last_enable_depth_test = gl.glIsEnabled(gl.GL_DEPTH_TEST)
        last_enable_scissor_test = gl.glIsEnabled(gl.GL_SCISSOR_TEST)
        last_scissor_box = gl.glGetIntegerv(gl.GL_SCISSOR_BOX)
        last_blend_src = gl.glGetIntegerv(gl.GL_BLEND_SRC)
        last_blend_dst = gl.glGetIntegerv(gl.GL_BLEND_DST)
        last_blend_equation_rgb = gl. glGetIntegerv(gl.GL_BLEND_EQUATION_RGB)
        last_blend_equation_alpha = gl.glGetIntegerv(gl.GL_BLEND_EQUATION_ALPHA)

        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_COLOR_BUFFER_BIT | gl.GL_TRANSFORM_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_SCISSOR_TEST)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnable(gl.GL_TEXTURE_2D)

        gl.glViewport(0, 0, int(fb_width), int(fb_height))
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, io.display_size[0], io.display_size[1], 0.0, -1., 1.)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        for commands in draw_data.commands_lists:
            idx_buffer = commands.idx_buffer_data

            gl.glVertexPointer(2, gl.GL_FLOAT, imgui.VERTEX_SIZE, ctypes.c_void_p(commands.vtx_buffer_data + imgui.VERTEX_BUFFER_POS_OFFSET))
            gl.glTexCoordPointer(2, gl.GL_FLOAT, imgui.VERTEX_SIZE, ctypes.c_void_p(commands.vtx_buffer_data + imgui.VERTEX_BUFFER_UV_OFFSET))
            gl.glColorPointer(4, gl.GL_UNSIGNED_BYTE, imgui.VERTEX_SIZE, ctypes.c_void_p(commands.vtx_buffer_data + imgui.VERTEX_BUFFER_COL_OFFSET))

            for command in commands.commands:
                gl.glBindTexture(gl.GL_TEXTURE_2D, command.texture_id)

                x, y, z, w = command.clip_rect
                gl.glScissor(int(x), int(fb_height - w), int(z - x), int(w - y))

                if imgui.INDEX_SIZE == 2:
                    gltype = gl.GL_UNSIGNED_SHORT
                else:
                    gltype = gl.GL_UNSIGNED_INT

                gl.glDrawElements(gl.GL_TRIANGLES, command.elem_count, gltype, ctypes.c_void_p(idx_buffer))

                idx_buffer += (command.elem_count * imgui.INDEX_SIZE)

        gl.glBlendEquationSeparate(last_blend_equation_rgb, last_blend_equation_alpha)
        gl.glBlendFunc(last_blend_src, last_blend_dst)

        if last_enable_blend:
            gl.glEnable(gl.GL_BLEND)
        else:
            gl.glDisable(gl.GL_BLEND)

        if last_enable_cull_face:
            gl.glEnable(gl.GL_CULL_FACE)
        else:
            gl.glDisable(gl.GL_CULL_FACE)

        if last_enable_depth_test:
            gl.glEnable(gl.GL_DEPTH_TEST)
        else:
            gl.glDisable(gl.GL_DEPTH_TEST)

        if last_enable_scissor_test:
            gl.glEnable(gl.GL_SCISSOR_TEST)
        else:
            gl.glDisable(gl.GL_SCISSOR_TEST)

        gl.glScissor(last_scissor_box[0], last_scissor_box[1], last_scissor_box[2], last_scissor_box[3])

        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        if last_texture:
            gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glPopAttrib()

        gl.glViewport(last_viewport[0], last_viewport[1], last_viewport[2], last_viewport[3])

    def _invalidate_device_objects(self):
        if self._font_texture > -1:
            gl.glDeleteTextures([self._font_texture])
        self.io.fonts.texture_id = 0
        self._font_texture = 0

    def process_inputs(self, gui_time, delta_time, 
                       mouse_btn, is_focused, cursor_pos,
                       window_size):
        io = imgui.get_io()

        io.display_size = window_size
        io.display_fb_scale = (1, 1)

        if is_focused:
            io.mouse_pos = cursor_pos
        else:
            io.mouse_pos = -1, -1

        io.mouse_down[0] = mouse_btn[0]
        io.mouse_down[1] = mouse_btn[1]
        io.mouse_down[2] = mouse_btn[2]


        io.delta_time = 1.0/60
        self.io.delta_time = delta_time
        if(io.delta_time <= 0.0): io.delta_time = 1./ 1000.
        self._gui_time = gui_time

if __name__ == "__main__":
    main()
