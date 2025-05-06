#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Check if config.ini exists
if [ ! -f "config.ini" ]; then
    echo "Error: config.ini not found!"
    echo "Please copy config.ini.template to config.ini and update the values."
    exit 1
fi

# Read database configuration from config.ini
DB_NAME=$(grep "^db_name" config.ini | cut -d'=' -f2 | tr -d ' ')
DB_USER=$(grep "^db_user" config.ini | cut -d'=' -f2 | tr -d ' ')
DB_PASSWORD=$(grep "^db_password" config.ini | cut -d'=' -f2 | tr -d ' ')
DB_HOST=$(grep "^db_host" config.ini | cut -d'=' -f2 | tr -d ' ')

# Validate configuration
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_HOST" ]; then
    echo "Error: Missing database configuration in config.ini"
    exit 1
fi

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
echo "Installing system dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv mysql-server nginx python3-dev default-libmysqlclient-dev build-essential pkg-config

# Start and enable MySQL service
echo "Configuring MySQL..."
sudo systemctl start mysql
sudo systemctl enable mysql

# Create application directory
echo "Setting up application directory..."
sudo mkdir -p /var/www/addressbook
sudo chown -R $USER:$USER /var/www/addressbook

# Copy application files
echo "Copying application files..."
cp -r ./* /var/www/addressbook/

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd /var/www/addressbook
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service file
echo "Creating systemd service..."
sudo tee /etc/systemd/system/addressbook.service << EOF
[Unit]
Description=Address Book Flask Application
After=network.target mysql.service

[Service]
User=$USER
WorkingDirectory=/var/www/addressbook
Environment="PATH=/var/www/addressbook/venv/bin"
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
ExecStart=/var/www/addressbook/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/addressbook << EOF
server {
    listen 80;
    server_name itmd504-webapp.ramarajan.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # Logging
    access_log /var/log/nginx/addressbook_access.log;
    error_log /var/log/nginx/addressbook_error.log;

    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    # Static files
    location /static {
        alias /var/www/addressbook/static;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Favicon
    location /favicon.ico {
        alias /var/www/addressbook/static/favicon.ico;
        access_log off;
        log_not_found off;
    }

    # API documentation
    location /api/docs {
        alias /var/www/addressbook/API.md;
        default_type text/markdown;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/addressbook /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Create log directory for Nginx
sudo mkdir -p /var/log/nginx
sudo chown -R www-data:www-data /var/log/nginx

# Test Nginx configuration
sudo nginx -t

# Restart services
echo "Restarting services..."
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl enable addressbook
sudo systemctl restart addressbook

# Verify services are running
echo "Verifying services..."
sudo systemctl status nginx | grep "Active:" | cat
sudo systemctl status addressbook | grep "Active:" | cat

# Clean up sensitive information
unset DB_PASSWORD

echo "Deployment completed successfully!"
echo "The application should now be accessible at http://itmd504-webapp.ramarajan.com"
echo "API documentation is available at http://itmd504-webapp.ramarajan.com/api/docs"
echo "MySQL Database: $DB_NAME"
echo "MySQL User: $DB_USER" 