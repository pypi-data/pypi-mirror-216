#!/usr/bin/env python

import typer
import lumaCLI.dbt as dbt
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = typer.Typer()

app.add_typer(dbt.app, name="dbt")


def cli():
    """For python script installation purposes (flit)"""
    app()


if __name__ == "__main__":
    app()
