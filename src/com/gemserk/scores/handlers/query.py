'''
Created on 12/08/2010

@author: gemserk
'''
from google.appengine.ext import webapp

import cgi
import time

from django.utils import simplejson as json

from com.gemserk.scores.model.game import Game

from com.gemserk.scores.model import score as scoreDao

from  com.gemserk.scores.utils import dateutils
import datetime

class Query(webapp.RequestHandler):  
    
    def get(self):
        gameKey = cgi.escape(self.request.get('gameKey'))
        game = Game.all().filter("gameKey =", gameKey).get()
        
        if(not game):
            self.response.set_status(500, message="Can't find game with key " + gameKey)
            return
        
        range = self.request.get('range')
        tags = self.request.get_all('tag')        
        limit = self.request.get_range('limit')
        ascending = self.request.get('ascending')
        
        distinct  = self.request.get('distinct', "true")
        distinct = False if distinct == "false" else True 
                
        if(ascending == "true"):
            order = "points"
        else:
            order = "-points"
        
        rangeNumber  = self.request.get_range('rangeNumber')
         
        year, month, week, day = dateutils.get_datetime_data(datetime.datetime.now())
        scores = scoreDao.get_scores(game, range, tags, order, limit, year, month, week, day, rangeNumber, distinct)

        self.response.headers['Content-Type'] = 'text/plain'
        scoreList = []
        for score in scores:
            data = json.loads(score.data)
            scoreData = {'id': str(score.key()), 'profilePublicKey': score.profilePublicKey, 'name': score.name, 'tags':score.tags, 'points':score.points, 'timestamp':long(time.mktime(score.timestamp.timetuple())*1000), 'data':data}
            scoreList.append(scoreData)
        
        self.response.out.write(json.dumps(scoreList))
        
