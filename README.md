# General Exchanges

A Python-first Django marketplace starter for raw materials like wood, steel, bricks, cement, gravel, plywood, and construction supplies.

This is the first working version:

- Buyer can browse products
- Buyer can check out products
- Buyer can search/filter products
- Seller can register
- Seller can add products
- Seller can edit/delete their own products
- Seller dashboard shows their listings
- Django admin can approve sellers
- No Stripe, cart, payouts, or shipping APIs yet

## Tech Stack

- Python
- Django
- SQLite for local development
- Django Templates
- Simple CSS

## How to Run

### 1. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```



### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create admin user

```bash
python manage.py createsuperuser
```

### 5. Run server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```


## Next Milestones



1. Add manual tracking number
2. Add Stripe test payment
3. Add Stripe Connect seller payouts
4. Add seller verification
5. Add Texas-only delivery filters
