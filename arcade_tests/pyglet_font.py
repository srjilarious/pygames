import pyglet

window = pyglet.window.Window()
pyglet.font.add_file("../assets/Inconsolata-Regular.ttf")
pyglet.font.add_file("./AmigaTopaz.ttf")
# label = pyglet.text.Label('Hello, world', font_name="Inconsolata")
label = pyglet.text.Label('Hello, world', font_name="Amiga Topaz Unicode Rus", font_size=20)

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()
