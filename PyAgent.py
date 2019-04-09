# PyAgent.py

import Action
import Orientation
import Search


class Agent:
    def __init__(self):
        self.agentHasGold = False
        self.actionList = []
        self.lotovisit=[]
        self.locvisted=[]
        self.frontier=[]
        self.known=[]
        self.searchEngine = Search.SearchEngine()
        self.oritation=Orientation.RIGHT
        self.posx=1
        self.posy=1
        self.wumpus=True
        self.pos=[]
    def Initialize(self):
        # Works only for test world.
        # You won't initially know safe locations or world size.
        self.searchEngine.AddSafeLocation(1,1)
        self.agentHasGold = False
        self.actionList = []
        self.locvisted.append([1,1])
        self.known.append([1,1,0,0])

    # Input percept is a dictionary [perceptName: boolean]
    def Process(self, stench, breeze, glitter, bump, scream):
        toreturn=Action.SHOOT
        if(bool(scream)):
            self.wumpus=False
        if(bool(bump)):
            if(self.oritation==Orientation.RIGHT):
                if(not self.posx==1):
                    self.posx-=1
            elif(self.oritation==Orientation.LEFT):
                if(not self.posx==4):
                    self.posx+=1
            elif(self.oritation==Orientation.UP):
                if(not self.posy==1):
                    self.posy-=1
            elif(self.oritation==Orientation.DOWN):
                if(not self.posy==4):
                    self.posy+=1
        if (bool(glitter)):
            self.actionList.append(Action.GRAB)
        elif (not self.actionList):
            if (not self.agentHasGold):
                if(bool(breeze)):
                    if(not [self.posx+1,self.posy] in self.locvisted and self.posx+1<=5):
                        self.searchEngine.RemoveSafeLocation(self.posx+1,self.posy)
                    if(not [self.posx,self.posy+1] in self.locvisted and self.posy+1<=5):
                        self.searchEngine.RemoveSafeLocation(self.posx, self.posy+1)
                    if(not [self.posx-1,self.posy] in self.locvisted and self.posx-1>=1):
                        self.searchEngine.RemoveSafeLocation(self.posx-1, self.posy)
                    if(not [self.posx,self.posy-1] in self.locvisted and self.posy-1>=1):
                        self.searchEngine.RemoveSafeLocation(self.posx, self.posy-1)
                elif(bool(stench)):
                    if (not [self.posx + 1, self.posy] in self.locvisted and self.posx + 1 <= 5):
                        self.searchEngine.RemoveSafeLocation(self.posx + 1, self.posy)
                    if (not [self.posx, self.posy + 1] in self.locvisted and self.posy + 1 <= 5):
                        self.searchEngine.RemoveSafeLocation(self.posx, self.posy + 1)
                    if (not [self.posx - 1, self.posy] in self.locvisted and self.posx - 1 >= 1):
                        self.searchEngine.RemoveSafeLocation(self.posx - 1, self.posy)
                    if (not [self.posx, self.posy - 1] in self.locvisted and self.posy - 1 >= 1):
                        self.searchEngine.RemoveSafeLocation(self.posx, self.posy - 1)
                else:
                    if (not [self.posx + 1, self.posy] in self.searchEngine.explored and self.posx+1<=4):
                        self.searchEngine.AddSafeLocation(self.posx+1,self.posy)
                        self.lotovisit.append([self.posx+1,self.posy])
                    if (not [self.posx - 1, self.posy] in self.searchEngine.explored and self.posx-1>=1):
                        self.searchEngine.AddSafeLocation(self.posx-1,self.posy)
                        self.lotovisit.append([self.posx - 1, self.posy])
                    if (not [self.posx, self.posy+1] in self.searchEngine.explored and self.posy+1<=4):
                        self.searchEngine.AddSafeLocation(self.posx,self.posy+1)
                        self.lotovisit.append([self.posx, self.posy+1])
                    if (not [self.posx, self.posy-1] in self.searchEngine.explored and self.posy-1>=1):
                        self.searchEngine.AddSafeLocation(self.posx,self.posy-1)
                        self.lotovisit.append([self.posx, self.posy-1])
                if(bool(glitter)):
                    self.actionList.clear()
                    self.actionList.append(Action.GRAB)
                elif(self.lotovisit):
                    self.pos=self.lotovisit.pop(0)
                    self.actionList+=self.searchEngine.FindPath([self.posx,self.posy],self.oritation,self.pos,self.oritation)
                else:
                    self.actionList+=self.searchEngine.FindPath([self.posx,self.posy],self.oritation,[1,1],self.oritation)
                    self.actionList.append(Action.CLIMB)
                if(not self.actionList):
                    self.actionList.append(Action.GOFORWARD)
            else:
                self.actionList += self.searchEngine.FindPath([self.posx,self.posy], self.oritation, [1, 1], Orientation.RIGHT)
                self.actionList.append(Action.CLIMB)
        print(str(self.pos))
        print(str(self.posx)+":x")
        print(str(self.posy)+":y")
        print(str(self.oritation)+":oritation")
        self.printworld()
        action = self.actionList.pop(0)
        if(action==Action.GOFORWARD):
            if(self.oritation==Orientation.RIGHT):
                self.posx+=1
            elif(self.oritation==Orientation.LEFT):
                self.posx-=1
            elif(self.oritation==Orientation.UP):
                self.posy+=1
            elif(self.oritation==Orientation.DOWN):
                self.posy-=1
        if(action==Action.TURNRIGHT):
            if (self.oritation == Orientation.RIGHT):
                self.oritation=Orientation.DOWN
            elif (self.oritation == Orientation.LEFT):
                self.oritation=Orientation.UP
            elif (self.oritation == Orientation.UP):
                self.oritation=Orientation.RIGHT
            elif (self.oritation == Orientation.DOWN):
                self.oritation=Orientation.LEFT
        if(action==Action.TURNLEFT):
            if (self.oritation == Orientation.RIGHT):
                self.oritation=Orientation.UP
            elif (self.oritation == Orientation.LEFT):
                self.oritation=Orientation.DOWN
            elif (self.oritation == Orientation.UP):
                self.oritation=Orientation.LEFT
            elif (self.oritation == Orientation.DOWN):
                self.oritation=Orientation.RIGHT
        if(action==Action.GRAB):
            self.agentHasGold=True
        if(not[self.posx,self.posy]in self.locvisted):
            self.locvisted.append([self.posx,self.posy])
        return action
    def printworld(self):
        for x in self.locvisted:
            print(str(x))
    def GameOver(self, score):
        pass


# Global agent
myAgent = 0


def PyAgent_Constructor():
    global myAgent
    myAgent = Agent()


def PyAgent_Destructor():
    global myAgent
    # nothing to do here


def PyAgent_Initialize():
    global myAgent
    myAgent.Initialize()


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    global myAgent
    return myAgent.Process(stench, breeze, glitter, bump, scream)


def PyAgent_GameOver(score):
    global myAgent
    myAgent.GameOver(score)
