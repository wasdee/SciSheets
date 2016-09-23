{
  "SciSheets_Class": "<class 'scisheets.ui.dt_table.DTTable'>",
  "_columns": [
    {
      "SciSheets_Class": "<class 'scisheets.core.column.Column'>",
      "_asis": true,
      "_cells": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
      ],
      "_formula": null,
      "_name": "row"
    },
    {
      "SciSheets_Class": "<class 'scisheets.core.column.Column'>",
      "_asis": false,
      "_cells": [
        ".",
        "",
        "nan",
        "nan",
        "nan",
        "nan"
      ],
      "_formula": null,
      "_name": "Path"
    },
    {
      "SciSheets_Class": "<class 'scisheets.core.column.Column'>",
      "_asis": false,
      "_cells": [
        "Glu.csv",
        "LL-DAP.csv",
        "THDPA.csv",
        "scisheets_log.csv",
        null,
        null
      ],
      "_formula": null,
      "_name": "CSVFiles"
    },
    {
      "SciSheets_Class": "<class 'scisheets.core.column.Column'>",
      "_asis": false,
      "_cells": [
        "THDPA.csv",
        "nan",
        "nan",
        "nan",
        "nan",
        "nan"
      ],
      "_formula": null,
      "_name": "InputFile"
    },
    {
      "SciSheets_Class": "<class 'scisheets.core.column.Column'>",
      "_asis": false,
      "_cells": [
        0.01,
        0.05,
        0.12,
        0.2,
        0.5,
        1.0
      ],
      "_formula": null,
      "_name": "S"
    },
    {
      "SciSheets_Class": "<class 'scisheets.core.column.Column'>",
      "_asis": false,
      "_cells": [
        0.11,
        0.19,
        0.21,
        0.22,
        0.21,
        0.24
      ],
      "_formula": null,
      "_name": "V"
    }
  ],
  "_epilogue_formula": "",
  "_filepath": "/home/ubuntu/SciSheets/mysite/user/guest/tables/csv_explorer.sci",
  "_hidden_columns": [],
  "_is_evaluate_formulas": true,
  "_name": "CSVExplorer",
  "_prologue_formula": "# Prologue\nimport numpy as np\nfrom os import listdir\nfrom os.path import isfile, join\n\npath = Path[0]\nCSVFiles = [f for f in listdir(path) if f[-4:] == '.csv']\nCSVFiles.sort()\n\nnames = s.getColumnNames()\npath = param(s, 'Path')\n# Delete old columns\nfor name in names:\n  if not name in ['row', 'InputFile', 'CSVFiles', 'Path']:\n    s.deleteColumn(name)\n# Get the file to process\n# Check for a missing file\nif len(InputFile) == 0:\n  if not this_file in CSVFiles:\n    InputFile = [\"***File not found\"]\nelse:\n  this_file = InputFile[0]\n  full_file = join(path, this_file)\n  new_columns = importCSV(s, full_file)"
}