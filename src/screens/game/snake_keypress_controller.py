import curses


class InGameKeyPress:
    def __init__(self, head):
        self.head = head

    def get_keypress_object(self, direction):
        if direction == curses.KEY_RIGHT:
            return InGameKeyPressRight(self.head)
        elif direction == curses.KEY_LEFT:
            return InGameKeyPressLeft(self.head)
        elif direction == curses.KEY_UP:
            return InGameKeyPressUp(self.head)
        elif direction == curses.KEY_DOWN:
            return InGameKeyPressDown(self.head)
        else:
            raise KeyError("Key not recognized.")


class InGameKeyPressRight(InGameKeyPress):
    def __init__(self, head):
        super().__init__(head)
        self.key = curses.KEY_RIGHT
        self.snake_symbol_head = "─"
        self.new_head = [self.head[0], self.head[1] + 1]

    @staticmethod
    def determine_neck_symbol(prev_direction):
        if prev_direction == curses.KEY_UP:
            return "╭"
        elif prev_direction == curses.KEY_DOWN:
            return "╰"
        elif prev_direction == curses.KEY_LEFT or prev_direction == curses.KEY_RIGHT:
            return "─"


class InGameKeyPressLeft(InGameKeyPress):
    def __init__(self, head):
        super().__init__(head)
        self.key = curses.KEY_LEFT
        self.snake_symbol_head = "─"
        self.new_head = [self.head[0], self.head[1] - 1]

    @staticmethod
    def determine_neck_symbol(prev_direction):
        if prev_direction == curses.KEY_UP:
            return "╮"
        elif prev_direction == curses.KEY_DOWN:
            return "╯"
        elif prev_direction == curses.KEY_LEFT or prev_direction == curses.KEY_RIGHT:
            return "─"


class InGameKeyPressUp(InGameKeyPress):
    def __init__(self, head):
        super().__init__(head)
        self.key = curses.KEY_UP
        self.snake_symbol_head = "│"
        self.new_head = [self.head[0] - 1, self.head[1]]

    @staticmethod
    def determine_neck_symbol(prev_direction):
        if prev_direction == curses.KEY_UP or prev_direction == curses.KEY_DOWN:
            return "│"
        elif prev_direction == curses.KEY_LEFT:
            return "╰"
        elif prev_direction == curses.KEY_RIGHT:
            return "╯"


class InGameKeyPressDown(InGameKeyPress):
    def __init__(self, head):
        super().__init__(head)
        self.key = curses.KEY_UP
        self.snake_symbol_head = "│"
        self.new_head = [self.head[0] + 1, self.head[1]]

    @staticmethod
    def determine_neck_symbol(prev_direction):
        if prev_direction == curses.KEY_UP or prev_direction == curses.KEY_DOWN:
            return "│"
        elif prev_direction == curses.KEY_LEFT:
            return "╭"
        elif prev_direction == curses.KEY_RIGHT:
            return "╮"
