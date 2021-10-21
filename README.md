# psy_logparser

Parses data from .txt-Files to a certain format and saves them as .csv-Files.

Has multiple parts that can be chosen individually or chained together to produce a final, accumulated result.

## What do you need to use the parser?

### Option 1: Jupyter Notebook (Browser)

Open this [Jupyter Notebook on Binder](https://mybinder.org/v2/gh/Faydyn/psy_logparser.git/master).

__DISCLAIMER__: This option is more __restricted__ when it comes to customization.

### Option 2: Python 3 (Local)
The following is a quick guide of a Python Installation primarily for Windows, with some comments for Unix-based Operating Systems.

If you already installed `Python 3.9.7` or higher, you can skip this part. 

#### 1. Python Installation Guide 

##### __WINDOWS__
__WARNING__: `Python 3.9.7` cannot be used on Windows 7 or earlier.

######  Download and run Python 3
1. Download `Python 3.9.7` from the [Python Website](https://www.python.org/downloads/release/python-397/). Choose either __Windows installer (32-bit)__ or __Windows installer (64-bit, recommended)__.
2. Run `python-3.9.7.exe` as __Administrator__.
3. Check "__Add Python 3.9 to PATH__". (Optional, but recommended)
4. Choose "__Install Now__".
5. Wait for installation to complete.
6. When done, __Disable Path Length Limit__. (If not already done - thus does not show up in picture).
7. Close the Installer and remove `python-3.9.7.exe`. 

###### Testing Python 3
1. Press __Win+S__ to search for "cmd", choose __Command Prompt__ (or PowerShell).
2. Inside __Command Prompt__ type: `python`. 
3. Check, if it installed correctly and prints out the correct version number (__3.9.7__).
4. Do another simple check, like `2 + 2`, which check result in `4` without any errors.
5. Type `quit()` to exit Python.

##### __OS X__
Download Anaconda via Homebrew and simply set up an Environment with Python 3.9.7.

You might need to use `python3` in __Terminal__.
Contact me, when issues arise during this. 

##### __LINUX__
I guess, you know how to do this.


#### 2. Github Guide 
Now you need to download the files from this repository. They can be download as `zip`, or you can __clone__ them. 

##### __DOWNLOAD ZIP__
Click the green "__Code__" at the top of this page and choose "__Download ZIP__".
Move the files where you like - as long as you got the permissions to access the chosen directory.

##### __GIT CLONE__ 
Choose a directory inside a __Terminal__ (with `cd`, see below) and type `git clone https://github.com/Faydyn/psy_logparser.git`.


#### 3. pip Guide 

###### Using Command-Line to install dependencies

1. Open up __Command Prompt__,__PowerShell__ or a __Terminal__ (Unix) of your choice.
2. Copy/Type the path of the downloaded/cloned repository (this is `<PATH>`) to the Prompt/Shell: `cd <PATH>`
3. Type `pip install -r requirements.txt` and `pip3 install -r requirements.txt`, but the latter should suffice in most cases.

###### Testing dependencies

1. Type `python -c "import numpy; print(numpy.__version__)"`. That should be: `1.21.2`. 
2. Type `python -c "import pandas; print(pandas.__version__)"`. That should be: `1.3.2`. 


Open constants.json and change path for data in and out
IMPORTANT USE DOUBLE \\ INSTEAD OF SINGLE \ AS SEPARATOR FOR DIRECTORIES in constants.json
Save and Exit constants.json 

Go back to shell/prompt/terminal and type "python -m main"

IF You want to change to mode that is loaded in constants OR want to load an 
entirely other constant file that is also json: 
THIS CAN BE CHANGED WITH THE FIRST TWO VARIABLES OF constants.py (!PY!)
BE Careful to spell the mode correctly. 
IMPORTANT USE DOUBLE \\ INSTEAD OF SINGLE \ AS SEPARATOR FOR DIRECTORIES in constants.py





