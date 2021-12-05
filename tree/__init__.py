import random
from tree import context, io


class TreeController(object):
    model: context.Context = context.immutableprop(lambda s: s.__context)
    connector: context.ContextConnector = context.immutableprop(lambda s: s.__connection)
    xmas_tree: io.RGBXmasTree = context.immutableprop(lambda s: s.__tree)

    @property
    def is_on(self):
        return self.model.state == context.LightState.ON.value

    def __init__(self):
        self.__context: context.Context = context.Context()
        self.__connection: context.ContextConnector = context.ContextConnector()
        self.__tree: io.RGBXmasTree = io.RGBXmasTree()

    def run(self):
        while True:
            self.load_context()
            if self.is_on:
                self.apply_context()
            self.sleep()

    def load_context(self):
        with self.connector as ctx:
            new_context = ctx
        if self.model.state != new_context.state:
            if new_context.state == context.LightState.ON.value:
                self.xmas_tree.on()
            else:
                self.xmas_tree.off()
        self.__context = new_context

    def apply_context(self):
        self.xmas_tree.brightness = self.model.brightness
        if self.model.mode == context.LightMode.DYNAMIC.value:
            self.apply_dynamic_lighting()
        elif self.model.mode == context.LightMode.RGB.value:
            self.apply_rgb_lighting()
        elif self.model.mode == context.LightMode.LINEAR.value:
            self.apply_linear_lighting()
        else:
            self.apply_static_lighting()

    def apply_static_lighting(self):
        self.xmas_tree.color = (self.model.red, self.model.green, self.model.blue)

    def apply_dynamic_lighting(self):
        pixel = random.choice(self.xmas_tree)
        pixel.color = (random.random(), random.random(), random.random())

    def apply_rgb_lighting(self):
        self.xmas_tree.color = io.Color("red")
        self.sleep()
        self.xmas_tree.color = io.Color("green")
        self.sleep()
        self.xmas_tree.color = io.Color("blue")

    def apply_linear_lighting(self):
        colors = [io.Color("red"), io.Color("green"), io.Color("blue"), io.Color("white")]
        for color in colors:
            for pixel in self.xmas_tree:
                pixel.color = color
                self.sleep()

    def sleep(self):
        from time import sleep
        sleep(self.model.sleep)

    def exit(self):
        self.xmas_tree.off()
        self.xmas_tree.close()
