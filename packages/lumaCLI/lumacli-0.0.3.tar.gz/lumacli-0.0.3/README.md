# LumaCLI

LumaCLI is a command-line interface tool 🛠️ designed to streamline the interaction with your Luma instance. This utility enables users to send test results or ingest metadata from different tools such as dbt directly to Luma with ease.

## Installation 📦

Install LumaCLI via pip:

```bash
pip install lumaCLI
```

## Usage 🚀

LumaCLI's structure is organized as a tree of commands. At the top level, we have `dbt` and inside `dbt`, we have the sub-commands `ingest` and `send_test_results`.

## 1. dbt

This is the top-level command to interact with dbt metadata.

### 1.1 ingest

The `ingest` command sends a bundle of metadata files (manifest.json, catalog.json, sources.json, run_results.json) from your dbt project to a specified Luma endpoint.

```bash
luma dbt ingest "path/to/your/metadata/directory" --endpoint "https://your-luma-instance/the/endpoint"
```

- `metadata_dir`: (Optional, str) This argument requires the directory path that contains all the metadata files. If not provided, the current working directory will be used.
- `endpoint`: (Required, str) This option allows you to specify the URL of the ingestion endpoint.

This command will validate each JSON file, convert them to dictionaries, bundle them, and send the bundle to the specified Luma endpoint. If the validation for any file fails, the command will exit with a status of 1.

### 1.2 send_test_results

The `send_test_results` command sends a `run_results.json` file to a specified Luma endpoint.

```bash
luma dbt send_test_results "path/to/your/metadata/directory" --endpoint "https://your-luma-instance/the/endpoint"
```

- `metadata_dir`: (Optional, str) This argument requires the directory path that contains the `run_results.json` file. If not provided, the current working directory will be used.
- `endpoint`: (Required, str) This option allows you to specify the URL of the ingestion endpoint.

This command will validate the `run_results.json` file and send it to the specified Luma endpoint. If the validation fails, the command will exit with a status of 1.

## Error Handling ⚠️

If the provided JSON files for either command do not pass validation, the program will terminate and return an exit status of 1. If the HTTP request to the Luma endpoint fails, the program will print the response status and details.
