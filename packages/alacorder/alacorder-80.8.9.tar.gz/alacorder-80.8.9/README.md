```
    ___    __                          __         
   /   |  / /___  _________  _________/ /__  _____
  / /| | / / __ `/ ___/ __ \/ ___/ __  / _ \/ ___/
 / ___ |/ / /_/ / /__/ /_/ / /  / /_/ /  __/ /    
/_/  |_/_/\__,_/\___/\____/_/   \__,_/\___/_/     
                                                  
```
# **Alacorder**
### Alacorder collects and processes case detail PDFs into data tables suitable for research purposes.

<sup>[GitHub](https://github.com/sbrobson959/alacorder)  | [PyPI](https://pypi.org/project/alacorder/)     | [Report an issue](mailto:sbrobson@crimson.ua.edu)
</sup>

## **Installation**

**If your device can run Python 3.9+, it supports Alacorder. Download a prebuilt executable from GitHub to use the graphical user interface, or use `pip` to install the command line interface, graphical interface, and Python module `alac`.**

* Install [Anaconda Distribution](https://www.anaconda.com/products/distribution) to install the latest Python (not necessary for prebuilt executable). 
* Once your Anaconda environment is configured, open a terminal from Anaconda Navigator and enter `pip install alacorder` to install.
* To start the graphical interface, enter `python -m alacorder start`.
* Enter `python -m alacorder` to use the command line interface.
* To use the `alac` module, use the import statement `from alacorder import alac`.

# Getting Started with Alacorder

#### **Alacorder can be used without writing any code, and exports to common formats like Excel (`.xls`, `.xlsx`), Apache Parquet (`.parquet`), CSV (`.csv`), and JSON (`.json`).**

## Utilize the command line interface

Create data tables with a row per case using the `multi`, `cases`, `fees`, `charges`, `financial-history`, `settings`, `witnesses`, `attorneys`, `case-action-summary`, and `images` tools. Or create a `pair` template and match names to AIS numbers to summarize voting rights status. 

```
Usage: python -m alacorder [OPTIONS] COMMAND [ARGS]...

  ALACORDER collects and processes case detail PDFs into data tables suitable
  for research purposes.

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  adoc-crawl           Retrieve current inmates list from ADOC
  adoc-fetch           Retrieve records from ADOC Inmate Search
  append               Append one case text archive to another
  archive              Create full text archive from case PDFs
  attorneys            Create and export attorneys table
  case-action-summary  Create and export case action summaries
  cases                Create and export case information table
  charges              Create and export charges table
  fees                 Create and export fees table
  fetch                Fetch cases from Alacourt.com by party search
  fetch-cn             Fetch cases from Alacourt.com by case number
  financial-history    Create and export financial history table
  images               Create and export images table
  missing              Identify cases missing in archive from adoc-fetch results
  multi                Export all data tables to .xls/.xlsx
  pair                 Create blank AIS / unique pairing template
  rename               Rename cases in input directory to case numbers
  sentences            Create and export sentences table
  settings             Create and export settings table
  start                Launch graphical user interface
  vrr-pairs            Create voting rights summary from input cases and pairs
  witnesses            Create and export witnesses table
```

## Fetch cases in bulk from Alacourt.com 

Take a spreadsheet of names and/or other search parameters and download case PDFs from Alacourt in bulk. Download thousands of PDFs in just hours by leaving your computer unattended. (Google Chrome is required to use the `fetch` feature.)

```
Usage: python -m alacorder fetch [OPTIONS]

  Fetch cases from Alacourt.com by party search

Options:
  -in, --input-path PATH      Path to query table/spreadsheet (.xls, .xlsx)
                              [required]
  -out, --output-path PATH    Desired PDF output directory  [required]
  -c, --customer-id TEXT      Customer ID on Alacourt.com  [required]
  -u, --user-id TEXT          User ID on Alacourt.com  [required]
  -p, --password TEXT         Password on Alacourt.com  [required]
  -criminal, --criminal-only  Only search criminal cases
  -n, --no-mark               Do not update query template after completion
  --debug                     Print detailed runtime information to console
  -h, --help                  Show this message and exit.
```
```
Usage: python -m alacorder fetch-cn [OPTIONS]

  Fetch cases from Alacourt.com by case number

Options:
  -in, --input-path PATH    Query spreadsheet with CaseNo or CaseNumber column
                            [required]
  -out, --output-path PATH  Directory to download PDFs to  [required]
  -c, --customer-id TEXT    Customer ID on Alacourt.com  [required]
  -u, --user-id TEXT        User ID on Alacourt.com  [required]
  -p, --password TEXT       Password on Alacourt.com  [required]
  -h, --help                Show this message and exit.
```

## **Work with case data in Python**


Out of the box, Alacorder exports to `.xlsx`, `.xls`, `.csv`, `.json`, and `.parquet`. But you can use `polars` and other python libraries to create your own data collection workflows and customize Alacorder exports. 


```python
from alacorder import alac
import polars as pl

queue = alac.get_paths("/Users/crimson/Desktop/Tutwiler/") # -> [str]

rows = []

for i, path in enumerate(queue):
    text = alac.extract_text(path)
    cnum = alac.getCaseNumber(text)
    cty = alac.getCounty(text)
    tbal = alac.getTotalBalance(text)
    ptr = alac.getPaymentToRestore(text) # i.e. voting rights
    rows += [[cnum, cty, tbal, ptr]]

cases = pl.DataFrame(rows)

cases.write_excel("/Users/crimson/Desktop/Tutwiler/summary.xlsx")

```

## Extend Alacorder with `polars` and other tools

Alacorder runs on [`polars`](https://github.com/pola-rs/polars), a dataframes library you can use to work with and analyze tabular data. `polars` can read from and write to all major data storage formats. It can connect to a wide variety of services to provide for easy import and export.

```python
import polars as pl
contents = pl.read_json("/path/to/archive.json")
```

If you would like to visualize data without exporting to Excel or another format, create a `jupyter notebook` and install tools like `matplotlib`, `tabulate`, and `itables` to get started. [Jupyter Notebook](https://docs.jupyter.org/en/latest/start/index.html) is a Python project you can use to create interactive notebooks for data analysis and other purposes. It can be installed using `pip install jupyter` or `pip3 install jupyter` and launched using `jupyter notebook`. Your device may already be equipped to view `.ipynb` notebooks. 

## **Resources**
* [`polars` user guide](https://pola-rs.github.io/polars-book/user-guide/index.html)
* [regex cheat sheet](https://www.rexegg.com/regex-quickstart.html)
* [Anaconda (tutorials on python data analysis)](https://www.anaconda.com/open-source)
* [The Python Tutorial](https://docs.python.org/3/tutorial/)
* [Jupyter Notebook introduction](https://realpython.com/jupyter-notebook-introduction/)
