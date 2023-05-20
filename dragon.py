class Dragon:
    def __init__(self, position, niveau):
        self.__position = position
        self.__niveau = niveau

    def get_position(self):
        return self.__position

    def get_niveau(self):
        return self.__niveau

    def get_texture(self):
        return "dragon.png"