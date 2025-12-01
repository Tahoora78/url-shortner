import os
import random
import string
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import models
from sqlalchemy.exc import IntegrityError
import redis
from contextlib import contextmanager
from functools import lru_cache

KEY_BUFFER = []

_redis_host = os.getenv("REDIS_HOST", "localhost")
_redis_port = int(os.getenv("REDIS_PORT", "6379"))
_redis_db = int(os.getenv("REDIS_DB", "0"))
redis_client = redis.Redis(host=_redis_host, port=_redis_port, db=_redis_db)

def _random_code(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def create_short_url(original_url: str):
    global KEY_BUFFER
    db: Session = SessionLocal()
    try:
        if not KEY_BUFFER:
            KEY_BUFFER = get_100_unique_key()

        code = KEY_BUFFER.pop()
        url = models.URL(original_url=original_url, short_code=code)
        db.add(url)
        try:
            db.commit()
            db.refresh(url)
            return url
        except IntegrityError:
            db.rollback()
    finally:
        db.close()


@lru_cache(maxsize=1024)
def get_url_by_code(short_code: str):
    db: Session = SessionLocal()
    try:
        return db.query(models.URL)\
                 .filter(models.URL.short_code == short_code)\
                 .first()
    finally:
        db.close()


# def increment_visit_count(short_code: str):
#     # it should pop the elements from the queue and increment the count in the database
#     db: Session = SessionLocal()
#     try:
#         url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
#         if not url:
#             return None
        
#         url.visit_count += 1
#         db.commit()
#     finally:
#         db.close()

def get_visit_count(short_code: str):
    db: Session = SessionLocal()
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not url:
        return 0
    return url.visit_count


def to_base36(num: int) -> str:
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return "0"
    out = []
    while num > 0:
        num, r = divmod(num, 36)
        out.append(chars[r])
    return ''.join(reversed(out))


def generate_keys():
    batch_size = 1000
    db: Session = SessionLocal()
    
    try:
        counter = db.query(models.Counter).filter(models.Counter.id == 1).with_for_update().first()
        start = counter.value
        end = start + batch_size

        keys = []
        for i in range(start, end):
            k = to_base36(i).rjust(7, "0")
            keys.append(k)

        objs = [models.Key(value=k) for k in keys]
        db.bulk_save_objects(objs)

        counter.value = end
        db.commit()
    finally:
        db.close()

    return {"generated": batch_size, "start": start, "end": end, "keys": keys}


@contextmanager
def redis_lock(lock_key, expire=10):
    lock = redis_client.lock(lock_key, timeout=expire)
    acquired = lock.acquire(blocking=True)
    try:
        if not acquired:
            raise RuntimeError("Could not acquire distributed lock")
        yield
    finally:
        if acquired:
            lock.release()


def get_100_unique_key():
    with redis_lock("keys:global_lock"):
        with SessionLocal() as db:
            with db.begin():

                total = db.query(models.Key).count()
                if total < 300:
                    generate_keys()
                    db.flush()

                keys = (
                    db.query(models.Key)
                    .order_by(models.Key.value.asc())
                    .limit(100)
                    .all()
                )

                if len(keys) < 100:
                    raise RuntimeError("Not enough keys available.")

                vals = [k.value for k in keys]
                (
                    db.query(models.Key)
                    .filter(models.Key.value.in_(vals))
                    .delete(synchronize_session=False)
                )
                return vals
