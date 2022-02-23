# P4_Ocr

## Table of contents
* [General info](#general-info)
* [Packages](#packages)
* [Setup Linux](#setup-linux)
* [Setup Windows](#setup-windows)
* [Flake8 report](#flake8-report)

## General info
This project is a chess tournament software 
	
## Packages
Project is created with:
* tinydb: 4.5.2

For html flake8 reports:
* flake8-html: 0.4.1
	
## Setup Linux
To run this project, install python3 : ```sudo apt install python3.8```

Go in the project folder : ```cd /.../P4_Ocr_main```

Create a virtual environment : ```python3 -m venv env```

Activate the virtual environment : ```source env/bin/activate```

To install directly all packages you need : ```python -m pip install -r requirements.txt```

Run this project with : ```python3 main.py```

## Setup Windows
To run this project, write ```python3``` in the cmd to install python3 in microsoft store

Go in the project folder : ```cd \...\P4_Ocr_main```

Create a virtual environment : ```python3 -m venv env```

Activate the virtual environment : ```\Users\...\P4_Ocr_main\env\Scripts\activate.bat```

To install directly all package you need : ```python -m pip install -r requirements.txt```

Run this project with : ```python3 main.py```

## Flake8 report
To create a html report : ```flake8 "file" --format=html --htmldir=flake-report```
