class Game:
    class_name = ""
    score = 0
    objects = {}

    def __init__(self, name):
        self.name = name
        Game.objects[self.class_name] = self

    def get_decription(self):
        return self._score


class PlayerOne(Game):
    def __init__(self, name):
        self.class_name = "PlayerOne"
        self._score = 0
        self._attack = False
        self._attack_time = 0
        self._block = False
        self._block_time = 0
        super().__init__(name)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def attack_time(self):
        return self._attack_time

    @attack_time.setter
    def attack_time(self, value):
        self._attack_time = value

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, value):
        self._block = value

    @property
    def block_time(self):
        return self._block_time

    @block_time.setter
    def block_time(self, value):
        self._block_time = value


class PlayerTwo(Game):
    def __init__(self, name):
        self.class_name = "PlayerTwo"
        self._score = 0
        self._attack = False
        self._attack_time = 0
        self._block = False
        self._block_time = 0
        super().__init__(name)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def attack_time(self):
        return self._attack_time

    @attack_time.setter
    def attack_time(self, value):
        self._attack_time = value

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, value):
        self._block = value

    @property
    def block_time(self):
        return self._block_time

    @block_time.setter
    def block_time(self, value):
        self._block_time = value
