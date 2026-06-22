sudo apt install python3-virtualenv
virtualenv env_name
source env_name/bin/activate
which python3
pip3 install -r requirements.txt
pip3 install -U pyinstaller
pyinstaller main.spec
dist/modem_tester\ v1.0.0
