# Example of SEC Open API Usage

Get Funds information and save to csv file

Code style standard: pycodestyle

## Installation

Check installed python version, make sure you're using Python 3

```bash
python --version
```

Install dependencies

```bash
pip install -r requirements.txt
```

## How it works

- Get API Key from From Environment variable
- A python Script requests unique ID of every fund house available
- Each ID is then used to request all funds of the house to pandas dataframe.
- Convert dataframe to csv

Run the script using

```bash
SEC_OPEN_API_KEY={yourAPIKey} python get_funds_csv.py
```

Happy Scripting~
