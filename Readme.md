# Gift Registry

A simple gift registry web service. Thematically designed for a baby shower, but easily adaptable for any purpose.

## Features

* Built with a Django backend and Tailwind frontend
* Manage items with the Django admin interface
* Links to items automatically fetch images and descriptions using opengraph
* One-click to claim/mark items as bought
* Set limits on number of items and moves them down the list as they are claimed
* Prompts users for an email address to send them a link that allows them to return and manage items
* Webhook confirms email sent
* Dockerfiles for asset complilation and deployment
    * Main app served with gunicorn
    * Static files served with nginx
    * Traefik handles TLS and incoming requests

## Developing

* Install pip requirements `pip install -r requirements.txt`
* Install `node` and `npm` for Tailwind
* Perform database migration `python manage.py migrate --settings=registry.settings.dev `
* Launch Tailwind JIT compilier `python manage.py tailwind --settings=registry.settings.dev start`
* Launch Django development server `python manage.py runserver --settings=registry.settings.dev`

## Deploying

* Adjust production configuration in `registry/settings/prod.py`
* Adjust Traefik configuration in `docker-compose.yml`
* Build assets and app container `docker-compose build`
* Perform database migration `python manage.py migrate --settings=registry.settings.prod`
* Create admin account `python manage.py createsuperuser --settings=registry.settings.prod`
* Launch service directly `docker-compose up` or push containers to server and deploy with Docker-swarm

## Screenshots

### Main Page
<img src="https://raw.githubusercontent.com/Cameron-D/gift-registry/main/screenshots/MainPage.png" width="400" />

### Claimed Items
<img src="https://raw.githubusercontent.com/Cameron-D/gift-registry/main/screenshots/YourItems.png" width="400" />

### Email Address Field
<img src="https://raw.githubusercontent.com/Cameron-D/gift-registry/main/screenshots/EmailAddress.png" width="400" />

### All Item States
<img src="https://raw.githubusercontent.com/Cameron-D/gift-registry/main/screenshots/ItemStates.png" width="400" />