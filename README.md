# Tier List Maker
You can create your own list. 
## Website
Link : https://tierlistmaker.fly.dev/

## Built With
This project was built using these technologies:
- Python3
- Flask
- Docker

## Getting Started
### Prerequisites
1. Docker
2. Docker Compose

### Installation
1. Clone the repo
```
git clone https://github.com/TaigaVanilla/tier-list-maker.git
```
2. Build images and start containers
```
docker-compose up -d --build
```
3. Open the Flask shell in a running container
```
docker-compose exec web flask shell
```
4. Create tables
```
from models import init; init()
```

### Environment Variables
Create .env file
```
FLASK_APP=app.py
FLASK_ENV=development

POSTGRES_USER=user
POSTGRES_PASSWORD=password

POSTGRES_DB=tierlistmaker
TZ=Asia/Tokyo
POSTGRES_INITDB_ARGS=--encoding=UTF-8
```
