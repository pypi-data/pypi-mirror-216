from sqlalchemy import ForeignKey, Table, create_engine, Column, Integer, String, DateTime, Boolean, LargeBinary, Tuple
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime


"""
В своем примере я пользуюсь связкой postgres и alembic.
"""

engine = create_engine('postgresql://chat_admin:123456@192.168.1.77/chat')


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True)
    password = Column(String(255))
    data = Column(String)
    sock_number = Column(String(255))
    is_authenticated = Column(Boolean, default=False)
    auth_string = Column(String)
    status_online = Column(Boolean, default=False)
    registered_at = Column(DateTime, default=datetime.utcnow)



class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    client_ip = Column(String(255))
    client_login = Column(String(255), ForeignKey("clients.login"))
    client_message = Column(String)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )




class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    owner_login = Column(String(255), ForeignKey("clients.login"))
    owner_frend = Column(String(255), ForeignKey("clients.login"))
