from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import pprint


class AggregateRedditComments:
    url_base = "https://www.reddit.com/r/"
    conservative_middles = [
        "Conservatives",
        "asktrumpsupporters",
        "prolife",
        "askconservatives",
        "capitalism",
        "republican",
        "walkaway",
        "progun",
        "Conservative",
    ]
    liberal_middles = [
        "Liberal",
        "dsa",
        "WayOfTheBern",
        "Progressive",
        "murderedbyaoc",
        "esist",
        "askaliberal",
        "democrats",
        "joebiden",
    ]
    url_suffix = "/top/?t=year"

    def __init__(self, *args, **kwargs):
        self.comments = []
        self.liberal_posts = []
        self.conservative_posts = []
        self.liberal_comments = []
        self.conservative_comments = []
        self.reddit_df = pd.DataFrame(
            columns=["Political Leaning", "Subreddit", "Comment Title", "Comment Text"]
        )

    def get_subreddit_posts(self, subreddit, subreddit_type):
        posts = []
        self.driver = webdriver.Edge()
        url = self.url_base + subreddit + self.url_suffix
        self.driver.get(url)
        time.sleep(10)
        elements = self.driver.find_elements(By.CLASS_NAME, "inset-0")
        for element in elements:
            href = element.get_attribute("href")
            if href is not None:
                posts.append(href)
        if subreddit_type == "C":
            self.conservative_posts.append(posts)
        elif subreddit_type == "L":
            self.liberal_posts.append(posts)
        self.driver.quit()

    def get_subreddit_comments(self, post, subreddit_type):
        try:
            title = post.split("/")[-2].replace("_", " ").title()
            subreddit = post.split("/")[4]
        except IndexError:
            print(post)
            return False
        self.driver = webdriver.Edge()
        self.driver.get(post)
        time.sleep(1)
        elements = self.driver.find_elements(
            By.XPATH, '//div[@id="-post-rtjson-content"]/p'
        )
        if subreddit_type == "C":
            for element in elements:
                self.conservative_comments.append(element.text)
                self.add_to_dataframe("Conservative", subreddit, title, element.text)
        elif subreddit_type == "L":
            for element in elements:
                self.liberal_comments.append(element.text)
                self.add_to_dataframe("Liberal", subreddit, title, element.text)

        self.driver.quit()

    def add_to_dataframe(self, subreddit_type, subreddit, comment_title, comment_text):
        new_row = {
            "Political Leaning": subreddit_type,
            "Subreddit": subreddit,
            "Comment Title": comment_title,
            "Comment Text": comment_text,
        }
        self.reddit_df = pd.concat(
            [self.reddit_df, pd.DataFrame([new_row])], ignore_index=True
        )

    def create_excel_file(self):
        self.reddit_df.to_excel("RedditExcelOutput.xlsx", engine="xlsxwriter")


if __name__ == "__main__":
    start = time.perf_counter()

    reddit_driver = AggregateRedditComments()
    for subreddit in reddit_driver.conservative_middles:
        try:
            reddit_driver.get_subreddit_posts(subreddit, "C")
        except TimeoutException:
            reddit_driver.conservative_middles.append(subreddit)
            pass

    pprint.pprint(reddit_driver.conservative_middles)

    pprint.pprint(reddit_driver.conservative_posts)

    for post_group in reddit_driver.conservative_posts:
        for post in post_group:
            reddit_driver.get_subreddit_comments(post, "C")

    for subreddit in reddit_driver.liberal_middles:
        try:
            reddit_driver.get_subreddit_posts(subreddit, "L")
        except TimeoutException:
            reddit_driver.liberal_middles.append(subreddit)
            pass

    pprint.pprint(reddit_driver.liberal_middles)

    pprint.pprint(reddit_driver.liberal_posts)

    for post_group in reddit_driver.liberal_posts:
        for post in post_group:
            reddit_driver.get_subreddit_comments(post, "L")

    reddit_driver.create_excel_file()

    end = time.perf_counter()
    print(end - start)
