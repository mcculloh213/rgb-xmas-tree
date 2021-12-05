import os
from enum import Enum
from util.property import immutableprop

STATE_DIR = "/home/pi/xmas"


class LightMode(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"
    RGB = "rgb"
    LINEAR = "linear"


class LightState(Enum):
    ON = "on"
    OFF = "off"


class ContextConnector(object):
    def __init__(self):
        pass

    def __enter__(self):
        return Context(**ContextConnector.__load_context())

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def __load_context() -> dict:
        context = {}
        try:
            from json import load

            with open(os.path.join(STATE_DIR, "context.json"), "r") as f:
                context.update(load(f))
        finally:
            return context


class Context(object):
    state = immutableprop(lambda s: s.__state)
    mode = immutableprop(lambda s: s.__mode)
    brightness = immutableprop(lambda s: s.__brightness)
    red = immutableprop(lambda s: s.__r)
    green = immutableprop(lambda s: s.__g)
    blue = immutableprop(lambda s: s.__b)
    sleep = immutableprop(lambda s: s.__t)

    def __init__(
        self,
        state: str = "off",
        mode: str = "static",
        brightness: float = 0.5,
        r: int = 255,
        g: int = 255,
        b: int = 255,
        period: float = 2.5,
    ):
        import random
        self.__state: str = state
        self.__mode: str = mode
        self.__brightness: float = brightness
        self.__r: float = random.random() if r == -1 else (r / 255.0)
        self.__g: float = random.random() if g == -1 else (g / 255.0)
        self.__b: float = random.random() if b == -1 else (b / 255.0)
        self.__t: float = period
