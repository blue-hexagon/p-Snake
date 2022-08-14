class GameConfig:
    _game_speed = None
    _stdscr = None
    _canvas = None
    _h = None
    _w = None
    _no_of_obstacles = None

    @classmethod
    def get_gamespeed(cls):
        return cls._game_speed

    @classmethod
    def set_h_w(cls, h, w):
        cls._h = h
        cls._w = w

    @classmethod
    def get_h_w(cls):
        return cls._h, cls._w

    @classmethod
    def get_canvas_dimensions(cls):
        return cls._canvas

    @classmethod
    def set_canvas_dimensions(cls, canvas):
        cls._canvas = canvas

    @classmethod
    def get_stdscr(cls):
        return cls._stdscr

    @classmethod
    def set_stdscr(cls, stdscr):
        cls._stdscr = stdscr

    @classmethod
    def set_number_of_obstacles(cls, no_of_obstacles):
        cls._no_of_obstacles = no_of_obstacles

    @classmethod
    def get_no_of_obstacles(cls):
        return cls._no_of_obstacles

    @classmethod
    def set_game_speed(cls, game_speed):
        """Unit is milliseconds"""
        cls._game_speed = game_speed
