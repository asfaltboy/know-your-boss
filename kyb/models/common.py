from peewee import Model, SqliteDatabase, DateField

db = SqliteDatabase("kyb.db")


class Temporal(Model):
    updated_at = DateField()
    created_at = DateField()

    class Meta:
        database = db
