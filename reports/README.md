# Nature Recorder Reporting

This folder contains Jupyter notebooks and supporting files for reporting on wildlife sightings stored in the Nature Recorder SQLite database. This provides more flexible reporting than the built-in reports in the application itself.

The following reports are currently available:

| Notebook | Report Type |
| --- | --- |
| heatmap.ipynb | Heatmap of number of sightings of each species in a category at a location during a specified year | 

## Setting Up the Reporting Environment

The reports have been written and tested using [Visual Studio Code](https://code.visualstudio.com/download) and the Jupyter extension from Microsoft using a Python virtual environment with the requirements listed in requirements.txt installed as the kernel for running the notebooks.

### Set Environment Variables

The following environment variable to be set *before* running code and opening the notebook:

``` bash
export NATURE_RECORDER_DB=/path/to/naturerecorder.db
```

Or, in PowerShell:

```powershell
$env: NATURE_RECORDER_DB = C:\path\to\naturerecorder.db
```

### Build the Virtual Environment

To build the virtual environment, run the following command:

```bash
./make_venv.sh
```

Or, in PowerShell:

```powershell
.\make_venv.bat
```

## Running a Report in Visual Studio Code

- Open the Jupyter notebook for the report of interest
- If using Visual Studio Code, select the Python virtual environment as the kernel for running the notebook
- Review the instructions at the top of the report and make any required changes to e.g. reporting parameters
- Click on "Run All" to run the report and export the results
- Exported results are written to a folder named "exported" within the reports folder
