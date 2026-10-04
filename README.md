# Comeiin Works

Comeiin Works is a Django website for browsing laboratory equipment and consumables, exploring supported industries, signing in and submitting quotation requests.

This guide explains how to set up the `master2` branch in Visual Studio Code and run it locally.

## Technology

- Python and Django
- Django REST Framework
- Django Allauth for account and Google sign-in flows
- PostgreSQL in production
- SQLite can be used for local development
- WhiteNoise for static files
- HTML, CSS and JavaScript frontend

## Prerequisites

Install the following before starting:

- [Git](https://git-scm.com/downloads)
- [Python 3.11](https://www.python.org/downloads/) or another compatible Python 3 version
- [Visual Studio Code](https://code.visualstudio.com/)
- The VS Code **Python** extension from Microsoft

Python 3.11 is recommended because the project has a large, pinned dependency list. Using the same Python version across the team reduces installation differences.

Check that Git and Python are available:

```bash
git --version
python3 --version
```

On Windows, the Python command may be `python` instead of `python3`.

## 1. Clone the project

Open a terminal and run:

```bash
git clone https://github.com/Madenet/Comeiin-Dynamic.git
cd Comeiin-Dynamic
git switch master2
```

Confirm that the correct branch is active:

```bash
git branch --show-current
```

The result should be `master2`.

## 2. Open the project in VS Code

From the project folder, run:

```bash
code .
```

Alternatively, open VS Code and select **File → Open Folder**, then choose the `Comeiin-Dynamic` folder.

## 3. Create a virtual environment

A virtual environment keeps this project's Python packages separate from other projects.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

When the environment is active, the terminal prompt normally starts with `(.venv)`.

In VS Code, select the same environment:

1. Open the Command Palette with `Ctrl+Shift+P` or `Cmd+Shift+P`.
2. Select **Python: Select Interpreter**.
3. Choose the interpreter inside `.venv`.

## 4. Install the Python requirements

Upgrade the packaging tools first:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Install all packages listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Use `python -m pip` instead of a standalone `pip` command so the packages are installed into the active virtual environment.

## 5. Create the local environment file

Create a file named `.env` in the project root, beside `manage.py`.

```env
SECRET_KEY=replace-this-with-a-long-random-development-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
DEFAULT_FROM_EMAIL=Comeiin Works <Admin@comeiin.co.za>
CONTACT_RECEIVER_EMAIL=Admin@comeiin.co.za
```

The `.env` file is ignored by Git. Never commit real production passwords, API keys or OAuth secrets.

With `DEBUG=True`, contact and quotation emails are printed in the terminal instead of being sent through the production email account.

### Optional PostgreSQL database

SQLite is the simplest option for local development. To use PostgreSQL instead, create a local database and change `DATABASE_URL`:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/comeiin
```

Replace the username, password and database name with your local PostgreSQL details.

## 6. Prepare the database

Apply the Django migrations:

```bash
python manage.py migrate
```

Create an administrator account if you need access to Django Admin:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter the administrator email and password.

## 7. Check the project

Run Django's configuration check:

```bash
python manage.py check
```

The expected result is:

```text
System check identified no issues (0 silenced).
```

## 8. Run the website locally

Start Django's development server:

```bash
python manage.py runserver
```

Open these addresses in a browser:

- Website: <http://127.0.0.1:8000/>
- Products: <http://127.0.0.1:8000/products/>
- Industries: <http://127.0.0.1:8000/industries/>
- Contact: <http://127.0.0.1:8000/contact/>
- Admin: <http://127.0.0.1:8000/admin/>

Stop the server with `Ctrl+C`.

## Static files

During local development, Django serves assets from the `static/` folder.

Use `static/` when editing CSS, JavaScript and images. The `staticfiles/` folder is generated output and should not be edited manually.

To collect production-style static files locally, run:

```bash
python manage.py collectstatic --noinput
```

If an older design remains visible after frontend changes, clear the browser's site data or unregister the old service worker, then reload the page.

## Google sign-in

Normal email/password accounts can be tested locally after running the migrations.

Google sign-in also requires a Google OAuth client and a Django Allauth `SocialApp` configured for the current Django Site. Ask the project administrator for the approved development credentials and redirect URLs. Do not add production OAuth secrets to the repository.

## Running tests

Run the Django test suite with:

```bash
python manage.py test
```

Before committing a change, also run:

```bash
python manage.py check
git diff --check
```

## Project structure

```text
comeiin/       Django project settings and root URLs
core/          Home, About, Contact, Industries and shared APIs
products/      Product catalogue, product APIs and product pages
quotes/        Quotation models, APIs and email handling
templates/     Django HTML templates
static/        Source CSS, JavaScript, images and PWA files
staticfiles/   Generated static output
manage.py      Django management command entry point
requirements.txt
```

## Working safely with Git

Before starting new work:

```bash
git switch master2
git pull --ff-only origin master2
git switch -c feature/short-description
```

Make and verify the change, then commit it on the feature branch:

```bash
git status
git add path/to/changed-file
git commit -m "Describe the change"
git push -u origin feature/short-description
```

Open a pull request into `master2`. Avoid force-pushing shared branches and avoid committing `.env`, database files, virtual environments or production credentials.

## Troubleshooting

### `No module named django`

Activate `.venv`, select it as the VS Code Python interpreter and reinstall the requirements:

```bash
python -m pip install -r requirements.txt
```

### Database configuration error

Confirm that the `.env` file is beside `manage.py` and contains:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

Then run:

```bash
python manage.py migrate
```

### PowerShell blocks virtual-environment activation

Run this once in the current PowerShell session, then activate `.venv` again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Frontend changes do not appear

1. Confirm that you edited files under `static/`, not `staticfiles/`.
2. Restart the Django server.
3. Perform a hard refresh.
4. Clear the site's service worker and cached storage if necessary.

### Port 8000 is already in use

Run the development server on another port:

```bash
python manage.py runserver 8001
```

Then open <http://127.0.0.1:8001/>.

## Production

The public deployment uses production environment variables and PostgreSQL. Keep those values in the hosting platform rather than in Git. A production deployment should apply migrations and run `collectstatic` before starting the application server.

