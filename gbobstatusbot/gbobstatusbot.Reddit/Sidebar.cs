using System;
using System.Configuration;
using RedditSharp;

namespace gbobstatusbot.Reddit
{
    public class Sidebar
    {
        private string redditUsername;
        private string redditPassword;
        private RedditSharp.Reddit reddit;

        public string Subreddit { get; set; }

        public Sidebar (string username, string password, string subreddit)
        {
            redditUsername = username;
            redditPassword = password;
            Subreddit = subreddit;

            reddit = new RedditSharp.Reddit (username, password, true);
        }

        public string CurrentText() {

        }
    }
}

