# Copyright (c) 2013 Robert Winslow Dalpe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from unittest.mock import patch
from gbobstatusbot.sidebar.stream import create_stream_object, Stream


class MockResponse:
    def __init__(self, json, status):
        self.json = json.encode()
        self.status = status
    def read(self):
        return self.json


class StreamTest(unittest.TestCase):

    def test_create_stream_object_offline(self):
        expected = Stream("rwdalpe", False, "[]")
        with patch('urllib.request.urlopen') as mock:
            mock.return_value = MockResponse(('{"_links":{"channel":"https://ap'
                                              'i.twitch.tv/kraken/channels/rwda'
                                              'lpe","self":"https://api.twit'
                                              'ch.tv/kraken/streams/rwdalpe"},'
                                              '"stream":null}'), 
                                             200)
            actual = create_stream_object("rwdalpe")
            self.assertEqual(expected.stream_name, actual.stream_name)
            self.assertEqual(expected.stream_status, actual.stream_status)
            self.assertEqual(expected.cur_playing, actual.cur_playing)
    
    def test_create_stream_object_online_nogame_gametitle(self):
        expected = Stream("online_gametitle", True, "[Civilization]")
        with patch('urllib.request.urlopen') as mock:
            mock.return_value = MockResponse(('{"stream":{"channel":{"status":"'
                                              'Test stream status'
                                              ' with game [Civilization]"}}}'),
                                             200)
            actual = create_stream_object("online_gametitle")
            self.assertEqual(expected.stream_name, actual.stream_name)
            self.assertEqual(expected.stream_status, actual.stream_status)
            self.assertEqual(expected.cur_playing, actual.cur_playing)
    
    def test_create_stream_object_online_game_nogametitle(self):
        expected = Stream("online_gametitle", True, "[test]")
        with patch('urllib.request.urlopen') as mock:
            mock.return_value = MockResponse(('{"stream":{"channel":{"status":"'
                                              'Test stream status'
                                              ' with no game"}, "game":"test"}}'
                                              ), 200)
            actual = create_stream_object("online_gametitle")
            self.assertEqual(expected.stream_name, actual.stream_name)
            self.assertEqual(expected.stream_status, actual.stream_status)
            self.assertEqual(expected.cur_playing, actual.cur_playing)
    
    def test_create_stream_object_online_nogame_nogametitle(self):
        expected = Stream("online_gametitle", True, "[]")
        with patch('urllib.request.urlopen') as mock:
            mock.return_value = MockResponse(('{"stream":{"channel":{"status":"'
                                              'Test stream status'
                                              ' with no game"}}}'
                                              ), 200)
            actual = create_stream_object("online_gametitle")
            self.assertEqual(expected.stream_name, actual.stream_name)
            self.assertEqual(expected.stream_status, actual.stream_status)
            self.assertEqual(expected.cur_playing, actual.cur_playing)


if __name__ == "__main__":
    unittest.main()