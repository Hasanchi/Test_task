# Test_task
docker-compose up --build
docker-compose exec web alembic upgrade head
docker-compose exec web python -m src.script
