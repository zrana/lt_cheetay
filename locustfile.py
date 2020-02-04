import os
from locust import HttpLocust, TaskSet
from CheetayLocustTasks import CheetayTasks


class CheetayTasks(TaskSet):
    tasks = {
        CheetayTasks: 1,
    }


class CheetayLocust(HttpLocust):
    """
    Representation of an HTTP "user".
    Defines how long a simulated user should wait between executing tasks, as
    well as which TaskSet class should define the user's behavior.
    """
    host = 'https://test.cheetay.pk/'
    task_set = globals()[os.getenv('LOCUST_TASK_SET', 'CheetayTasks')]
    min_wait = 30000
    max_wait = 60000