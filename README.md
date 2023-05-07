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
5. Open a browser and type in _localhost_
