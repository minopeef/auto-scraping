cd ../../
py -m venv .venv
".venv/scripts/pip.exe" install -r requirement/requirements.txt
.venv\scripts\python.exe init_drive.py
pause
