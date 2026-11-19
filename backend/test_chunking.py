
from app.services.chunk_service import split_document


sample_text = """
Python is a high-level programming language.
Python supports object-oriented programming.
Python is commonly used for web development.

Django is a Python web framework.
Django provides tools for building web applications.
Django includes an ORM for database operations.

FastAPI is a modern Python framework.
FastAPI is used to build REST APIs.
FastAPI supports asynchronous programming.

React is a JavaScript library.
React is used to build user interfaces.
React uses reusable components.

MySQL is a relational database.
PostgreSQL is another relational database.
Both databases can be used with Python applications.
""" * 5


chunks = split_document(sample_text)


print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):

    print(f"\n========== CHUNK {index} ==========")

    print(chunk)

    print("Character count:", len(chunk))
