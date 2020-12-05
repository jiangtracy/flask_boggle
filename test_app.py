from unittest import TestCase

import json

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            # test that you're getting a template
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form method="POST" id="newWordForm">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            # write a test for this route

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.headers.get('content-type')
                == 'application/json')

            response_dict = json.loads(response.data)
            self.assertIn(response_dict["gameId"], games.keys())
            self.assertTrue(type(response_dict["board"]) is list)
            

       
    def test_api_score_word(self):
        """ Check if word  is legal """
        with self.client as client:
            response = client.get('/api/new-game')
    
        gameid = response.get_json()['gameId']
        game = games[gameid]
        game.board = [
            ['X', 'Y', 'S', 'D', 'A'],
            ['F', 'D', 'W', 'E', 'P'],
            ['S', 'D', 'W', 'E', 'P'],
            ['D', 'E', 'S', 'Q', 'L'],
            ['S', 'E', 'W', 'V', 'E']
        ]
    
        response = self.client.post('/api/score-word', json={
                'gameId': gameid,
                'word': 'APPLE'
            })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'result': 'ok'})

        
        response = self.client.post('/api/score-word', json={
                'gameId': gameid,
                'word': 'PEAR'
                })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'result': "not-on-board"})
