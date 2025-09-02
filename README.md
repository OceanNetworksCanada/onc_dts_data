# ONC-DTS: Ocean Networks Canada Distributed Temperature Sensing

> **⚠️ EARLY DEVELOPMENT NOTICE**: This package is in early stages and under heavy development. APIs and functionality may change frequently without notice. Use with caution in production environments.

A Python library for plotting data retrieved from Silixa Distributed Temperature Sensing (DTS) systems.

## Content
This repository contains code and jupyter notebook tutorial on data acquisiton, processing, and plotting of the distributed temperature sensor (DTS) which is owned by University of Rhode Island research group (see [PhD thesis of Johann Becker](https://digitalcommons.uri.edu/oa_diss/4440/) )

The jupyter notebooks on how to access data in ONCs database and processing can be found here: [notebooks](https://github.com/OceanNetworksCanada/onc_dts_data/tree/main/notebooks)

The below instructions are for monitoring real-time data coming into Oceannetworks.ca:

## Running the Monitoring Script

### Prerequisites: Installing uv

This project uses `uv` for dependency management and script execution. If you don't have `uv` installed, you'll need to install it first.

**Installation Options:**

- **Standalone installer (Recommended):**
  ```bash
  # On macOS/Linux:
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # On Windows (PowerShell):
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- **Alternative methods:** See the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for other installation options including Homebrew, pip, winget, and more.

### What is uvx?

`uvx` is a tool that comes with `uv` for running Python tools and scripts in isolated environments. It automatically:
- Creates temporary virtual environments
- Installs dependencies as needed
- Runs the specified tool/script
- Cleans up after execution

This ensures your system Python remains clean and prevents dependency conflicts.

### Obtain your ONC API token
A unique Oceans 3.0 API token is required to access ONCs data. To obtain a token, follow the steps below:
1. Register for an Oceans 3.0 account at https://data.oceannetworks.ca/Registration.
2. Log into your account at https://data.oceannetworks.ca by clicking the Log In link.
3. Click the Profile link (top right corner) to access your account profile.
4. Access the Web Services API tab and click Copy Token.
   
If you forget your token, you can always find it again in your Oceans 3.0 account profile.
You can store your token in a .env file in the same directory as ONC_API_TOKEN = ''.

### Running the DTS Monitoring Script

The monitoring script can be executed directly from the GitHub repository without needing to clone or install the package locally:

```bash
uvx --from git+https://github.com/OceanNetworksCanada/onc_dts_data monitor_dts --start-time "2025-07-30T20:33:59.134Z" --log-level DEBUG
```

**Parameter Breakdown:**

- `uvx` - The uv tool runner command
- `--from git+https://github.com/OceanNetworksCanada/onc_dts_data` - Specifies the source location
  - `git+` tells uvx to install from a Git repository
  - The URL points to this project's GitHub repository
  - uvx will clone the repo, install dependencies, and make the `monitor_dts` command available
- `monitor_dts` - The name of the script/command to run (defined in the project's configuration)
- `--start-time "2025-07-30T20:33:59.134Z"` - Sets the monitoring start time
  - Must be in ISO 8601 format with timezone (Z = UTC)
  - Example format: `YYYY-MM-DDTHH:MM:SS.sssZ`
- `--log-level DEBUG` - Sets the logging verbosity level
  - Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
  - `DEBUG` provides the most detailed output for troubleshooting

**Example Usage:**

```bash
# Basic monitoring from current time
uvx --from git+https://github.com/OceanNetworksCanada/onc_dts_data monitor_dts --start-time "2025-01-15T12:00:00.000Z"

# With detailed logging
uvx --from git+https://github.com/OceanNetworksCanada/onc_dts_data monitor_dts --start-time "2025-01-15T12:00:00.000Z" --log-level DEBUG

# With minimal logging
uvx --from git+https://github.com/OceanNetworksCanada/onc_dts_data monitor_dts --start-time "2025-01-15T12:00:00.000Z" --log-level WARNING
```

**Troubleshooting:**

- If you get a "command not found" error, ensure `uv` is installed and in your PATH
- If the script fails to start, check that your start time is in the correct ISO 8601 format
- Use `--log-level DEBUG` to get detailed error information
- Ensure you have an active internet connection for downloading dependencies and accessing the GitHub repository

**Note:** The first run may take longer as uvx downloads and installs all required dependencies. Subsequent runs will be faster due to caching.

For more information about uv and script execution, see the [uv scripts documentation](https://docs.astral.sh/uv/guides/scripts/).


