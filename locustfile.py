import os
from locust import HttpLocust, TaskSet, between
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
    wait_time = between(30, 60)