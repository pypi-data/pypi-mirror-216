import os
from pathlib import Path
import requests
import typer
from rich import print
from rich.panel import Panel
from lumaCLI.common import (
    validate_json,
    json_to_dict,
    print_response,
)

app = typer.Typer()


@app.command()
def ingest(
    metadata_dir: str = typer.Argument(
        None,
        help="Path to the directory with dbt metadata files. If not provided, current working directory will be used.",
    ),
    endpoint: str = typer.Option(
        ...,
        "--endpoint",
        "-e",
        help="URL of the ingestion endpoint.",
    ),
):
    """
    Sends a bundle of JSON files (manifest.json, catalog.json, sources.json, run_results.json) to a Luma endpoint. If 'metadata_dir' is not specified, the current working directory is used.

    Args:
        metadata_dir (str, optional): Directory path containing all the metadata files. Defaults to current working directory if not provided.
        endpoint (str): The endpoint URL for ingestion.

    Returns:
        response: The HTTP response obtained from the endpoint.
    """
    if metadata_dir is None:
        metadata_dir = os.getcwd()
        print(
            Panel(
                f"[yellow]'metadata_dir' not specified, using current working directory {metadata_dir}[/yellow]"
            )
        )
    # Define JSON paths
    manifest_json_path = os.path.join(metadata_dir, "manifest.json")
    catalog_json_path = os.path.join(metadata_dir, "catalog.json")
    sources_json_path = os.path.join(metadata_dir, "sources.json")
    run_results_json_path = os.path.join(metadata_dir, "run_results.json")

    # Validate each JSON file
    is_manifest_json_valid = validate_json(
        json_path=manifest_json_path, endswith="manifest.json"
    )
    is_catalog_json_valid = validate_json(
        json_path=catalog_json_path, endswith="catalog.json"
    )
    is_sources_json_valid = validate_json(
        json_path=sources_json_path, endswith="sources.json"
    )
    is_run_results_json_valid = validate_json(
        json_path=run_results_json_path, endswith="run_results.json"
    )

    if not all(
        [
            is_manifest_json_valid,
            is_catalog_json_valid,
            is_sources_json_valid,
            is_run_results_json_valid,
        ]
    ):
        raise typer.Exit(1)

    # Convert each JSON to dict
    manifest_dict = json_to_dict(json_path=manifest_json_path)
    catalog_dict = json_to_dict(json_path=catalog_json_path)
    sources_dict = json_to_dict(json_path=sources_json_path)
    run_results_dict = json_to_dict(json_path=run_results_json_path)

    # Define bundle dict
    bundle_dict = {
        "manifest_json": manifest_dict,
        "catalog_json": catalog_dict,
        "sources_json": sources_dict,
        "run_results_json": run_results_dict,
    }

    try:
        response = requests.post(
            endpoint, json=bundle_dict, verify=False, timeout=(3.05, 60 * 30)
        )
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        error_message = (
            "[red]The request has failed. Please check your connection and try again."
        )
        if isinstance(e, requests.exceptions.Timeout):
            error_message += " If you're using a VPN, ensure it's properly connected or try disabling it temporarily."
        elif isinstance(e, requests.exceptions.ConnectionError):
            error_message += (
                " This could be due to maximum retries being exceeded or failure to establish a new connection. "
                "Please check your network configuration."
            )
        print(Panel(error_message + "[/red]"))
        raise typer.Exit(1)

    print_response(response)
    return response


@app.command()
def send_test_results(
    metadata_dir: str = typer.Argument(
        None,
        help="Path to the directory with the run_results.json file. If not provided, current working directory will be used.",
    ),
    endpoint: str = typer.Option(
        ...,
        "--endpoint",
        "-e",
        help="URL of the ingestion endpoint.",
    ),
):
    """
    Sends the run_results.json file located in the specified directory to a Luma endpoint. If 'metadata_dir' is not specified, the current working directory is used.

    Args:
        metadata_dir (str, optional): Directory path containing the run_results.json file. Defaults to current working directory if not provided.
        endpoint (str): The endpoint URL for ingestion.

    Returns:
        response: The HTTP response obtained from the endpoint.
    """
    if metadata_dir is None:
        metadata_dir = os.getcwd()
        print(
            Panel(
                f"[yellow]'metadata_dir' not specified, using current working directory {metadata_dir}[/yellow]"
            )
        )
    run_results_path = Path(metadata_dir) / "run_results.json"
    is_run_results_json_valid = validate_json(run_results_path, "run_results.json")
    if not is_run_results_json_valid:
        raise typer.Exit(1)

    run_results_dict = json_to_dict(json_path=run_results_path)

    try:
        response = requests.post(
            endpoint, json=run_results_dict, verify=False, timeout=(3.05, 60 * 30)
        )
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        error_message = (
            "[red]The request has failed. Please check your connection and try again."
        )
        if isinstance(e, requests.exceptions.Timeout):
            error_message += " If you're using a VPN, ensure it's properly connected or try disabling it temporarily."
        elif isinstance(e, requests.exceptions.ConnectionError):
            error_message += (
                " This could be due to maximum retries being exceeded or failure to establish a new connection. "
                "Please check your network configuration."
            )
        print(Panel(error_message + "[/red]"))
        raise typer.Exit(1)

    print_response(response)
    return response


if __name__ == "__main__":
    app()
