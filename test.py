class A:
    def __init__(self):
        self.name = "A"

    def tests(self):
        print(self.name)


class B(A):
    def __init__(self):
        self.name = "B"

    def run(self):
        self.tests()


class C(A):
    def __init__(self):
        self.name = "C"

    def run(self):
        self.tests()


B().run()
C().run()
B().run()
