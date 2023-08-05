from acondbs.db.sa import sa


class AccountAdmin(sa.Model):  # type: ignore
    __tablename__ = "account_admins"
    admin_id = sa.Column(sa.Integer(), primary_key=True)
    git_hub_login = sa.Column(sa.Text(), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.git_hub_login!r}>"
