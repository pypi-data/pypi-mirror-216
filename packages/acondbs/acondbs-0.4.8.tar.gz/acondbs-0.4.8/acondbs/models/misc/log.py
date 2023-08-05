import datetime

from acondbs.db.sa import sa


class Log(sa.Model):  # type: ignore
    __tablename__ = "log"
    id_ = sa.Column(sa.Integer(), primary_key=True)
    level = sa.Column(sa.Text())
    message = sa.Column(sa.Text())
    time = sa.Column(sa.DateTime(), default=lambda: datetime.datetime.now())

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.time}>"
