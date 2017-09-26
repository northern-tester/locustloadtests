from locust import HttpLocust, TaskSet, task
from pyquery import PyQuery
import random


class GoogleTasks(TaskSet):

    toc_urls = []

    def on_start(self):
        pass

    @task(1)
    def homepage(self):
        self.client.get("/")

    @task(1)
    def search(self):
        searchterms = ["cheese", "bread", "ham"]
        searchterm = random.choice(searchterms)
        r = self.client.get("/search?q="+searchterm)
        pq = PyQuery(r.content)
        link_elements = pq("#res h3.r a")
        self.toc_urls = [
            l.attrib["href"] for l in link_elements
        ]

    @task(1)
    def result(self):
        url = random.choice(self.toc_urls)
        self.client.get(url)


class WebsiteUser(HttpLocust):
    task_set = GoogleTasks
    # If you don't declare a host you have to pass it in the cli using --host
    host = "https://www.google.co.uk"
    # If you don't specify a min and max wait, it will default to a second
    min_wait = 5000
    max_wait = 15000