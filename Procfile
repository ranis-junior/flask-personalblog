web: flask db upgrade; flask transflate compile; gunicorn microblog:app
worker: rq worker -u $REDIS_URL personalblog_tasks