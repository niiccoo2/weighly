# Weighly

Weighly is a service to weigh things, it was originally meant for food, but it works for anything really.

Weighly is in a very early version right now, so most NEW feautres will not be in issues yet, and drastic changes many happen at any time.

## How to run

If someone wants to make this smoother, be my guest, but we are probably going to be scrapping the python backend for suprabase if it can do what wee need.

First clone the repo.
```shell
git clone https://github.com/niiccoo2/weighly
```

Then open the server code on one screen and app on other. To start the backend, run this from server directory.
```shell
uvicorn main:app --reload
```

Then run the python file for the app.
```shell
python3 main.py
# -- OR --
python3 ./app/main.py
```
