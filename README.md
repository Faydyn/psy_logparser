# psy_logparser

## How to use?

### Option 1: Download files and install Python
https://www.python.org/downloads/release/python-397/
Note that Python 3.9.7 cannot be used on Windows 7 or earlier.
Windows installer (32-bit)
Windows installer (64-bit) (recommended)
Run as admin
TICK ADD TO PATH
INSTALL NOW
DISABLE PATH LENGTH LIMIT (IF NOT DONE AND POPS UP)
CLOSE
REMOVE INSTALLER

Press Windows button + S and type "cmd", then open Command Prompt (or PowerShell)
Inside the Terminal type "python" and see if 
    a) installation worked and
    b) if the version is "Python 3.9.7"
Type "2 + 2" and see if everything works (should print out 4)
Type "quit()" to exit python

Go to Github and down Zip of the project 
Unpack it where u want (Copy the path)

Go back to command prompt and type "cd C:\...\psy_logparser"
enter the full absolute path (above is just an example, can also be run on D:, etc.)
type "pip install -r requirements.txt" and "pip3 install -r requirements.txt" 
Pip is python automatic package manager 
type " python -c "import numpy; print(numpy.__version__)" " == 1.21.2
type " python -c "import pandas; print(pandas.__version__)" " == 1.3.2

Open constants.json and change path for data in and out
IMPORTANT USE DOUBLE \\ INSTEAD OF SINGLE \ AS SEPARATOR FOR DIRECTORIES in constants.json
Save and Exit constants.json 

Go back to shell/prompt/terminal and type "python -m main"

IF You want to change to mode that is loaded in constants OR want to load an 
entirely other constant file that is also json: 
THIS CAN BE CHANGED WITH THE FIRST TWO VARIABLES OF constants.py (!PY!)
BE Careful to spell the mode correctly. 
IMPORTANT USE DOUBLE \\ INSTEAD OF SINGLE \ AS SEPARATOR FOR DIRECTORIES in constants.py

### Option 2: Run code in Jupyter Notebook 

