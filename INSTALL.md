# Installation Guide for Linux

## Development environment

### Python dependencies

Requirements : Python ^3.7

Create a virtual environment :

```bash
python -m venv venv
```

Activate the virtual environment :

```bash
source venv/bin/activate # Linux/MacOS
venv\Scripts\activate  # Windows
```

Install the python dependencies :

```bash
pip install -r requirements.txt
```

If you want to install the development dependencies, run :

```bash
pip install -r requirements-dev.txt
```

You should do so if you intend to contribute to the project or want to create and populate your own database.

## Configuration

Some configurations are necessary to run the application.
Create a .env file at the root of the project using the `.env.example` file as a template.

```bash
cp .env.example .env # Linux/MacOS
copy .env.example .env # Windows
```

Edit the `.env` file to match your configuration.

## Start the application

Start the application from the root of the project and from within the virtual environment :

```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
