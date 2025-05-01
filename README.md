# Usage

In an empty folder run
```bash
git clone https://github.com/ilia-moroz-ees/enDAQ-testing.git
```

Folder "samples" contains sample data from CanEdge in 00000006\00000001.MF4, **use parseCANedge.py to convert to CSV** <br/> 
bobby_000056.IDE is an output file from enDAQ, **use enDAQtoCSV.py to convert to CSV**

If there is a ModuleNotFoundError when running these scripts, run these lines in order<br/> 
On Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On UNIX:
```bash
python -m venv .venv
source .venv/scripts/activate
pip install -r requirements.txt
```
-----
### `enDAQtoCSV.py`

Converts enDAQ IDE files to CSV format.

Usage:

```bash
python enDAQtoCSV.py <path_to_endeq_file>
```

Example:

```bash
python enDAQtoCSV.py samples\bobby_000056.IDE
```
-----
### `canEdgeTesting.py`

Sends commands to the CANedge using PCAN transmitter

Usage:

```bash
python canEdge_testing.py
```
-----
### `parseCANedge.py`

Converts MF4 files to CSV format. Note: DBC file must be capable of decoding MF4 files <br/> 
Reads all the MF4 files in the specified folder <br/> 
As many DBC files can be specified as needed

```bash
python parseCANedge.py <path_to_folder_containing_MF4_files>  <path_to_dbc_file>
```

Example: (creates a folder with csv files inside samples\00000006 folder)
``` bash
python parseCANedge.py samples\00000006 samples\test_dbc.dbc
```

