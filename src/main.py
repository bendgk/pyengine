import moderngl
import glfw
import numpy as np

class Window:
    def __init__(self, size=(640, 480), title="window", monitor=None, share=None):
        self.x = size[0]
        self.y = size[1]
        self.title = title
        self.monitor = monitor
        self.share = share

        #glfw
        if not glfw.init(): raise Exception("GLFWInitException", "failed to initialize glfw!")

        #window hints
        glfw.window_hint(glfw.RESIZABLE, True)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        #only for macOS
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

        self.glfw_window = glfw.create_window(self.x, self.y, self.title, None, None)
        if not self.glfw_window:
            glfw.terminate()
            raise Exception("GLFWWindowCreationException", "failed to create window!")

        glfw.make_context_current(self.glfw_window)

        #glfw callbacks
        glfw.set_framebuffer_size_callback(self.glfw_window, self.framebuffer_size_callback)

        #moderngl
        self.ctx = moderngl.create_context()

        self.prog = self.ctx.program(
#            vertex_shader = """
#                #version 330
#
#                in vec3 in_vert;
#
#                void main() {
#                    gl_Position = vec4(in_vert, 1.0);
#                }
#            """,
#            fragment_shader = """
#                #version 330
#
#                out vec4 f_color;
#
#                void main() {
#                    f_color = vec4(1, 1, 1, 1);
#                }
#            """
            vertex_shader='''
                #version 330
                in vec2 in_vert;
                in vec3 in_color;
                out vec3 v_color;    // Goes to the fragment shader
                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                    v_color = in_color;
                }
            ''',
            fragment_shader='''
                #version 330
                in vec3 v_color;
                out vec4 f_color;
                void main() {
                    // We're not interested in changing the alpha value
                    f_color = vec4(v_color, 1.0);
                }
            '''
            )

    def framebuffer_size_callback(self, window, width, height):
        self.on_draw()

        glfw.swap_buffers(self.glfw_window)
        glfw.poll_events()

    def on_input(self):
        if glfw.get_key(self.glfw_window, glfw.KEY_ESCAPE) == True:
            glfw.set_window_should_close(self.glfw_window, True)

    def on_draw(self):
        global vao

        self.ctx.clear(0.5, 0.7, 1, 1)
        vao.render()

    def on_exit(self):
        glfw.terminate()

if __name__ == '__main__':
    window = Window([640, 480], "pyengine-demo", None, None)
    
    """
    points = np.array([
        -0.5,  -0.5,  0,
        0.5, -0.5,  0,
        0.5, 0.5,  0,
        -0.5, 0.5, 0
    ])
    """
    
    vertices = np.array([
            # x, y, red, green, blue
            0.0, 0.8, 1.0, 0.0, 0.0,
            -0.6, -0.8, 0.0, 1.0, 0.0,
            0.6, -0.8, 0.0, 0.0, 1.0,
        ])

    while not glfw.window_should_close(window.glfw_window):
        #moderngl stuff
        
        """
        ibo = window.ctx.buffer(np.asarray([0, 1, 2, 0, 2, 3]).astype('i4').tobytes())
        vbo = window.ctx.buffer(points.astype('f4').tobytes())

        vao_content = [(vbo, '3f', 'in_vert')]
        vao = window.ctx.vertex_array(window.prog, vao_content, ibo)
        """
        
        vbo = window.ctx.buffer(vertices.astype('f4').tobytes())

        # We control the 'in_vert' and `in_color' variables
        vao = window.ctx.simple_vertex_array(window.prog, vbo, 'in_vert', 'in_color')
        
        window.on_input()

        window.on_draw()

        glfw.swap_buffers(window.glfw_window)
        glfw.poll_events()

    glfw.terminate()
