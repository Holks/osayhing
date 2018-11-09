set FLASK_APP=osayhing.py
F:
cd git\osayhing
call venv\scripts\activate

python -m flask run
REM --host=0.0.0.0


REM flask db init
REM flask db migrate -m "shareholders table"
REM flask db upgrade