using System;
using System.Configuration;
using RedditSharp;
using RedditSharp.Things;

namespace gbobstatusbot.Reddit
{
    public class Sidebar
    {
        private string redditUsername;
        private string redditPassword;
        private RedditSharp.Reddit reddit;

        public string Subreddit { get; private set; }

        public Sidebar (string username, string password, string subreddit)
        {
            redditUsername = username;
            redditPassword = password;
            Subreddit = subreddit;

            reddit = new RedditSharp.Reddit (username, password, true);
        }

        public string CurrentText() {
            RedditSharp.Things.Subreddit sr = reddit.GetSubreddit (Subreddit);
            return sr.Description;
        }
    }
}

