from playhouse.postgres_ext import BinaryJSONField

from pilot.database.config import DATABASE_TYPE
from pilot.database.models.components.progress_step import ProgressStep
from pilot.database.models.components.sqlite_middlewares import JSONField


class DevelopmentPlanning(ProgressStep):
    if DATABASE_TYPE == "postgres":
        development_plan = BinaryJSONField()
    else:
        development_plan = JSONField()  # Custom JSON field for SQLite

    class Meta:
        table_name = "development_planning"
