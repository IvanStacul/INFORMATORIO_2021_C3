# CHACÚ.py

Repository of the final web project, developed with Django, for the course given by the Informatorio.

## Usage

### Clone the repo

#### HTTPS

``` shell
git clone https://github.com/IvanStacul/INFORMATORIO_2021_C3.git
cd INFORMATORIO_2021_C3
```

#### SSH

``` shell
git clone git@github.com:IvanStacul/INFORMATORIO_2021_C3.git
cd INFORMATORIO_2021_C3
```

### Create virtualenv and install requirements

On windows PowerShell

```shell
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

On windows cmd

```shell
py -m venv venv
venv/Scripts/activate.bat
pip install -r requirements.txt
```

On linux

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run aplication

```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Authors

Informatorio 2021 - Commission 3 - Group 4
