from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Category(Base):
    """
    Class representing the top-level categorisation into e.g. birds, insects etc.
    """
    __tablename__ = "Categories"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Category name
    name = Column(String, nullable=False, unique=True)

    #: Species associated with this category
    species = relationship("Species",
                           back_populates="category",
                           cascade="all, delete, delete-orphan",
                           lazy="joined")

    __table_args__ = (UniqueConstraint('name', name='CATEGORY_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(Id={self.id!r}, name={self.name!r})"
