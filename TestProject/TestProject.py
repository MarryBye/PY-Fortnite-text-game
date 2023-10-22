# class Vector:
#     def __init__(self, p1: tuple = (0, 0), p2: tuple = (0, 0)):
#         self.p1 = p1
#         self.p2 = p2
#         self.coordinates = (p2[0] - p1[0], p2[1] - p1[1])

#     def __str__(self) -> str:
#         return f"Vector {self.coordinates}"

#     def __add__(self, v):
#         return (self.coordinates[0] + v.coordinates[0], self.coordinates[1] + v.coordinates[1])


# vec1 = Vector((15, 7), (12, 13))
# vec2 = Vector((3, -5), (-5, 16))

# print(vec1)
# print(vec1 + vec2)

class Coordinates:
    LAYER = 0
    ROOM = 1
    LEVEL = 2

class Side:
    TOP = 0
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3


class Map:
    def __init__(self, map: list):
        self.set_map(map=map)

    def set_map(self, map: list):
        self.map = map
        self.level = self.map[0]
        self.room = self.level.scheme[0][0]
        self.coordinates = [0, 0, 0]

    def sign_in_room(self, side: Side):
        match side:
            case Side.TOP:
                if self.room.paths[side]:
                    self.set_room(room=(self.coordinates[Coordinates.LAYER] - 1, self.coordinates[Coordinates.ROOM]))
                else:
                    print("[MapManager] Эта комната недоступна!")
            case Side.LEFT:
                if self.room.paths[side]:
                    self.set_room(room=(self.coordinates[Coordinates.LAYER], self.coordinates[Coordinates.ROOM] - 1))
                else:
                    print("[MapManager] Эта комната недоступна!")
            case Side.BOTTOM:
                if self.room.paths[side]:
                    self.set_room(room=(self.coordinates[Coordinates.LAYER] + 1, self.coordinates[Coordinates.ROOM]))
                else:
                    print("[MapManager] Эта комната недоступна!")
            case Side.RIGHT:
                if self.room.paths[side]:
                    self.set_room(room=(self.coordinates[Coordinates.LAYER], self.coordinates[Coordinates.ROOM] + 1))
                else:
                    print("[MapManager] Эта комната недоступна!")

    def set_room(self, room: tuple):
        try:
            if self.level.scheme[room[Coordinates.LAYER]][room[Coordinates.ROOM]] != None:
                self.coordinates[Coordinates.LAYER] = room[Coordinates.LAYER]
                self.coordinates[Coordinates.ROOM] = room[Coordinates.ROOM]
                self.room = self.level.scheme[room[Coordinates.LAYER]][room[Coordinates.ROOM]]
                print(f"[MapManager] Перемещение в комнату {room}!")
            else:
                print("[MapManager] Эта комната недоступна!")
        except IndexError:
            print("[MapManager] В схеме нет такой комнаты!")

    def get_room(self):
        return self.room

    def set_level(self, level: int):
        try:
            if self.level != self.map[level]:
                self.coordinates[Coordinates.LEVEL] = level
                self.level = self.map[level]
                print(f"[MapManager] Перемещение на уровень {level}!")
                self.set_room(room=(0, 0))
            else:
                print("[MapManager] Вы уже находитесь на этом уровне!")
        except IndexError:
            print("[MapManager] Этого уровня нет на карте!")

    def get_level(self):
        return self.level

    def update(self):
        pass


class Level:
    def __init__(self, scheme: list):
        self.scheme = scheme
        for k_layer, layer in enumerate(scheme):
            for k_room, room in enumerate(layer):
                if room is None:
                    continue
                room.paths[Side.TOP] = k_layer > 0 and scheme[k_layer - 1][k_room] != None
                room.paths[Side.LEFT] = k_room > 0 and scheme[k_layer][k_room - 1] != None
                room.paths[Side.BOTTOM] = k_layer < len(scheme) - 1 and scheme[k_layer + 1][k_room] != None
                room.paths[Side.RIGHT] = k_room < len(layer) - 1 and scheme[k_layer][k_room + 1] != None


class Room:
    def __init__(self):
        self.paths = [False, False, False, False]
        self.no_collide_objects = []
        self.collide_objects = []
        self.items_objects = []

    def place_walls(self):
        if self.paths[Side.TOP]:
            pass
        if self.paths[Side.LEFT]:
            pass
        if self.paths[Side.BOTTOM]:
            pass
        if self.paths[Side.RIGHT]:
            pass


level1 = [
    [Room(),    None,       Room(),     Room(),     Room()],
    [Room(),    Room(),     Room(),     None,       Room()],
    [None,      Room(),     None,       Room(),     Room()],
    [Room(),    Room(),     None,       Room(),     Room()],
    [Room(),    Room(),     Room(),     Room(),     None]
]

level2 = [
    [Room(),    Room(),     None,       None,       Room()],
    [None,      Room(),     Room(),     Room(),     Room()],
    [None,      Room(),     Room(),     Room(),     Room()],
    [None,      None,       None,       Room(),     Room()],
    [Room(),    Room(),     Room(),     Room(),     None]
]

map = [
    Level(scheme=level1),
    Level(scheme=level2)
]

map = Map(map=map)
map.set_room(room=(0, 0))
map.set_room(room=(0, 1))
map.set_room(room=(0, 2))
map.set_room(room=(3, 3))

map.sign_in_room(Side.TOP)
map.sign_in_room(Side.TOP)
map.sign_in_room(Side.TOP)
map.sign_in_room(Side.TOP)
map.sign_in_room(Side.RIGHT)
map.sign_in_room(Side.TOP)
map.sign_in_room(Side.TOP)
map.sign_in_room(Side.TOP)

map.set_level(1)

map.sign_in_room(Side.TOP)
map.sign_in_room(Side.RIGHT)
map.sign_in_room(Side.BOTTOM)