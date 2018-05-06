import praw
from db_engine import DBConnection
from cons import SPOILER, DB

class Reddit(object):
    def __init__(self):
        self.api = praw.Reddit(client_id='DiI57R025MBQLQ',
                               client_secret='4IaDtRqQrX4jIEDZeYqh_y4cJCA',
                               user_agent='script')

        self.db_connection = DBConnection()
        self.subreddit_list = []
        self.submission_list = []

    def get_subreddit(self, name):
        # assume you have a Reddit instance bound to variable `reddit`
        subreddit = self.api.subreddit(name)
        self.subreddit_list.append(subreddit)

        # print(subreddit.display_name)
        # print(subreddit.title)
        # print(subreddit.description)

    def get_top_comments(self, subreddit):
        count = 0
        for submission in subreddit.new():
        # for submission in subreddit.top(time_filter='month'):
        # for submission in subreddit.new(limit=1000):
            count +=1
            # print(dir(submission))
            if "spoiler" in submission.title.lower() or submission.spoiler:
                comments = submission.comments.list()
                for comment in comments:
                    
                print(submission.title)
                print(submission.selftext)
                if submission.selftext != "":
                    doc = {
                        SPOILER.ID: submission.id,
                        SPOILER.TITLE: submission.title,
                        SPOILER.CONTENT: submission.selftext,
                        SPOILER.SHOW: 'Breaking Bad',
                    }
                    try:
                        self.db_connection.insert(doc)
                    except Exception:
                        pass



            # print(submission.title)
            # print(submission.selftext)
            # comments = submission.comments.list()
            # for comment in comments:
            #     print(comment.body)
            # print(submission.title)  # Output: the submission's title
            # print(submission.score)  # Output: the submission's score
            # print(submission.id)  # Output: the submission's ID
            # print(submission.url)
            # submission.# Output: the URL the submission points to
            # print("-------")
            # or the submission's URL if it's a self post

            # top_level_comments = list(submission.comments)
            # all_comments = submission.comments.list()
        print(count)

if __name__ == "__main__":
    r = Reddit()
    r.get_subreddit(name="breakingbad")
    r.get_top_comments(subreddit=r.subreddit_list[0])