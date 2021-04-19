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
import os.path

class Player(ABC):
    def __init__(self, playernum: int, board: Board, checker: Checker,repeat:int=1):
        self.id = playernum
        self.board = board
        self.checker = checker
    
    @abstractmethod
    def play(self,e) -> int:
        pass
    
    def send_reward(self,reward):
        pass


class Human(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
      
    def play(self,e) -> int:
        col = int( input("Column: ") ) -1
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            print("Wrong column")
            self.play(e)


class ComputerRand(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)

    def play(self,e) -> int:
        col = random.randint(0, self.board.cols -1)
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            self.play(e) #Invalid column selected, try again
            

class ComputerDef(Player): #Defensive IA player
    def __init__(self, playernum: int, board: Board, checker: Checker):
        super().__init__(playernum, board, checker)
      
    def play(self,e) -> int:
        maxscore = 0
        selectedcolumn = 0
        
        # Tries to predict the other player's best move and 'steal' it:
        for col in range(self.board.cols):
            row = self.board.insert(col, -self.id, trial=True)
            if row != -1:
                trialscore = self.checker.checkgrid(-self.id, row, col)
                if trialscore > maxscore:
                    maxscore = trialscore
                    selectedcolumn = col
                
        col = selectedcolumn
        if maxscore < 2:
            col = random.randint(0, self.board.cols -1)
        row = self.board.insert(col, self.id)
        if row != -1:
            return self.checker.check4win(self.id, row, col)
        else:
            self.play(e) #Invalid column selected, try again

class PlayerDQN(Player):
    def __init__(self, playernum: int, board: Board, checker: Checker,repeat:int=1):
        super().__init__(playernum, board, checker)
        self.dqnagent = DQNAgent(self.board.cols*self.board.rows,self.board.cols,repeat)
        if os.path.isfile("./connectX-weights_deep.h5"):
            self.dqnagent.load("./connectX-weights_deep.h5") # load prelearned weights
        self.batch_size = 10
        self.total_rewards = 0
        self.all_total_rewards = np.empty(repeat)
        self.all_avg_rewards = np.empty(repeat)
        self.previous = None
        self.previous_action = None
        #self.dqnagent = DQNAgent(42,7,1)

    def play(self,e):
        #ouvrir fichier
        export = open("statistics.txt", "a")

        previous_state = self.board.grid.copy()
        action = self.dqnagent.act(self.board.grid)
        self.previous_action = action
        row = self.board.insert(action, self.id)
        if row != -1:
            (next_state,reward,done)= self.checker.check4win(self.id, row, action)
            self.previous = next_state.copy()
            self.dqnagent.memorize(previous_state, action, reward, next_state.copy(),done)
            self.total_rewards += reward

            if len(self.dqnagent.memory) > self.batch_size:
                self.dqnagent.replay(self.batch_size)
                self.all_total_rewards[e] = self.total_rewards
                avg_reward = self.all_total_rewards[max(0, e - 3):e].mean()
                self.all_avg_rewards[e] = avg_reward
                if e % 3 == 0 :
                    self.dqnagent.save("./connectX-weights_deep.h5")
                    print("episode: {}/{}, epsilon: {:.2f}, average: {:.2f}".format(e, self.dqnagent.episodes, self.dqnagent.epsilon, avg_reward))

                    # Saving stat to file:
                    export.write("episode: {}/{}, epsilon: {:.2f}, average: {:.2f}\n".format(e, self.dqnagent.episodes, self.dqnagent.epsilon, avg_reward))

                    self.dqnagent.memory.clear()
                    self.dqnagent.load("./connectX-weights_deep.h5")
                export.close

        else:
            export.close
            print("Colonne pleine:     ",self.total_rewards)
            print("Winner :", -self.id)
            # We penalize this AI hard when trying to play in a full column
            # Instead of letting it play again (like the 2 other bots), 
            # we end the current game and set it as that game's loser.
            self.board.keepplaying = False
            self.board.winner = -self.id

    def send_reward(self,reward):
            self.dqnagent.memorize(self.previous, self.previous_action, reward, self.board.grid.copy(),True)
            self.total_rewards += reward

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
        self.episodes = episodes
    
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(20, input_dim=self.state_size, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr = 0.00001))
        return model

    def _build_model2(self):
        # Second Neural Net for Deep-Q learning Model (Work in progress)
        model = Sequential()
        model.add(Dense(20, input_dim=self.state_size, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',optimizer=Adam(lr = 0.00001))
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
                target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape(1,-1))[0])
            target_f = self.model.predict(state.reshape(1,-1))
            target_f[0][action] = target
            self.model.fit(state.reshape(1,-1), target_f, epochs=1, verbose=0)#################################reshape##########
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)
    
    def save(self, name):
        self.model.save_weights(name)
