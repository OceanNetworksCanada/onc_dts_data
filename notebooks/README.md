# Notebooks

This directory contains Jupyter notebooks for acquiring, processing, and visualizing Distributed Temperature Sensing (DTS) data from Ocean Networks Canada (ONC).

## Prerequisites

Before running the notebooks, make sure you have:

1. A valid ONC API token (see [Obtaining an API Token](../README.md#obtain-your-onc-api-token)).
2. A `.env` file in the `notebooks/` directory with the following content:
   ```
   ONC_API_TOKEN=your_api_token_here
   ```
3. Required Python packages installed (see `pyproject.toml` at the root of the repository).

---

## Notebook Overview

### [1.1 — Explore XT Files](./1.1-mhee_explore_xt_files.ipynb)

**Author:** mhee

Explores the raw `.xt` binary files produced by the Silixa DTS instrument. Uses the `onc_dts` library to read and parse `.xt` files, then visualises the temperature profiles along the fibre-optic cable using `plot_dts_data`. Also demonstrates how to build an `xarray.DataArray` from raw DTS JSON response data (base64-encoded binary arrays) for more advanced analysis.

**Key steps:**
- Read `.xt` files with `read_xt_file` (with optional trimming and raw-data inclusion).
- Plot temperature profiles along depth/distance using `plot_dts_data`.
- Decode base64-encoded binary payloads from the ONC API JSON response into a structured `xarray` dataset.

---

### [2.0 — Get ONC Realtime Data](./2.0-mhee_Get_ONC_Realtime_Data.ipynb)

**Author:** mhee

Demonstrates how to fetch **real-time** raw DTS readings directly from the ONC REST API using the `requests` library. Data are saved locally as JSON files for subsequent processing.

**Key steps:**
- Authenticate with the ONC API using a token loaded from a `.env` file.
- Call the `/rawdata/device` endpoint to retrieve the latest rows of raw DTS data for a given `deviceCode`.
- Parse the multi-line response, filter valid `getData` JSON records, and persist them to `data/realtime/`.
- Also shows how to fetch **archived** raw data from the same API.

**Reference:** [ONC OpenAPI — `/rawdata/device`](https://data.oceannetworks.ca/OpenAPI#get-/rawdata/device)

---

### [3.0 — Get ONC Archive Files](./3.0-aschlesin_Get_ONC_ArchiveFiles.ipynb)

**Author:** aschlesin

Shows how to retrieve **archived** JSON files from the ONC database using the official [`onc` Python client library](https://oceannetworkscanada.github.io/api-python-client/).

**Key steps:**
- Authenticate via the `ONC` client class.
- Query archived files for a specific `deviceCode` over a date range (ISO 8601 format), filtering by file extension (e.g., `JSON`).
- Save the returned archive files locally to `data/archive/`.

---

### [4.0 — Plot JSON Data](./4.0-aschlesin_Plot_JSON_Data.ipynb)

**Author:** aschlesin

Reads the JSON files downloaded (or generated) by the previous notebooks and produces publication-quality DTS temperature plots.

**Key steps:**
- Parse saved JSON files with `read_JSON_file`, decoding base64-encoded binary temperature arrays and extracting per-channel metadata.
- Visualise multi-channel temperature profiles along the fibre-optic cable with `plot_dts_data`, including optional raw-signal overlays and configurable temperature ranges.
- Batch-process multiple JSON files using glob patterns.
