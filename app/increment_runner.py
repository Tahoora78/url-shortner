# queue_tasker.py
import queue
import threading
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import models
from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager
from functools import lru_cache

visit_queue = queue.Queue()

def increment_visit_count(short_code: str):
    db: Session = SessionLocal()
    try:
        url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        if not url:
            return None
        
        url.visit_count += 1
        db.commit()
    finally:
        db.close()

def worker():
    while True:
        short_code = visit_queue.get()
        print("short_code from queue:", short_code)
        try:
            increment_visit_count(short_code)
        except Exception as e:
            print("Error:", e)
        visit_queue.task_done()

thread = threading.Thread(target=worker, daemon=True)
thread.start()
