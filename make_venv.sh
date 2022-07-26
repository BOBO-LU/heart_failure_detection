python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install setuptools==47.1.1
pip3 install wheel
pip3 install -r requirements.txt

export PROJECT_PROFILE="`hostname`_$USER"
export PROJECT_LOCATION="`pwd`"

python3 ./src/config/env_manager.py