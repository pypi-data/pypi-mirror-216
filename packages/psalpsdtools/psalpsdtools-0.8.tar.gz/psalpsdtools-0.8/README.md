# psalpsdtools
![LPSD Logo](LPSD%20Logo.png =100x100)

_psalpsdtools_ was developed for the processing of PSA’s Livestock and Poultry Statistics Division.

# Features

Some of the features include:

####  Electronic Data Review Worksheet (EDRW)
- Looking-up and copying of values from the Supply-Disposition file
- Pasting copied values to the EDRW output file
- Creating output files by province, based on user specified inputs including:
	- region
	- commodity
	- year

# Requirements

Python 3.8 or later with all [requirements.txt](https://github.com/tondiaz/psalpsdtools/blob/main/docs/requirements.txt) dependencies installed. To install run:

```bash
pip install psalpsdtools
```
# Usage
```bash
from psalpsdtools import Edrw

# Specify Region

regName = “Caraga”

# Specify quarter, this used in identifying which worksheet to paste the copied values from the S-D file..

qtr = “Q1”

# Specify folder location of Sources and Final files, the S-D file should also be found here.

baseFolder = “D:/EDRW/Q1”

# Specify S-D filename
# IMPORTANT! Only .xlsm or .xlsx extensions are accepted

sdFile = ‘SD Q1 2023.xlsm’

# Commodity code i.e. 08=chicken, 09=duck, etc.

commcode = ‘08’

# Year

yr = ‘23’

# Call an instance of the Edrw package

myedrw = Edrw()

# Run update_sources with the parameters

myedrw.update_sources(regName,qtr,baseFolder,sdFile,commcode,yr)
```

# Contribute

Issue Tracker: github.com/psalpsdtools/psalpsdtools/issues

Source Code: github.com/psalpsdtools/psalpsdtools

# Support

If you are having issues, please let us know. We have a mailing list located at: a.diaziii@psa.gov.ph

# License

The project is licensed under the MIT license.