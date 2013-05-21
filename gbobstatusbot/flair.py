"""Manage link flair in a subreddit"""
import logging


def update_flair(reddit, sub_name, mapping):
    """Determine and set link flair for new links in a subreddit
    
    Args:
        reddit: A PRAW Reddit object for a moderator of the subreddit. This
            object should be authenticated.
        sub_name: A string name of the subreddit to be updated
        mapping: A dictionary where the keys are regexes to match to submission
            titles and the values are the link flair CSS classes to apply to
            the matched submissions 
    
    """
    logging.info("Updating link flair for subreddit %s" % sub_name)
    sub = reddit.get_subreddit(sub_name)
    for p in sub.get_new(limit=None):
        if(not p.link_flair_css_class):
            new_flair = get_flair_by_title(mapping, p.title)
            logging.debug("Got mapping %s for title %s" % (new_flair, p.title))
            if(new_flair is not None):
                p.set_flair(flair_text="", flair_css_class=new_flair)


def get_flair_by_title(mapping, title):
    """Map a submission title to a flair CSS class
    
    Args:
        mapping: A dictionary object where the keys are regexes to match against
            submission titles, and the values are the link flair CSS classes to
            apply to the matched submissions
        title: A string representation of a submission's title
    
    Returns:
        A string representing the link flair CSS to be applied to the submission
        or None if the submission title did not map to any value. 
    
    """
    logging.debug("Looking for flair mapping for title %s" % title)
    for key in mapping:
        if key in title:
            return mapping[key]
    return None