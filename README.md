# CSV-to-Postgres

Batch-import every CSV in a folder into PostgreSQL using a Jupyter notebook and a small Python helper module.

Adapted from [StrataScratch's csv_to_db_automation](https://github.com/Strata-Scratch/csv_to_db_automation) and extended for Electronic Medical Record (EMR) export quirks — especially encoding issues common in clinical data extracts.

## Features

- Import all CSVs from a directory into PostgreSQL
- Encoding-tolerant reads for messy EMR exports
- Notebook-driven workflow for inspection before load
- Helper functions in `csv_import_functions.py`

## Requirements

- Python 3.x
- PostgreSQL
- `pandas`, `psycopg2` (or compatible Postgres driver)

## Usage

1. Place CSV files in the target folder.
2. Configure your database connection in the notebook / script.
3. Open `main.ipynb` (or `10e11 Import to SQL.ipynb`) and run the cells, **or** call the helpers from `csv_import_functions.py`.

## Notes

- Some EMR exports require `errors='ignore'` during decode. That can drop invalid characters — review loaded data when fidelity matters.
- Credit: Nate / StrataScratch tutorials on Pandas and NumPy are excellent references for this style of workflow.

## License

No license file is currently published in this repository. Contact the author if you need reuse terms.
