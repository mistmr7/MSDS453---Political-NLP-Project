from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


# url = "https://www.reddit.com/r/Conservative/top/?t=year"
# driver.get(url)
# time.sleep(5)
# elements = driver.find_elements(By.CLASS_NAME, "inset-0")
# urls = []
# comments = []
# for e in elements:
#     href = e.get_attribute("href")
#     if href is not None:
#         urls.append(href)

# for u in url:
#     driver.get(url)
#     time.sleep(5)
# lengths = []
# for i in range(10):
#     url = "https://www.reddit.com/r/Conservative/comments/1d4el7p/breaking_trump_found_guilty_on_all_34_charges/"
#     driver.get(url)
#     time.sleep(1)
#     comments = []
#     elements = driver.find_elements(By.XPATH, '//div[@id="-post-rtjson-content"]/p')
#     for element in elements:
#         print(element.text)
#         comments.append(element.text)

#     lengths.append(len(comments))
# print(lengths)


class AggregateRedditComments:
    def __init__(self, *args, **kwargs):
        self.comments = []
        self.posts = []
        self.subreddit_lengths = []
        self.comment_lengths = []

    def get_subreddit_posts(self, subreddit):
        print(subreddit)
        posts = []
        self.driver = webdriver.Edge()
        self.driver.get(subreddit)
        time.sleep(10)
        elements = self.driver.find_elements(By.CLASS_NAME, "inset-0")
        for element in elements:
            href = element.get_attribute("href")
            if href is not None:
                posts.append(href)
        self.posts.append(posts)
        # self.get_subreddit_comments(posts)
        self.driver.quit()
        time.sleep(2)
        self.subreddit_lengths.append(len(posts))

    def get_subreddit_comments(self, posts):
        for post in posts:
            self.driver = webdriver.Edge()
            print(post)
            self.driver.get(post)
            time.sleep(1)
            elements = self.driver.find_elements(
                By.XPATH, '//div[@id="-post-rtjson-content"]/p'
            )

            self.comment_lengths.append(len(elements))
            for element in elements:
                self.comments.append(element.text)
            self.driver.quit()


if __name__ == "__main__":
    start = time.perf_counter()
    url_base = "https://www.reddit.com/r/"
    # url_middles = [
    #     "Conservative",
    #     "Conservatives",
    #     "asktrumpsupporters",
    #     "prolife",
    #     "askconservatives",
    #     "capitalism",
    #     "republican",
    #     "walkaway",
    #     "progun",
    # ]
    url_middles = [
        # "Liberal",
        # "dsa",
        # "WayOfTheBern",
        # "Progressive",
        # "murderedbyaoc",
        # "esist",
        # "askaliberal",
        # "democrats",
        "joebiden",
    ]
    url_suffix = "/top/?t=year"

    reddit_driver = AggregateRedditComments()

    for middle in url_middles:
        reddit_driver.get_subreddit_posts(url_base + middle + url_suffix)

    print(reddit_driver.subreddit_lengths)
    print(reddit_driver.comment_lengths)

    for post in reddit_driver.posts:
        try:
            reddit_driver.get_subreddit_comments(post)
        except TimeoutException:
            print(post)
            pass

    print(reddit_driver.comments)
    print(reddit_driver.comment_lengths)

    with open("r_joebiden.txt", "w", encoding="utf-8") as f:
        for comment in reddit_driver.comments:
            f.write(f"{comment}\n")

    end = time.perf_counter()
    print(end - start)
