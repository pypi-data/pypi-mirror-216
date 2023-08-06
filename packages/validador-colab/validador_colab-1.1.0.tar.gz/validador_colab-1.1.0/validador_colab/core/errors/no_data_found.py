class NoDataFound(Exception):

    def __init__(self):
        self.message = "Não há dados cadastrados para este cliente."
        super().__init__(self.message)
