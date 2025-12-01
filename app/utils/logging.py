import functools
from datetime import datetime

def log_visit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if request:
            client_ip = request.client.host
            timestamp = datetime.utcnow().isoformat()
            print(f"[VISIT] IP={client_ip} | TIME={timestamp}")
        
        return func(*args, **kwargs)

    return wrapper