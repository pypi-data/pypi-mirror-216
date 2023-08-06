class SmarketCounter:

    def __init__(self, seqproduto: int, date: str,
                 description: str, ean: str, analytics: int,
                 client_id: int):

        self.seqproduto = seqproduto
        self.date = date
        self.description = description
        self.ean = ean
        self.analytics = analytics
        self.client_id = client_id

    
