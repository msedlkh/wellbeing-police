import pandas as pd
import praw
import argparse
import config
from datetime import date


## Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query", help="subreddit to query")
parser.add_argument("-n", "--size", type=int, help="size to query")
args = parser.parse_args()
print("You are querying subreddit r/" + args.query)
print("Query Size : ", args.size)


## Credential
client_id_ = config.Credential["client_id"]
client_secret_ = config.Credential["client_secret"]
user_agent_ = config.Credential["user_agent"]
reddit = praw.Reddit(
    client_id=client_id_, client_secret=client_secret_, user_agent=user_agent_
)

posts = []
ml_subreddit = reddit.subreddit(args.query)
for post in ml_subreddit.hot(limit=None):
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
posts = pd.DataFrame(
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


today = date.today()
str_date = today.strftime("%y%m%d")
filename = f"csvs/{str_date}_{args.query}_{args.size}.csv"
print("Generating CSV with filename: " + filename)
posts.to_csv(filename)
print("Done")
