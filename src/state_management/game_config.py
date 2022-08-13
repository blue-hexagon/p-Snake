class GameConfig:
    game_speed = 150
    stdscr = None
    canvas = None
    h = None
    w = None

    @classmethod
    def get_gamespeed(cls):
        return cls.game_speed

    @classmethod
    def set_h_w(cls, h, w):
        cls.h = h
        cls.w = w

    @classmethod
    def get_h_w(cls):
        return cls.h, cls.w

    @classmethod
    def get_canvas_dimensions(cls):
        return cls.canvas

    @classmethod
    def set_canvas_dimensions(cls, canvas):
        cls.canvas = canvas

    @classmethod
    def get_stdscr(cls):
        return cls.stdscr

    @classmethod
    def set_stdscr(cls, stdscr):
        cls.stdscr = stdscr