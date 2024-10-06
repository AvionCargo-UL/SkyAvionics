class ApplicationVariableNotFoundException(RuntimeError):

    MESSAGE: str = "Application variable not found at %s, %s"

    def __init__(self, header: str, variable_name: str):
        super().__init__(self.MESSAGE % (header, variable_name))
