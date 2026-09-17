<div align="center">

<img
  src="https://raw.githubusercontent.com/JuliaKeller13/Coderr_frontend/main/assets/logo/logo_coderr.svg"
  alt="Coderr Logo"
  width="180"
/>

# Coderr Backend

REST API for a service marketplace built with Django and Django REST Framework.

<p>
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-6.1.1-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.18.1-A30000" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/Coverage-100%25-success" alt="Coverage">
</p>

</div>

## About

Coderr is a service marketplace where customers can browse offers, place orders and review business users.

Business users can create service offers and manage incoming orders.

This repository contains my backend implementation created as part of the Developer Akademie Backend curriculum. The frontend was provided separately.

## Quickstart / Setup

### Prerequisites

- Python 3.14
- Git

### 1. Clone the repository

```bash
git clone https://github.com/JuliaKeller13/coderr_backend.git
cd coderr_backend
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create the environment file

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create demo data

```bash
python manage.py seed_demo_data
```

### 7. Start the server

```bash
python manage.py runserver
```

The API is available at:

```text
http://127.0.0.1:8000/api/
```

## Usage

The API uses Django REST Framework Token Authentication.

After login or registration, protected requests require:

```text
Authorization: Token <your-token>
```

Main API resources:

| Resource | Endpoint |
| --- | --- |
| Registration | `/api/registration/` |
| Login | `/api/login/` |
| Profiles | `/api/profile/<user_id>/` |
| Offers | `/api/offers/` |
| Orders | `/api/orders/` |
| Reviews | `/api/reviews/` |
| Base information | `/api/base-info/` |

Demo accounts can be created with:

```bash
python manage.py seed_demo_data
```

Customer:

```text
Username: andrey
Password: asdasd
```

Business:

```text
Username: kevin
Password: asdasd24
```

## Project Structure

```text
coderr_backend/
├── core/
├── base_info_app/
│   ├── api/
│   └── tests/
├── users_app/
│   ├── api/
│   └── tests/
├── offers_app/
│   ├── api/
│   └── tests/
├── orders_app/
│   ├── api/
│   └── tests/
├── reviews_app/
│   ├── api/
│   └── tests/
├── manage.py
├── requirements.txt
└── README.md
```

## Tests

Run all tests:

```bash
python manage.py test --settings=core.settings_test
```

For faster repeated test runs:

```bash
python manage.py test --keepdb --settings=core.settings_test
```

Run test coverage:

```bash
python -m coverage erase
python -m coverage run manage.py test --settings=core.settings_test
python -m coverage report -m
```

Current test coverage: **100%**

## Notes

- The SQLite database is not committed to the repository.
- Environment variables are stored in `.env`.
- Uploaded media files are excluded from version control.
- The frontend is maintained in a separate repository.

Frontend repository:

https://github.com/JuliaKeller13/Coderr_frontend

## Contributing

This project was created as an educational portfolio project. Contributions are currently not actively requested.

## License

No license has been specified for this project.