from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Species(Base):
    """
    Class representing an individual species
    """
    __tablename__ = "Species"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Parent category Id
    categoryId = Column(Integer, ForeignKey("Categories.id"), nullable=False)
    #: Species name
    name = Column(String, nullable=False, unique=True)
    #: Audit columns
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)

    #: Parent airline instance
    category = relationship("Category", back_populates="species", lazy="joined")

    __table_args__ = (UniqueConstraint('name', name='SPECIES_NAME_UX'),
                      CheckConstraint("LENGTH(TRIM(name)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, categoryId={self.categoryId!r}, name={self.name!r})"
