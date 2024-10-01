from sqlalchemy import create_engine

def connect_to_db():
   engine = create_engine("postgresql://postgres:123@0.0.0.0:6000/twait")
   conn = engine.connect()
   
   print(conn)

connect_to_db()
