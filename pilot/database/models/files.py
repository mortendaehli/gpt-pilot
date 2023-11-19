from peewee import AutoField, CharField, ForeignKeyField, TextField

from pilot.database.models.app import App
from pilot.database.models.components.base_models import BaseModel


class File(BaseModel):
    id = AutoField()
    app = ForeignKeyField(App, on_delete="CASCADE")
    name = CharField()
    path = CharField()
    full_path = CharField()
    description = TextField(null=True)

    class Meta:
        indexes = ((("app", "name", "path"), True),)
