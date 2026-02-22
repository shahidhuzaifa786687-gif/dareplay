# DarePlay

Simple truth-or-dare web app built with Flask.

Run locally:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python game.py
```

## API Endpoints

- `GET /api/question` &nbsp;&nbsp;– retrieve a random truth/dare question (see code for parameters)
- `GET /api/difficulties` &nbsp;&nbsp;– list available difficulty levels
- `GET /api/choices` &nbsp;&nbsp;– list choices for a given difficulty
- `GET /api/health` &nbsp;&nbsp;– simple health check
- `POST /api/players` &nbsp;&nbsp;– send JSON `{"names": ["Alice","Bob",...]}` with 2–4 player names; returns a randomly selected name

To deploy, use a WSGI server such as `gunicorn` or a platform's recommended method.