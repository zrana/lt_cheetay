from cheetay_apis import CheetayApis
from locust import task, TaskSet
from config import USER_CREDENTIALS
import random


class CheetayTasks(TaskSet):

    def __init__(self, *args, **kwargs):
        """
        Initialize the Task set.
        """
        super(CheetayTasks, self).__init__(*args, **kwargs)
        self.cheetay_apis = CheetayApis(self.locust.host, self.client)

    def on_start(self):
        """
        Login to Cheetay
        """
        self.credentials = random.choice(USER_CREDENTIALS)
        USER_CREDENTIALS.remove(self.credentials)
        print(len(USER_CREDENTIALS))
        email = self.credentials[0]
        self.cheetay_apis.login(email)
        # self.cheetay_apis.homepage()

    @task(3)
    def search(self):
        self.cheetay_apis.search_partner()

    @task(9)
    def food_tiles(self):
        self.cheetay_apis.food_tiles()

    @task(6)
    def restaurant_detail_page(self):
        self.cheetay_apis.restaurant_detail()

    # @task(1)
    # def add_to_basket(self):
    #     self.cheetay_apis.add_basket()

    @task(3)
    def checkout_call(self):
        self.cheetay_apis.final_checkout()

    @task(1)
    def order_list(self):
        self.cheetay_apis.order_list()

