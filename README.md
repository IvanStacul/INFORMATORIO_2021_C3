# CHACÚ.py

CHACÚ.py es un juego gratuito, didáctico y de habilidad, donde el jugador debe contestar preguntas sobre conocimientos generales en torno a la Provincia el Chaco.

## Online version

[Chacú.py](https://chacu-py.herokuapp.com/)

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
venv\Scripts\activate.bat
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
python manage.py migrate
python manage.py runserver
```

### Change settings in manage.py file

from

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chacu_py.settings.production')
```

to

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chacu_py.settings.development')
```

## Authors

Informatorio 2021 - Commission 3 - Group 4
