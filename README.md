﻿# Project Name
<b>url-shortener<b>

## Description

url-shortener

The URL Shortener is a web application built using Python with the Django framework. It provides users with the ability to shorten long URLs, making them more convenient to share. The application includes features such as user authentication, URL management, basic analytics, and a clean user interface

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.11.5
- Redis
- Nginx
- Gunicorn

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mddas2/url-shortener.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd yourproject
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install and configure Redis:**

    - On Ubuntu:

        ```bash
        sudo apt-get update
        sudo apt-get install redis-server
        ```
        please setup redis server password
    - On other systems, follow the appropriate installation instructions for cache from the [realpython](https://pypi.org/project/channels-redis/).

## Configuration

1. **Update your Django settings for production in `settings.py`:**

    ```python
    # settings.py

    DEBUG = False

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://redis_ip/1','LOCATION':# 'redis://:redis-password@redis_ip:6379/1',  
            'KEY_PREFIX': 'urlshort',
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'MASTER_NAME': 'mymaster',
            }
        }
    }
    ```

    Replace `your-redis-password` with the actual password you have set for your Redis server. If there is no password, remove `:your-redis-password` from the `LOCATION` URL.

2. **Configure your database, Redis, and other settings as needed.**

## Websocket

1. **Update your Django settings for production in `settings.py`:**

    ```python
    # settings.py

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("redis_ip/0", 6379)], #"hosts": [("redis://:redis-password@redis_ip:6379/0",)],
            },
        },
    }
    ```

    Replace `redis-password` with the actual password you have set for your Redis server. If there is no password, remove `:redis-password` from the `LOCATION` URL.

2. **Configure your database, Redis, and other settings as needed.**

## Deployment

Run the development server:

```bash
python manage.py runserver

## Deployment

# Install Gunicorn (if not installed)
pip install gunicorn

# Run Gunicorn to serve your Django application ,where asgi is file inside setting.py
gunicorn yourproject.asgi:application # please test asgi, and make sure websocket is running

# Install Nginx (if not installed)
sudo apt-get install nginx

# Create an Nginx configuration file, for example, yourproject_nginx.conf
# Add the following content and update placeholders with your actual values
sudo nano /etc/nginx/sites-available/yourproject_nginx.conf

# yourproject_nginx.conf
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/yourproject;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}

# Create a symbolic link to enable the Nginx site
sudo ln -s /etc/nginx/sites-available/yourproject_nginx.conf /etc/nginx/sites-enabled/

# Restart Nginx to apply changess
sudo systemctl restart nginx

## License
This project is licensed under the MIT License.
   ```
