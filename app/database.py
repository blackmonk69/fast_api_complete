from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Maria182*@localhost/fastapi'

# 1. Crea el motor (engine) que maneja la conexión con PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. Crea una clase SessionLocal para abrir sesiones con la base de datos
SessionLocal = sessionmaker(
    autocommit=False,  # No hace commit automáticamente después de cada operación
    autoflush=False,   # No envía cambios automáticamente hasta que lo decidas
    bind=engine        # La sesión se conecta con el engine definido
)

# 3. Crea una clase Base para definir los modelos (tablas)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()