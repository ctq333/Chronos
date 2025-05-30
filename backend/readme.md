# Chronos Backend

## Development

### Create Python Virtual Environment

Virtual environments are created by executing the venv module:

```
python -m venv .venv
```

### Activate the Python virtual environment:

Before you work on your project, activate the corresponding environment:

macOS/Linux

```
$ . .venv/bin/activate
```

Windows

```
> .venv\Scripts\activate
```
### Install Depedencies
```
pip3 install -r requirements.txt
```
### Config .env file

Create `.env` text file in the backend root folder and set the following environment variables in the file:

```
GENAI_API_KEY=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_HOST=
MYSQL_PORT=3306
MYSQL_DB=
MYSQL_CHARSET=utf8mb4
ALLOWED_CORS_ORIGINS=https://domain1.com,https://domain2.com,...
```

### Run Backend
```
flask run
```
