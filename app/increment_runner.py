# queue_tasker.py
import queue
import threading
import time
import os
import random
import string
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models
from sqlalchemy.exc import IntegrityError
import redis
from contextlib import contextmanager
from functools import lru_cache

visit_queue = queue.Queue()

def increment_visit_count(short_code: str):
    # it should pop the elements from the queue and increment the count in the database
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
        try:
            increment_visit_count(short_code)
        except Exception as e:
            print("Error:", e)
        visit_queue.task_done()

thread = threading.Thread(target=worker, daemon=True)
thread.start()
