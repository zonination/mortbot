# Import python libraries
import praw
import prawcore
import rlogin
import time

# Log in to the bot
r=rlogin.mb()
print('Logged in as: {0}'.format(r.user.me()))
print('')

# Number of hours to delay
minutes = 60

# Main function: Check subreddit mail
def chksubmail():
    #print('Checking modmail...')
    
    # Check all chains in inbox
    for chain in r.subreddit('mortgages').modmail.conversations(limit=10, state='join_requests'):
        
        # Keep and read a log of subreddit modmails, so we don't modmail twice.
        f = open('.log.txt', 'r')
        log = f.read().split(' ')
        f.close()
        
        if (chain.id not in log):
            print('Valid chain: {0}'.format(chain.id))
            
            # Count the number of replies
            n = 0
            for message in r.subreddit('mortgages').modmail(chain.id, mark_read=True).messages:
                author = message.author.name
                n = n + 1
            
            if n == 1:
                print('  Replying to {0}'.format(author))
                
                # Caught a live one! Log the event
                f = open('.log.txt', 'a+')
                log = f.write('{0} '.format(chain.id))
                f.close()
                
                # Replying to text, then archiving the conversation
                chain.reply('[Hello there](https://thumbs.gfycat.com/NeatFlimsyKingfisher-mobile.mp4), {0}! Thank you for reaching out. As you\'re well aware, and as per the sticky on the subreddit, we\'re no longer taking submissions to /r/Mortgages[,](https://www.reddit.com/r/redditrequest/comments/fc7jh7/requesting_rmortgages_five_months_after_mod_hid/) because of significant amounts of spam and fraud.\n\nBut there\'s excellent news! We\'re redirecting submissions to /r/PersonalFinance instead. I think you\'ll find the management is quite effective and welcoming there, and with instant results.\n\nAll the best,  \n— the /r/Mortgages mod team'.format(author), author_hidden=True)
                print('  Archiving chain.\n')
                chain.archive()
                
            elif n > 1:
                print('  Another mod replied already: n = {0}\n'.format(n))
            else:
                print('  Chain in log.\n')
            
        else:
            print('')


# Check personal mail and clear inbox
def check_mail():
    #print('Checking mail...')
    for message in r.inbox.unread(limit=10):
        try:
            # Skip non-messages and some accounts
            if not message.fullname.startswith("t4_") or message.author in ['mod_mailer', 'reddit', 'ModNewsletter']:
                message.mark_read()
                print('Marked as read: One of those annoying fucking Snoosletters.')
                continue
            
            # Skip non-subreddit messages
            if not message.subreddit:
                message.mark_read()
                print('Marked as read: non-subreddit message.')
                continue
                
            sub = message.subreddit.display_name
            message.mark_read()
        
        except praw.exceptions.APIException:
            print('  Probably a false alarm...')

# Main loop
while True:
    try:
        chksubmail()
        check_mail()
        
        # Sleep for a specified numbr of minutes
        time.sleep(60*minutes)
    
    # Exception list for when Reddit inevitably screws up
    except praw.exceptions.APIException:
        print('\nAn API exception happened.\nTaking a coffee break.\n')
        time.sleep(30)
    except prawcore.exceptions.ServerError:
        print('\nReddit\'s famous 503 error occurred.\nTaking a coffee break.\n')
        time.sleep(180)
    except prawcore.exceptions.RequestException:
        print('.')
        time.sleep(180)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as inst:
        print(type(inst))
        print(inst.args)        
        print('')
        time.sleep(30)
#    except:
#        print('\nException happened (mortgages_bot).\nTaking a coffee break.\n')
#        time.sleep(30)
