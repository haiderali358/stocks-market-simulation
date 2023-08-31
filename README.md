# Stock Marketing Stimulation Project:
## Create virtual Enviroment
<pre>
python3 -m venv env 
</pre>
## Activate Virtual Environment
<pre>
source env/bin/activate
</pre>
## Install All Requirements
<pre>
pip install -r requirements.txt
</pre>
## Create .env
<pre>
touch .env
</pre>
# Alembic Migrations:
## To initialize a new Alembic migration
<pre>
 alembic init alembic
</pre>
## To automatically generate a new migration script based on the changes detected in your SQLAlchemy models
<pre>
alembic revision --autogenerate -m "name"
</pre>
## To apply all pending migrations
<pre>
alembic upgrade head
</pre>
# Redis:
## Start Redis Server
<pre>
redis-server
</pre>
## To verify that the Redis server is running
<pre>
redis-cli ping
</pre>
## Run project 
<pre>
python app.py
</pre>
## To the Run the Celery worker
<pre>
PYTHONPATH=. celery -A celery_config.celery worker --loglevel=info
</pre>
## To run the Flower
<pre>
PYTHONPATH=. celery -A celery_config.celery flower
</pre>
## Postman Collection
<pre>
https://drive.google.com/drive/folders/1gNDope4agjlb6Qd-7hRkRBe4u4zUI85k?usp=sharing
</pre>
