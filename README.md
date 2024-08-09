## Introduction

A toy backend implemented in `litestar` that has basic login, registration and authorisation with google oauth. Also provides a basic API to write event to google calendar. Note that there is no database here - the file itself is already 300 lines, I don't want to make it longer. 

## Setup 

Install dependencies:

```bash
pdm install
```
Note that the first two steps are also the first two steps in [here](https://developers.google.com/identity/protocols/oauth2).
- Install Calendar in your google cloud project (Dashboard > APIs & Service > Library). 
- Then create a Web client OAuth2.0 credential (Dashboard > APIs & Services > Credentials). 
- For simplicity, set `Authorized JavaScript origins` to `http://localhost:8080` and `Authorized redirect URIs` to `http://localhost:8080/oauth2callback`. 
- Save the creds json file to `.creds/server_secret.json`

![OAuth Screen](doc/OAuthScreen.png)

## How to run 

```python
pdm run litestar --app src.app:app run --port 8080 --reload --debug
```

