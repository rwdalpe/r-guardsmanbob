using gbobstatusbot.Reddit;
using NUnit.Framework;
using System;
using System.Configuration;

namespace gbobstatusbot.Reddit.Tests.Integration_Tests
{
    [TestFixture ()]
    public class Sidebar
    {
        private string username = "";
        private string password = "";
        private string subredditName = "";

        [SetUp]
        public void Initialize()
        {

        }

        [Test ()]
        [Category("Integration Tests")]
        public void TestGetCurrentText ()
        {
        }
    }
}

