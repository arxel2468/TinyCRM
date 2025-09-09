# TinyCRM API

Welcome to the TinyCRM API — a powerful, secure, and flexible Customer Relationship Management backend designed to streamline your business operations.

## Live Demo

- **API Base URL:** [https://tinycrm-wxwb.onrender.com](https://tinycrm-wxwb.onrender.com)

## API Documentation

- **Documentation Endpoint:** `/api/docs`  
  Explore the interactive API docs, request samples, and detailed endpoint descriptions.

## Authentication

- **JWT Authentication:**  
  Obtain a token via the `/api/token` endpoint with your credentials.  
  Use the token in the `Authorization` header as `Bearer <token>` for authenticated requests.

### Sample Authentication Request

```bash
POST /api/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

## Features

- **JWT Authentication:** Secure, token-based authentication mechanism.
- **User Data Isolation:** Ensures users can only access their own data.
- **Filtering, Pagination, & Ordering:** Efficiently retrieve and organize large datasets.
- **Companies & Deals Management:** Core modules to manage customer info and sales pipelines.

## Tech Stack & Design Decisions

- Built with Django Rest Framework (DRF) for rapid API development.
- Utilizes `drf-spectacular` for OpenAPI schema and Swagger UI.
- Implements JWT for stateless, secure user authentication.
- Emphasizes data isolation for multi-user environments.
- Supports filters, pagination, and ordering for scalable data handling.

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/arxel2468/TinyCRM.git
   cd tinycrm
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser (optional for admin access):
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Usage

- Access the API at: [https://tinycrm-wxwb.onrender.com](https://tinycrm-wxwb.onrender.com)
- Explore the docs at: `https://tinycrm-wxwb.onrender.com/api/docs` (usually `/api/docs`)

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
