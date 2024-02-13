```
sudo service mysql start
```

```
uvicorn main:app --reload
```

```
alembic revision --autogenerate -m "Description"
```

```
alembic upgrade head
```