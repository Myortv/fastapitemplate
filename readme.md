<h1> Start up</h1>

you need running postgres with default configuration.

cloning repository
```
git clone https://github.com/Myortv/fastapitemplate.git
cd fastapitemplate
```
creating fresh virtual envirement
```
python -m venv env
. ./env/bin/activate
```
installing dependencies
```
pip install -r req.txt
# install fastapi plugins
pip install git+https://github.com/Myortv/fastapi-plugins.git
```
starts template
```
clear; uvicorn app.main:app --log-config app/core/log.config --port 8000 --reload
```


<h1> Key files</h1>

Key files contains commands to generate that keys.


