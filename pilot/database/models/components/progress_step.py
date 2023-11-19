from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField
from playhouse.postgres_ext import BinaryJSONField

from pilot.database.config import DATABASE_TYPE
from pilot.database.models.app import App
from pilot.database.models.components.base_models import BaseModel
from pilot.database.models.components.sqlite_middlewares import JSONField


class ProgressStep(BaseModel):
    app = ForeignKeyField(App, primary_key=True, on_delete="CASCADE")
    step = CharField()

    if DATABASE_TYPE == "postgres":
        app_data = BinaryJSONField()
        data = BinaryJSONField(null=True)
        messages = BinaryJSONField(null=True)
    else:
        app_data = JSONField()
        data = JSONField(null=True)
        messages = JSONField(null=True)

    completed = BooleanField(default=False)
    completed_at = DateTimeField(null=True)
