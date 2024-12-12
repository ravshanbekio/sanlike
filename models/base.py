from database.connection import DatabaseConnection

class Base:
    table_name = ""

    @classmethod
    def create_table(cls, fields):
        field_definitions = ", ".join([f"{name} {type}" for name, type in fields.items()])
        query = f"CREATE TABLE IF NOT EXISTS {cls.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {field_definitions})"
        with DatabaseConnection(cls.database) as cursor:
            cursor.execute(query)

    @classmethod
    def create(cls, **kwargs):
        keys = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?" for _ in kwargs.values()])
        query = f"INSERT INTO {cls.table_name} ({keys}) VALUES ({placeholders})"
        with DatabaseConnection(cls.database) as cursor:
            cursor.execute(query, tuple(kwargs.values()))
            last_id = cursor.lastrowid 
        return cls._make_instance(cls.get_one(id=last_id))

    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM {cls.table_name}"
        with DatabaseConnection(cls.database) as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return [cls._make_instance(record) for record in data]

    @classmethod
    def get_one(cls, **kwargs):
        conditions = " AND ".join([f"{key}=?" for key in kwargs.keys()])
        query = f"SELECT * FROM {cls.table_name} WHERE {conditions}"
        with DatabaseConnection(cls.database) as cursor:
            cursor.execute(query, tuple(kwargs.values()))
            data = cursor.fetchone()
            return cls._make_instance(data) if data else None
        
    @classmethod
    def get_one_or_none(cls, **kwargs):
        conditions = " AND ".join([f"{key}=?" for key in kwargs.keys()])
        query = f"SELECT * FROM {cls.table_name} WHERE {conditions}"
        with DatabaseConnection(cls.database) as cursor:
            cursor.execute(query, tuple(kwargs.values()))
            if not cursor:
                return None
            data = cursor.fetchone()
            return cls._make_instance(data) if data else None

    @classmethod
    def update(cls, filters, **kwargs):
        updates = ", ".join([f"{key}=?" for key in kwargs.keys()])
        conditions = " AND ".join([f"{key}=?" for key in filters.keys()])
        query = f"UPDATE {cls.table_name} SET {updates} WHERE {conditions}"
        with DatabaseConnection(cls.database) as cursor:
            cursor.execute(query, tuple(kwargs.values()) + tuple(filters.values()))
        return cls._make_instance(cls.get_one(**filters))

    @classmethod
    def delete(cls, **filters):
        data = cls.get_one(**filters)
        if data:
            conditions = " AND ".join([f"{key}=?" for key in filters.keys()])
            query = f"DELETE FROM {cls.table_name} WHERE {conditions}"
            with DatabaseConnection(cls.database) as cursor:
                cursor.execute(query, tuple(filters.values()))
        return data
    
    @classmethod
    def _make_instance(cls, data):
        """Convert a record (tuple) into a dynamic object with field access."""
        if not data:
            return None
        
        class Instance:
            def __init__(self, **fields):
                for key, value in fields.items():
                    setattr(self, key, value)

            def __repr__(self):
                return f"<{cls.table_name.capitalize()} {fields}>"
            
        fields = cls._get_field_names()
        return Instance(**dict(zip(fields, data)))
    
    @classmethod
    def _get_field_names(cls):
        """Retrieve column names for the table."""
        query = f"PRAGMA table_info({cls.table_name})"
        with DatabaseConnection(cls.database) as cursor:
            cursor.execute(query)
            return [info[1] for info in cursor.fetchall()]