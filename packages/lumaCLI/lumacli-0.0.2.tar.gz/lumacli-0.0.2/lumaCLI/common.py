import json
import os
from pathlib import Path
from rich import print
from rich.panel import Panel


def validate_json(json_path: str, endswith: str = ".json") -> bool:
    """
    Validates whether the provided file is a valid JSON file and ends with the specified string.

    Args:
        json_path (str): The full path to the file to be validated.
        endswith (str, optional): The string the file should end with. Defaults to ".json".

    Returns:
        bool: True if valid, False otherwise.
    """
    file = Path(json_path)

    # Check that file exists
    if not file.is_file():
        error_message = f"[red]Error[/red]: [yellow]{file.absolute()}[/yellow] [blue]is not a file[/blue]"
        print(Panel(error_message))
        return False

    # Check that filename ends with the required string
    if not str(file).endswith(endswith):
        error_message = f"[red]Error[/red]: [blue]File[/blue] [yellow]{os.path.basename(file.absolute())}[/yellow] [blue]does not have the required structure, it should end with [/blue][yellow]'{endswith}'[/yellow]"
        print(Panel(error_message))
        return False

    return True


def json_to_dict(json_path):
    """
    Converts a JSON file to a dictionary.

    Args:
        json_path (str): The full path to the JSON file.

    Returns:
        dict: The JSON data as a dictionary.
    """
    with open(json_path, "r") as json_file:
        json_data: dict = json.load(json_file)
    return json_data


def print_response(response):
    """
    Prints the HTTP response.

    Args:
        response (Response): The HTTP response to be printed.
    """
    if not response.ok:
        try:
            print(
                Panel(
                    f"[red]An HTTP error occurred, response status code[/red]: {response.status_code} {json.loads(response.text)['detail']}"
                )
            )
        except:
            print(
                Panel(
                    f"[red]An HTTP error occurred, response status code[/red]: {response.status_code} {response.text}"
                )
            )
    else:
        print(
            Panel(
                "[green]The dbt ingestion to luma was successful!\nItems ingested:[/green]"
            )
        )
        try:
            print(response.json())
        except:
            print("Error at printing items ingested")
