from dotenv import load_dotenv
import os
from models.base import Base

load_dotenv()

class Channel(Base):
    database = os.getenv("DATABASE_URL")
    table_name = "Channels"

if __name__ == "__main__":
    # Initialize the database
    Channel.create_table({
        "name": "TEXT",
        "email": "TEXT",
        "age": "INTEGER"
    })

    # Add a new user
    query = Channel.create(name="John Doe", email="john@example.com", age=30)
    print(query)

    # List all users
    users = Channel.get_all()
    print("All Users:", users)

    # Find a specific user
    user = Channel.get_one(name="John Doe")
    print("Fetched User:", user)

    # Update a user
    if user:
        user = Channel.update({"id": 1}, name="John Updated", age=31)
        print(user.id)

    # Delete a user
    if user:
        user = Channel.delete(id=2)
        print()
