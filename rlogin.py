def mb():
    import praw
    r = praw.Reddit(username='',
                    password='',
                    client_id='',
                    client_secret='',
                    user_agent='')
    return r
