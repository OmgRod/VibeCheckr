import time
from collections import defaultdict, deque
import random

start_time = time.time()
emotion_counts = defaultdict(int)
message_timestamps = deque(maxlen=600)

def register_message(emotion):
    emotion_counts[emotion] += 1
    message_timestamps.append(time.time())

def get_metrics():
    now = time.time()
    recent_msgs = [ts for ts in message_timestamps if now - ts <= 60]
    return {
        "start_time": start_time,
        "total_messages": sum(emotion_counts.values()),
        "messages_per_minute": len(recent_msgs),
        "server_strain": min(100, len(recent_msgs) * 1.5 + random.randint(0, 5)),
        "emotion_counts": dict(emotion_counts)
    }
