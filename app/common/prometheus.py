from prometheus_client import Counter

TASKS_REQUESTS = Counter("tasks", "Total count of tasks by type and name.", ["type", "name"])
