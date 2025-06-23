# Safi Green Backend setup
This repository contains the backend code for Safi Greens, built using Django. The backend is responsible for managing user accounts, product listings, orders, payments, and all business logic necessary for running a modern online grocery store.
## Features
- **User Authentication**: Secure registration, login, and password management for customers and admins.
- **Product Management**: CRUD operations for grocery products, categories, and inventory tracking.
- **Order Processing**: Customers can place orders, view order history, and track order status.
- **Cart Functionality**: Add, remove, and manage items in a shopping cart.
- **Payment Integration**: Support for various payment methods (can be customized based on requirements).
- **Admin Dashboard**: Manage products, view orders, update inventory, and analyze sales.
- **API Endpoints**: RESTful APIs for frontend or mobile app consumption.

## Tech Stack
- **Backend Framework**: Django (Python)
- **Database**: PostgreSQL
- **API**: Django REST Framework
## Getting Started
### Prerequisite
- Python 3.9+
- PostgreSQL (or SQLite for local development)
- pip (Python package manager)
## Installation
1. Clone the repository
   ```
   git clone git@github.com:akirachix/big-minds-backend.git
   cd big-minds-backend
   ```
2. Create Virtual Environment
   ```
   uv venv venv
   source venv/bin/activate
   ```
3. Install Dependencies
   ```
   uv pip install -r requirements.txt
   ```
4. Create Superuser
   ```
   python manage.py createsuperuser
   ```
5. Start the Development Server
   ```
   python manage.py runserver
   ```
## Big Minds members 
| Full Names               | 
|--------------------|
| Hewan Mehari       |
| Kevine Umutoni     |
| Tirsit Berihu      | 
| Rigbe Weleslasie   |
| Fana Bezabih       |
| Nebyat Hailu       |

