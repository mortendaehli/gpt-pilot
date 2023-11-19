from __future__ import print_function, unicode_literals

import builtins
import os
import sys
import traceback
from typing import Optional

import typer

from pilot.database import create_database, database_exists
from pilot.database.database import create_tables, get_created_apps_with_steps, tables_exist
from pilot.helpers.Project import Project
from pilot.logger.logger import logger
from pilot.utils.arguments import get_arguments
from pilot.utils.custom_open import get_custom_open
from pilot.utils.custom_print import get_custom_print
from pilot.utils.exit import exit_gpt_pilot
from pilot.utils.style import color_red

app = typer.Typer()


def init():
    # Check if the "euclid" database exists, if not, create it
    if not database_exists():
        create_database()

    # Check if the tables exist, if not, create them
    if not tables_exist():
        create_tables()

    arguments = get_arguments()

    logger.info("Starting with args: %s", arguments)

    return arguments


@app.command()
def main(
    api_key: Optional[str] = typer.Option(default=None),
    get_created_apps: bool = typer.Option(default=False),
):
    ask_feedback = True
    project = None
    run_exit_fn = True
    try:
        # Override the built-in 'open' with our version
        builtins.open = get_custom_open
        # sys.argv.append('--ux-test=' + 'continue_development')

        args = init()

        builtins.print, ipc_client_instance = get_custom_print(args)

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        if get_created_apps:
            if ipc_client_instance is not None:
                print({"db_data": get_created_apps_with_steps()}, type="info")
            else:
                print("----------------------------------------------------------------------------------------")
                print("app_id                                step                 dev_step  name")
                print("----------------------------------------------------------------------------------------")
                print(
                    "\n".join(
                        f"{app['id']}: {app['status']:20}      "
                        f"{'' if len(app['development_steps']) == 0 else app['development_steps'][-1]['id']:3}"
                        f"  {app['name']}"
                        for app in get_created_apps_with_steps()
                    )
                )
                run_exit_fn = False
        else:
            # TODO get checkpoint from database and fill the project with it
            project = Project(args, ipc_client_instance=ipc_client_instance)
            project.start()
            project.finish()
    except Exception:
        print(color_red("---------- GPT PILOT EXITING WITH ERROR ----------"))
        traceback.print_exc()
        print(color_red("--------------------------------------------------"))
        ask_feedback = False
    finally:
        if run_exit_fn:
            exit_gpt_pilot(project, ask_feedback)
        sys.exit(0)
