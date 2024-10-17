from enum import Enum

# Enumerations for cube faces and colors for readability
class Face(Enum):
    U = 0  # Up
    D = 1  # Down
    F = 2  # Front
    B = 3  # Back
    L = 4  # Left
    R = 5  # Right

class Color(Enum):
    WHITE = 'W'
    YELLOW = 'Y'
    GREEN = 'G'
    BLUE = 'B'
    ORANGE = 'O'
    RED = 'R'

class Cube:
    def __init__(self, size):
        self.size = size

        # Each face of the cube is represented as a 2D list (matrix) of colors.
        # The faces are stored in a dictionary with the Face enum as keys.
        self.faces = {
            Face.U: [[Color.WHITE for _ in range(size)] for _ in range(size)],
            Face.D: [[Color.YELLOW for _ in range(size)] for _ in range(size)],
            Face.F: [[Color.GREEN for _ in range(size)] for _ in range(size)],
            Face.B: [[Color.BLUE for _ in range(size)] for _ in range(size)],
            Face.L: [[Color.ORANGE for _ in range(size)] for _ in range(size)],
            Face.R: [[Color.RED for _ in range(size)] for _ in range(size)],
        }

        # This mapping is used during rotations to determine which rows or columns
        # of adjacent faces need to be updated.
        self.adjacent = {
            Face.U: [(Face.B, 'row', 0), (Face.R, 'row', 0), (Face.F, 'row', 0), (Face.L, 'row', 0)],
            Face.D: [(Face.F, 'row', -1), (Face.R, 'row', -1), (Face.B, 'row', -1), (Face.L, 'row', -1)],
            Face.F: [(Face.U, 'row', -1), (Face.R, 'col', 0), (Face.D, 'row', 0), (Face.L, 'col', -1)],
            Face.B: [(Face.U, 'row', 0), (Face.L, 'col', 0), (Face.D, 'row', -1), (Face.R, 'col', -1)],
            Face.L: [(Face.U, 'col', 0), (Face.F, 'col', 0), (Face.D, 'col', 0), (Face.B, 'col', -1)],
            Face.R: [(Face.U, 'col', -1), (Face.B, 'col', 0), (Face.D, 'col', -1), (Face.F, 'col', -1)],
        }

    # This method handles the rotation of any layer around a specified face. If the outermost layer (layer 0)
    # is being rotated, it also rotates the face itself using rotate_face.
    def rotate_layer(self, face, layer_index, direction):
        size = self.size
        if layer_index == 0:
            self.rotate_face(face, direction)
        self.rotate_adjacent_layers(face, layer_index, direction)

    # Rotates a face 90 degrees in the specified direction (clockwise or counter-clockwise) by rearranging the
    # elements in its 2D list. direction: +1 for clockwise, -1 for counter-clockwise rotation.
    def rotate_face(self, face, direction):
        original = self.faces[face]
        size = self.size
        rotated = [[None]*size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if direction == 1:
                    rotated[j][size - 1 - i] = original[i][j]
                else:
                    rotated[size - 1 - j][i] = original[i][j]
        self.faces[face] = rotated

    # Updates the rows or columns of adjacent faces affected by the rotation. It extracts the relevant layers,
    # rotates them, and then applies them back to the faces.
    def rotate_adjacent_layers(self, face, layer_index, direction):
        seq = self.get_adjacent_sequence(face)
        layers = []
        for adj_face, rc, idx in seq:
            if idx == 'row' or idx == 'col':
                idx = layer_index
            if rc == 'row':
                layer = self.get_row(adj_face, idx)
            else:
                layer = self.get_col(adj_face, idx)
            layers.append(layer)

        # Rotate the layers
        layers = layers[-direction:] + layers[:-direction]

        # Apply the rotated layers back
        for i, (adj_face, rc, idx) in enumerate(seq):
            if idx == 'row' or idx == 'col':
                idx = layer_index
            if rc == 'row':
                self.set_row(adj_face, idx, layers[i])
            else:
                self.set_col(adj_face, idx, layers[i])

    # get_adjacent_sequence get_row, set_row, get_col, and set_col are utility methods to
    # retrieve and set rows or columns on a face.
########################################################
    def get_adjacent_sequence(self, face):
        return self.adjacent[face]

    def get_row(self, face, idx):
        return self.faces[face][idx][:]

    def set_row(self, face, idx, row):
        self.faces[face][idx] = row

    def get_col(self, face, idx):
        return [self.faces[face][i][idx] for i in range(self.size)]

    def set_col(self, face, idx, col):
        for i in range(self.size):
            self.faces[face][i][idx] = col[i]
########################################################
    # print out each face of the cube
    def display(self):
        size = self.size
        for face in Face:
            print(f"Face {face.name}:")
            for row in self.faces[face]:
                print(' '.join([color.value for color in row]))
            print()

# Example usage
if __name__ == "__main__":
    # Create a 3x3 Rubik's Cube
    cube = Cube(3)

    print("Initial Cube State:")
    cube.display()

    # Rotate the front face clockwise
    cube.rotate_layer(Face.F, 0, 1)
    print("After rotating the front face clockwise:")
    cube.display()

    # Rotate the right face counter-clockwise
    cube.rotate_layer(Face.R, 0, -1)
    print("After rotating the right face counter-clockwise:")
    cube.display()

    # Rotate the top layer of the cube along the Y-axis
    cube.rotate_layer(Face.U, 0, 1)
    print("After rotating the top layer along the Y-axis clockwise:")
    cube.display()

    # Rotate the middle layer along the X-axis
    cube.rotate_layer(Face.L, 1, 1)
    print("After rotating the middle layer along the X-axis clockwise:")
    cube.display()

"""
example output:
Initial Cube State:
Face U:
W W W
W W W
W W W

Face D:
Y Y Y
Y Y Y
Y Y Y

Face F:
G G G
G G G
G G G

Face B:
B B B
B B B
B B B

Face L:
O O O
O O O
O O O

Face R:
R R R
R R R
R R R

After rotating the front face clockwise:
Face U:
W W W
W W W
O O O

Face D:
R R R
Y Y Y
Y Y Y

Face F:
G G G
G G G
G G G

Face B:
B B B
B B B
B B B

Face L:
O O Y
O O Y
O O Y

Face R:
W R R
W R R
W R R

After rotating the right face counter-clockwise:
Face U:
W W B
W W B
O O B

Face D:
R R G
Y Y G
Y Y G

Face F:
G G W
G G W
G G O

Face B:
R B B
Y B B
Y B B

Face L:
O O Y
O O Y
O O Y

Face R:
R R R
R R R
W W W

After rotating the top layer along the Y-axis clockwise:
Face U:
O W W
O W W
B B B

Face D:
R R G
Y Y G
Y Y G

Face F:
R R R
G G W
G G O

Face B:
O O Y
Y B B
Y B B

Face L:
G G W
O O Y
O O Y

Face R:
R B B
R R R
W W W

After rotating the middle layer along the X-axis clockwise:
Face U:
Y W W
B W W
B B B

Face D:
R R G
G Y G
G Y G

Face F:
O R R
O G W
B G O

Face B:
O O R
Y B Y
Y B Y

Face L:
G G W
O O Y
O O Y

Face R:
R B B
R R R
W W W
"""