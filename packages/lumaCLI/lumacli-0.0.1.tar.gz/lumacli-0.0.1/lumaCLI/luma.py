#!/usr/bin/env python

import typer
import lumaCLI.dbt as dbt


app = typer.Typer()

app.add_typer(dbt.app, name="dbt")


def cli():
    """For python script installation purposes (flit)"""
    app()


if __name__ == "__main__":
    app()
