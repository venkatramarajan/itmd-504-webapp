# Address Book Web Application

A web-based address book application built with Flask, MySQL, and Bootstrap.

## Features

- Contact management (add, edit, delete)
- Search and filter contacts
- Responsive design
- RESTful API
- MySQL database backend

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- Nginx (for production)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd addressbook
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
   - Create a MySQL database
   - Create a MySQL user with appropriate permissions
   - Copy `config.ini.template` to `config.ini`
   - Update the database configuration in `config.ini`

5. Initialize the database:
```bash
flask db upgrade
```

## Configuration

1. Copy the configuration template:
```bash
cp config.ini.template config.ini
```

2. Edit `config.ini` with your database settings:
```ini
[database]
db_name = your_database_name
db_user = your_database_user
db_password = your_database_password
db_host = your_database_host
```

## Security Notes

- Never commit `config.ini` to version control
- Keep your database credentials secure
- Use strong passwords
- Regularly update dependencies
- Use HTTPS in production

## Development

Run the development server:
```bash
flask run
```

## Production Deployment

Use the provided deployment script:
```bash
./deploy.sh
```

## API Documentation

The API documentation is available at `/api/docs` when the application is running.

## License

[Your License Here] 