''' LICENCE
This file is part of primeDiceBot.

    primeDiceBot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    primeDiceBot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Nome-Programma.  If not, see <http://www.gnu.org/licenses/>.
'''

import primeDiceClass as primedice
import requests
import json
import sys
import logging
import random
import math

class primedice_tester():
    def __init__(self, balance = 200):
        self.login_url = 'https://api.primedice.com/api/login'
        self.bet_url = 'https://api.primedice.com/api/bet'
        self.info_url = 'https://api.primedice.com/api/users/1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 Chrome/43.0.2357.130 Safari/537.36'
        }
        self.session = requests.Session()
        self.bet_count = 0
        self.balance = balance
        self.sleep_interval = 0
        self.token = ''
        self.rate = {'10' : 9.9, '15' : 6.6, '20' : 4.95, '25' : 3.96, '30' : 3.3, '35' : 2.829, '40' : 2.475, '45' : 2.2,\
            '50' : 2, '55' : 1.8, '60' : 1.65, '65' : 1.5, '70' : 1.414, '75' : 1.32, '80' : 1.238, '85' : 1.165, '90' : 1.1, '95' : 1.042}

    def session_post(self, url, post):
        pass

    def login(self, username, password):
        pass

    def percent2gain(self, target, amount):
      #rate = 6.493 - 0.071 * target
      #rate = -3.373326116 * math.log10(target) + 15.60586788
      #rate = self.rate[str(int(target))]
      #POW approximation
      rate = round( 98.99259811 * pow(target, -9.999729126E-1 ), 4)
      
      logging.debug ('rate = '+str(rate)+' res = '+str(rate*amount))
      
      return rate*amount
      
    def calculate_bet(self, amount, condition, target):
        '''
        http://www.mathportal.org/calculators/statistics-calculator/correlation-and-regression-calculator.php
        X: 15,20,25,30,40,49.5,50,60,66,70,80,90
        Y: 6.6,4.95,3.96,3.3,2.475,2,1.98,1.65, 1.5, 1.414,1.238,1.1
        y = 5.788 − 0.062⋅x
        
        X: 10  15  20   25   30  35     40    45  49.5 50    55  60   66  70    75    80      85     90   95
        Y: 9.9 6.6 4.95 3.96 3.3 2.829  2.475 2.2 2    1.98  1.8 1.65 1.5 1.414 1.32  1.238   1.165  1.1  1.042        
        y = 6.493 − 0.071⋅x
        
        10 9.9
        15 6.6
        20 4.95
        25 3.96
        30 3.3
        35 2.829
        40 2.475
        45 2.2
        50 1.98
        55 1.8
        60 1.65
        66 1.5
        70 1.414
        75 1.32
        80 1.238
        85 1.165
        90 1.1
        95 1.042

        y = -3.373326116 ln(x) + 15.60586788
         
        '''
        dice = round(random.uniform(00, 100), 2)
        logging.debug('dice = '+str(dice))
        
        if ( (condition == "<" and dice < target) or (condition == ">" and dice > target)): 
            win = True
            profit = round( self.percent2gain(target, amount), 4 )
            self.balance = self.balance + profit
        else: 
            win = False
            profit = -1 * amount
            self.balance = self.balance - amount
            
        if(win):
          res = "+"
        else:
          res = "-"
        
        log_str = res+ '  amount: '+str(amount)+' condition: '+str(condition)+' target: "'+str(target)+'" dice: '+str(dice)+' balance: '+str(round(self.balance, 2))+' profit: '+str(round(profit, 2))
        logging.debug(log_str)
        print(log_str)
        
        jackpot = False        
        return (jackpot,win,amount)
        
        
        
    def bet(self, amount = 0, target = 95, condition = "<"):
        try:
            target = float(target)
            amount = int(amount)
        except:
            return "Target must be an integer!"

        #try:
        if not condition in ["<",">"]:
            logging.debug ("Wrong condition. Must be either > or <")
        else:
            params = {
                'access_token': self.token
            }
            
            (jackpot,win,amount) = self.calculate_bet(amount, condition, target)

            feedback = {
                'jackpot': jackpot,
                'win': win,
                'amount': amount,
            }
            
            #print (feedback)
            return feedback


        #except:
        #    logging.debug ("Some error happened processing your request")

class helpers():
    def config_check(self, config):
        try:
            config.base_bet = float(config.base_bet)
        except:
            sys.exit("Base bet must be a float")

        try:
            config.base_bet = int(config.base_bet)
        except:
            sys.exit("Base bet must be a integer")

        try:
            config.win_chance = float(config.win_chance)
        except:
            sys.exit("Win chance must be a float")

        if config.win_chance > 98 or config.win_chance < 0.01:
            sys.exit("Win chance not in range 0.01 - 98")
