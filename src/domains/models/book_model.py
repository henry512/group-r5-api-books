from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, Table


Base = declarative_base()


books_authors = Table("books_authors", Base.metadata,
    Column("book_id", String, ForeignKey("books.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True)
)


books_categories = Table("books_categories", Base.metadata,
    Column("book_id", String, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)


class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Book(Base):
    __tablename__ = "books"
    
    id = Column(String, primary_key=True)
    title = Column(String)
    subtitle = Column(String, nullable=True)
    description = Column(String, nullable=True)
    publisher_date = Column(String, nullable=True)
    image = Column(String, nullable=True)
    
    publishing_id = Column(Integer, ForeignKey('publishing.id'))
    publisher = relationship("Publisher", backref=backref("books", lazy=True))
    
    authors = relationship("Author", secondary=books_authors, backref=backref("books", lazy=True))
    categories = relationship("Category", secondary=books_categories, backref=backref("books", lazy=True))
    

class Publisher(Base):
    __tablename__ = 'publishing'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
