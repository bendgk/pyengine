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
        if not glfw.init():
            raise Exception("GLFWInitException", "failed to initialize glfw!")

        self.glfw_window = glfw.create_window(640, 480, "pyengine-demo", None, None)
        if not self.glfw_window:
            glfw.terminate()
            raise Exception("GLFWWindowCreationException", "failed to create window!")

        glfw.make_context_current(self.glfw_window)

        #moderngl
        self.ctx = moderngl.create_context()

        self.prog = self.ctx.program(
            vertex_shader = """
                #version 330

                in vec3 in_vert;

                void main() {
                    gl_Position = vec4(in_vert, 1.0);
                }
            """,
            fragment_shader = """
                #version 330

                out vec4 f_color;

                void main() {
                    f_color = vec4(1, 1, 1, 1);
                }
            """)

    def on_draw(self):
        global vao

        self.ctx.clear(0.5, 0.7, 1, 1)
        vao.render()

    def on_exit(self):
        glfw.terminate()

if __name__ == '__main__':
    window = Window([640, 480], "pyengine-demo", None, None)
    while not glfw.window_should_close(window.glfw_window):
        #moderngl stuff
        points = np.array([
            -0.5,  -0.5,  0,
            0.5, -0.5,  0,
            0.5, 0.5,  0,
            -0.5, 0.5, 0
        ])

        ibo = window.ctx.buffer(np.asarray([0, 1, 2, 0, 2, 3]).astype('i4').tobytes())
        vbo = window.ctx.buffer(points.astype('f4').tobytes())

        vao_content = [(vbo, '3f', 'in_vert')]
        vao = window.ctx.vertex_array(window.prog, vao_content, ibo)

        window.on_draw()

        glfw.swap_buffers(window.glfw_window)
        glfw.poll_events()

    glfw.terminate()
