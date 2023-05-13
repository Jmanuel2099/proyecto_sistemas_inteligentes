from proyecto_sistemas_inteligentes.mongodb import db


class InsertData:
    def __init__(self) -> None:
        pass

    def insert_collection(self, documents, collection):
        db_collection = db.get_collection(collection)
        db_collection.insert_many(documents)