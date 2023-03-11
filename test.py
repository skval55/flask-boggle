from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!


  
    def test_session_info(self):
        """checking to see if correct document is connecting to '/'"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertTrue(session['table'])
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="text-center ">BOGGLE!</h1>', html)
   
    def test_check_word(self):
        """test to see if are getting a response from json from get request"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=cat')
            self.assertTrue(response.json['result'])    
            self.assertEqual(response.status_code, 200)              

    def test_get_score(self):
        """test to see if are getting a response from json from post request"""
        with app.test_client() as client:
            client.get('/')
            response = client.post('/get-score', json = { 'score': 10 })
            self.assertTrue(response.json['score'])    
            self.assertEqual(response.status_code, 200)              

    def test_valid_word(self):
        """test to see if session will hold table and see if word is correct """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['table']= [['C', 'O', 'O', 'L', 'L'],
                                ['C','O','O','L','L'],
                                ['C','O','O','L','L'],
                                ['C','O','O','L','L'],
                                ['C','O','O','L','L']]
            response = client.get('/check-word?word=cool')
            self.assertEqual(response.status_code, 200) 
            self.assertEqual(response.json['result'], 'ok')

    def test_dictionary(self):
        """test to see if word is in dictionary but not board"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=chocolate')
            self.assertEqual(response.json['result'], "not-on-board")
   
    def test_not_word(self):
        """test not word"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word=kasdj')
            self.assertEqual(response.json['result'], "not-word")
   
    def test_new_highscore(self):
        """test to see if correct response to new high score"""
        with app.test_client() as client:
            response = client.post('/get-score', json = { 'score': 10 })
            self.assertEqual(response.status_code, 200) 
            self.assertEqual(response.json['new_highscore'], "new high score")
    
    def test_not_new_highscore(self):
        """test to see if correct response to not a new high score"""
        with app.test_client() as client:
            response = client.post('/get-score', json = { 'score': -1 })
            self.assertEqual(response.status_code, 200) 
            self.assertEqual(response.json['new_highscore'], "nice try, but no high score")

