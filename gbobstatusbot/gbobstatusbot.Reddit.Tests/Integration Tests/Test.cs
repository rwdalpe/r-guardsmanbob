using gbobstatusbot.Reddit;
using NUnit.Framework;
using System;
using System.Configuration;

namespace gbobstatusbot.Reddit.Tests.Integration_Tests
{
    [TestFixture ()]
    public class Sidebar
    {
        private string username = ConfigurationManager.AppSettings["username"];
        private string password = ConfigurationManager.AppSettings["password"];
        private string subredditName = ConfigurationManager.AppSettings["subreddit"];
        private gbobstatusbot.Reddit.Sidebar sidebar;

        [SetUp]
        public void Initialize()
        {
            sidebar = new gbobstatusbot.Reddit.Sidebar (username, password, subredditName);
        }

        [Test ()]
        [Category("Integration Tests")]
        public void TestGetCurrentText ()
        {
            string desc = sidebar.CurrentText ();
            Assert.IsTrue (desc.Contains ("Stream Status"));
        }
    }
}

