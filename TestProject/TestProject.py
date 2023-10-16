class Vector:
    def __init__(self, p1: tuple = (0, 0), p2: tuple = (0, 0)):
        self.p1 = p1
        self.p2 = p2
        self.coordinates = (p2[0] - p1[0], p2[1] - p1[1])

    def __str__(self) -> str:
        return f"Vector {self.coordinates}"

    def __add__(self, v):
        return (self.coordinates[0] + v.coordinates[0], self.coordinates[1] + v.coordinates[1])


vec1 = Vector((15, 7), (12, 13))
vec2 = Vector((3, -5), (-5, 16))

print(vec1)
print(vec1 + vec2)
