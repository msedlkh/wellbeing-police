import pandas as pd
import praw
import config
from datetime import datetime

## Credential
client_id_ = config.Credential["client_id"]
client_secret_ = config.Credential["client_secret"]
user_agent_ = config.Credential["user_agent"]
reddit = praw.Reddit(
    client_id=client_id_, client_secret=client_secret_, user_agent=user_agent_
)

print("==========================START================================")
with open("subreddits.txt") as file:
    for line in file:
        subname = line.rstrip()
        print(f"================== START: {subname} ====================")
        print(f"getting posts from: {subname}")
        posts = []
        praw_subreddit = reddit.subreddit(subname)
        for post in praw_subreddit.hot(limit=None):
            posts.append(
                [
                    post.title,
                    post.score,
                    post.id,
                    post.subreddit,
                    post.url,
                    post.num_comments,
                    post.selftext,
                    post.created,
                ]
            )
        posts_df = pd.DataFrame(
            posts,
            columns=[
                "title",
                "score",
                "id",
                "subreddit",
                "url",
                "num_comments",
                "body",
                "created",
            ],
        )
        size = len(posts_df)
        current_time = datetime.now()
        timestamp = current_time.strftime("%y%m%d%H%M%S")
        filename = f"csvs/{timestamp}_{subname}_{size}.csv"
        print(f"Generating CSV with filename: {filename}")
        posts_df.to_csv(filename)
        print(f"================== END: {subname} ====================")
print("==========================END================================")
