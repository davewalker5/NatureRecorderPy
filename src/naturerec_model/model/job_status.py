from datetime import datetime
from sqlalchemy import Column, Integer, String, CheckConstraint
from .base import Base


class JobStatus(Base):
    """
    Class representing the status of a background job
    """
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DISPLAY_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

    __tablename__ = "JobStatuses"

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: Job name
    name = Column(String, nullable=False)
    #: Job parameters
    parameters = Column(String, nullable=True)
    #: Start date for the rating. The database is shared between .NET and Python code and Entity Framework
    #: creates a TEXT column in SQLite where data's written in the form YYYY-MM-DD HH:MM:SS. So, while
    #: this field is the one that's persisted to the DB the intention is that it should be accessed via
    #: the corresponding property
    start = Column(String, nullable=False)
    #: End date for the rating - see comments about the start date
    end = Column(String, nullable=True)
    #: Exit error, if any
    error = Column(String, nullable=True)
    #: Audit columns
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint("LENGTH(TRIM(name)) > 0"),
                      CheckConstraint("LENGTH(TRIM(start)) > 0"))

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"parameters={self.parameters!r}, " \
               f"start={self.start!r}, " \
               f"end={self.end!r}, " \
               f"error={self.error!r})"

    @property
    def start_date(self):
        return datetime.strptime(self.start, self.DATE_FORMAT)

    @start_date.setter
    def start_date(self, value):
        self.start = value.strftime(self.DATE_FORMAT) if value else None

    @property
    def end_date(self):
        return datetime.strptime(self.end, self.DATE_FORMAT) if self.end is not None else None

    @end_date.setter
    def end_date(self, value):
        self.end = value.strftime(self.DATE_FORMAT) if value else None

    @property
    def runtime(self):
        if not self.end_date:
            return None

        runtime = self.end_date - self.start_date
        hours, remainder = divmod(runtime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

    @property
    def display_start_date(self):
        return self.start_date.strftime(self.DISPLAY_DATE_FORMAT)

    @property
    def display_end_date(self):
        date = self.end_date
        return date.strftime(self.DISPLAY_DATE_FORMAT) if date else None
