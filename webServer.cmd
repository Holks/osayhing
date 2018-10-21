set FLASK_APP=osayhing.py
cd %userprofile%\git\osayhing
call venv\scripts\activate

python -m flask run --host=0.0.0.0
