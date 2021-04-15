from gameboard import Board

import random
from random import choice, uniform

from gamerules import Checker
from abc import ABC, abstractmethod
import numpy as np


from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from collections import deque
from math import exp, log

class Player(ABC):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        self.id = playernum
        self.board = board
        self.checker = checker
    
    @abstractmethod
    def play(self) -> int:
        pass


class Human(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
      
    def play(self) -> int:
        col = int( input("Column: ") ) -1
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            print("Wrong column")
            self.play()


class ComputerRand(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)

    def play(self) -> int:
        col = random.randint(0, self.board.cols -1)
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            self.play() #Invalid column selected, try again
            

class ComputerDef(Player): #Defensive IA player
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
      
    def play(self) -> int:
        maxscore = 0
        selectedcolumn = 0
        
        # Tries to predict other player's best move and 'steals' it:
        for col in range(self.board.cols):
            row = self.board.insert(col, 1, trial=True)
            if row != -1:
                trialscore = self.checker.checkgrid(1, row, col)
                #print("trialscore: ", trialscore)
                if trialscore > maxscore:
                    maxscore = trialscore
                    selectedcolumn = col
                
        col = selectedcolumn
        #print("CPUscore: ", maxscore)
        if maxscore < 2:
            col = random.randint(0, self.board.cols -1)
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            self.play() #Invalid column selected, try again

class PlayerDQN(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
        self.dqnagent = DQNAgent(self.board.cols*self.board.rows,self.board.cols,1)
        #self.dqnagent = DQNAgent(42,7,1)


    def play(self):
        #print(self.board.cols,1) ##########################################
        #print(self.board.cols*self.board.rows)
        action = self.dqnagent.act(self.board.grid)
        row = self.board.insert(action, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, action)

        else:
            self.play() #Invalid column selected, try again


# Deep Q-learning Agent
class DQNAgent:

    def __init__(self, state_size, action_size, episodes):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=500)
        self.gamma = 0.9   # discount rate
        self.epsilon = 0.10  # initial exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = exp((log(self.epsilon_min) - log(self.epsilon))/(0.8*episodes)) # reaches epsilon_min after 80% of iterations
        self.model = self._build_model()
    
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(20, input_dim=self.state_size, activation='relu'))
      
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr = 0.00001))
        return model
    
    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        if np.random.rand() <= self.epsilon: # Exploration
            return choice([c for c in range(self.action_size) if (state[:,c] == 0).any()])
            #when exploring, I allow for "wrong" moves to give the agent a chance 
            #to experience the penalty of choosing full columns
            #return choice([c for c in range(self.action_size)])
        act_values = self.model.predict(state.reshape(1,-1)) # Exploitation     ###############################reshape##########""
        action = np.argmax(act_values[0]) 
        return action
    
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state.reshape(1,-1), target_f, epochs=1, verbose=0)#################################reshape##########
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)
    
    def save(self, name):
        self.model.save_weights(name)
