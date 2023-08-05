# Luma CLI

A CLI tool for managing the data catalog platform.

# Commands

* [luma](./luma.py) 
    * [dbt](./dbt.py) (dbt related commands)
        * ingest

                Sends a bundle json containing manifest.json, catalog.json, sources.json, run_results.json to a luma endpoint.

                Usage:
                    luma dbt ingest "path/to/your/metadata_dir" --endpoint "https://url-of-your-luma-instance/endpoint".

                Sends a bundle json containing manifest.json, catalog.json, sources.json, run_results.json to a luma endpoint.

                Usage:
                    luma dbt ingest "path/to/your/metadata_dir" --endpoint "https://url-of-your-luma-instance/endpoint".

                Sends a bundle json containing manifest.json, catalog.json, sources.json, run_results.json to a luma endpoint.

                Usage:
                luma dbt ingest "path/to/your/metadata_dir" --endpoint "https://url-of-your-luma-instance/endpoint".

                Args:
                metadata_dir (str): Path to the dbt target directory containing the metadata files.
                endpoint (str, optional): The URL endpoint to use for the ingestion. Defaults to "http://localhost:8000/api/dbt/1.3.3".

                Returns:
                response: The response obtained from the endpoint.
        * send-test-results
                Sends run_results.json to a luma endpoint.

                Usage:
                    luma dbt send-test-results "path/to/your/run_results.json" --endpoint "https://url-of-your-luma-instance/endpoint".

                Args:
                    run_results_path (str): file to the run_results.json file.
                    endpoint (str, optional): The URL endpoint to use for the ingestion. Defaults to "http://localhost:8000/api/dbt/1.3.3".

                Returns:
                    response: The response obtained from the endpoint.
    