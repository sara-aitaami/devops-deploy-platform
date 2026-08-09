from sqlalchemy import text

from backend.app.database import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM applications"))
    
    for row in result:
        print(row)