class GameConfig:
    _game_speed = None
    _stdscr = None
    _canvas = None
    _h = None
    _w = None
    _no_of_obstacles = None

    @classmethod
    def get_gamespeed(cls):
        if cls._game_speed is not None:
            return cls._game_speed
        raise ValueError("Value not initialized yet.")

    @classmethod
    def set_game_speed(cls, game_speed):
        """Unit is milliseconds"""
        cls._game_speed = game_speed

    @classmethod
    def get_h_w(cls):
        if cls._h is not None and cls._w is not None:
            return cls._h, cls._w
        raise ValueError("Value not initialized yet.")

    @classmethod
    def set_h_w(cls, h, w):
        cls._h = h
        cls._w = w

    @classmethod
    def get_canvas_dimensions(cls):
        if cls._canvas is not None:
            return cls._canvas
        raise ValueError("Value not initialized yet.")

    @classmethod
    def set_canvas_dimensions(cls, canvas):
        cls._canvas = canvas

    @classmethod
    def get_stdscr(cls):
        if cls._stdscr is not None:
            return cls._stdscr
        raise ValueError("Value not initialized yet.")

    @classmethod
    def set_stdscr(cls, stdscr):
        cls._stdscr = stdscr

    @classmethod
    def get_no_of_obstacles(cls):
        if cls._no_of_obstacles is not None:
            return cls._no_of_obstacles
        raise ValueError("Value not initialized yet.")

    @classmethod
    def set_number_of_obstacles(cls, no_of_obstacles):
        cls._no_of_obstacles = no_of_obstacles
