from janim.imports import *

class HelloJAnimExample(Timeline):
    def construct(self):
        # define items
        circle = Circle(color=BLUE)
        square = Square(color=GREEN, fill_alpha=0.5)

        # do animations
        self.forward()
        self.play(Create(circle))
        self.play(Transform(circle, square))
        self.play(Uncreate(square))
        self.forward()