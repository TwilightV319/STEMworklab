from janim.imports import *

class TestScene(Timeline):
    def construct(self):
        NumberPlane(faded_line_ratio=1).show()

        square1 = Square(color=RED, fill_alpha=1)
        square2 = Square(color=GREEN, fill_alpha=1)
        square3 = Square(color=BLUE, fill_alpha=1)

        square2.points.rotate(PI / 2, axis=UP)
        square3.points.rotate(PI / 2, axis=RIGHT)

        squares = Group(square1, square2, square3)
        squares.show()

        self('camera')