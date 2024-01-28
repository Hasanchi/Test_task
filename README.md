# Test_task
1. Запуск контейнеров

```docker-compose up --build```

2. Запуск миграций
```docker-compose exec web alembic upgrade head```

3. Запуск скрипта для наполнения бд

```docker-compose exec web python -m src.script```

После выполнения скрипта в бд появится 4 пользователя:
1. Meneger
2. Developer
3. TeamLeader
4. TestEngineer
Для всех этих пользователей пароль: testpass

