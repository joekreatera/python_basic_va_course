class InputManager:
    arrowUp = "arrow_up"
    arrowLeft = "arrow_left"
    arrowRight = "arrow_right"
    arrowDown = "arrow_down"
    space = "space"
    keyA = "a"
    keyS = "s"
    keyV = "v"
    keyX = "x"


    instance = None

    @staticmethod
    def initWith(app , list):
        print(app)
        InputManager.instance = InputManager()

        for i in list:
            evt = i
            InputManager.instance.setInput(evt , False)
            app.accept( "raw-" + evt, InputManager.createInputFunction(evt, InputManager.instance, True)  )
            app.accept( "raw-" + evt + "-up",  InputManager.createInputFunction(evt, InputManager.instance, False) )

    @staticmethod
    def createInputFunction(evt, inputManagerObject, down=True):
        def receiveInput():
            #print(evt + " [DOWN]:" + str(down) )
            inputManagerObject.setInput(evt, down)
        return receiveInput

    @staticmethod
    def isInputDown(inp):
        return InputManager.instance.getInput(inp)

    def __init__(self):
        self.input = {}

    def getInput(self, input):
        return self.input[input]

    def setInput(self, input, value = False):
        self.input[input] = value
