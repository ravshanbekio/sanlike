
class Query:
    @staticmethod
    def initialize_database(model, fields):
        model.create_table(fields)

    @staticmethod
    def create(model, **kwargs):
        model.insert(**kwargs)

    @staticmethod
    def read_all(model):
        return model.all()

    @staticmethod
    def get_one(model, **filters):
        return model.get(**filters)

    @staticmethod
    def update(model, filters, **kwargs):
        model.update(filters, **kwargs)

    @staticmethod
    def delete(model, **filters):
        model.delete(**filters)