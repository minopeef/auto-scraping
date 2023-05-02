
class Store:

    mode = "Auto"
    flag = False
    status = "None"

    class Auto:
        flag = False
        status = "None"
    
    class Manual:
        flag = False
        status = "None"

    def __init__(self) -> None:
        pass