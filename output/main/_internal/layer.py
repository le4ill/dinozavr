from enum import IntEnum, auto


# Класс для упрощенной работы со слоями
class Layer(IntEnum):
    BACKGROUND = auto()
    OBSTACLE = auto()
    PLAYER = auto()
    UI = auto()
