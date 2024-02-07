from peewee import CharField
from kyb.models.common import Temporal


class CrunchBaseCompany(Temporal):
    name = CharField()
    url = CharField()
