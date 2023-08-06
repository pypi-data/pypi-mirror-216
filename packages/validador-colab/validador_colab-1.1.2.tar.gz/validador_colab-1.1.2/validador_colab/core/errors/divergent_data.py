class DivergentData(Exception):

    def __init__(self, seqproduto, date):
        self.message = f"Dados divergentes para o seqproduto: {seqproduto} na data: {date}"
        super().__init__(self.message)
