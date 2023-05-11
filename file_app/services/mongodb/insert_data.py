from proyecto_sistemas_inteligentes.mongodb import db_collection_test


class InsertData:
    def __init__(self) -> None:
        pass

    def insert_collection(self, documents):
        db_collection_test.insert_many(documents)