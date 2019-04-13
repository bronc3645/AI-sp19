# PyAgent.py

import Action
import Orientation
import Search


class Agent:
    def __init__(self):
        self.agentHasGold = False
        self.actionList = []
        self.returnList=[]
        self.tovisit=[]
        self.visited=[]
        self.breezes=[]
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
        self.visited.append([1,1])

    # Input percept is a dictionary [perceptName: boolean]
    def Process(self, stench, breeze, glitter, bump, scream):
        self.getpit()
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
            self.returnList=self.searchEngine.FindPath([self.posx,self.posy],self.oritation,[1,1],self.oritation)
            self.returnList.append(Action.CLIMB)
            return Action.GRAB
        if(self.returnList):
            action=self.returnList.pop(0)
            self.track(action)
            return action
        elif (not self.actionList):
            if(bool(breeze)):
                if(not [self.posx,self.posy] in self.breezes):
                    self.breezes.append([self.posx,self.posy])
                if((not [self.posx+1,self.posy] in self.visited)and (not [self.posx+1,self.posy] in self.tovisit) and self.posx+1<=5):
                    self.searchEngine.RemoveSafeLocation(self.posx+1,self.posy)
                if((not [self.posx,self.posy+1] in self.visited)and (not [self.posx,self.posy+1] in self.tovisit) and self.posy+1<=5):
                    self.searchEngine.RemoveSafeLocation(self.posx, self.posy+1)
                if((not [self.posx-1,self.posy] in self.visited)and (not [self.posx-1,self.posy] in self.tovisit) and self.posx-1>=1):
                    self.searchEngine.RemoveSafeLocation(self.posx-1, self.posy)
                if((not [self.posx,self.posy-1] in self.visited)and (not [self.posx,self.posy-1] in self.tovisit) and self.posy-1>=1):
                    self.searchEngine.RemoveSafeLocation(self.posx, self.posy-1)
            elif(bool(stench)):
                if ((not [self.posx+1,self.posy] in self.visited)and (not [self.posx+1,self.posy] in self.tovisit) and self.posx + 1 <= 5):
                    self.searchEngine.RemoveSafeLocation(self.posx + 1, self.posy)
                if ((not [self.posx,self.posy+1] in self.visited)and (not [self.posx,self.posy+1] in self.tovisit) and self.posy + 1 <= 5):
                    self.searchEngine.RemoveSafeLocation(self.posx, self.posy + 1)
                if ((not [self.posx-1,self.posy] in self.visited)and (not [self.posx-1,self.posy] in self.tovisit) and self.posx - 1 >= 1):
                    self.searchEngine.RemoveSafeLocation(self.posx - 1, self.posy)
                if ((not [self.posx, self.posy - 1] in self.visited) and (not [self.posx,self.posy-1] in self.tovisit) and self.posy - 1 >= 1):
                    self.searchEngine.RemoveSafeLocation(self.posx, self.posy - 1)
            else:
                if (not [self.posx + 1, self.posy] in self.searchEngine.explored and self.posx+1<=4):
                    self.searchEngine.AddSafeLocation(self.posx+1,self.posy)
                    if(not [self.posx+1,self.posy]in self.tovisit):
                        self.tovisit.append([self.posx + 1, self.posy])
                if (not [self.posx - 1, self.posy] in self.searchEngine.explored and self.posx-1>=1):
                    self.searchEngine.AddSafeLocation(self.posx-1,self.posy)
                    if (not [self.posx - 1, self.posy] in self.tovisit):
                        self.tovisit.append([self.posx - 1, self.posy])
                if (not [self.posx, self.posy+1] in self.searchEngine.explored and self.posy+1<=4):
                    self.searchEngine.AddSafeLocation(self.posx,self.posy+1)
                    if (not [self.posx, self.posy+1] in self.tovisit):
                        self.tovisit.append([self.posx, self.posy+1])
                if (not [self.posx, self.posy-1] in self.searchEngine.explored and self.posy-1>=1):
                    self.searchEngine.AddSafeLocation(self.posx,self.posy-1)
                    if (not [self.posx, self.posy-1] in self.tovisit):
                        self.tovisit.append([self.posx, self.posy-1])
            if(self.tovisit):
                self.pos=self.tovisit.pop(0)
                self.actionList+=self.searchEngine.FindPath([self.posx,self.posy],self.oritation,self.pos,self.oritation)
            else:
                self.pos=[1,1]
                self.actionList+=self.searchEngine.FindPath([self.posx,self.posy],self.oritation,[1,1],self.oritation)
                self.actionList.append(Action.CLIMB)
        print(str(self.pos))
        print(str(self.posx)+":x")
        print(str(self.posy)+":y")
        print(str(self.oritation)+":oritation")
        self.printworld()
        if(self.actionList):
            action = self.actionList.pop(0)
        else:
            self.actionList+=self.searchEngine.FindPath([self.posx,self.posy],self.oritation,[1,1],self.oritation)
            self.actionList.append(Action.CLIMB)
            action=self.actionList.pop(0)
        self.track(action)
        if(not[self.posx,self.posy]in self.visited):
            self.visited.append([self.posx,self.posy])
        self.check()
        return action

    def printworld(self):
        print("visited")
        for x in self.visited:
            print(str(x))
        print("to visit")
        for x in self.tovisit:
            print(str(x))
    def getpit(self):
        pits=[]
        for i in self.breezes:
            print("breezes: "+str(i))
            x = i.pop(0)
            y=i.pop(0)
            print("x: "+str(x)+" y: "+str(y))
            if ((not [x+1,y] in self.visited) and (not [x+1,y] in self.tovisit) and x+1<=4):
                pits.append([x+1,y])
            if ((not [x-1,y] in self.visited) and (not [x-1,y] in self.tovisit) and x-1>=1):
                pits.append([x-1,y])
            if ((not [x,y+1] in self.visited) and (not [x,y+1] in self.tovisit) and y+1<=4):
                pits.append([x,y+1])
            if ((not [x,y-1] in self.visited) and (not [x,y-1] in self.tovisit) and y-1>=1):
                pits.append([x, y-1])
            i.append(x)
            i.append(y)

        for x in pits:
            print("possible pits: "+str(x))

    def check(self):
        for x in self.tovisit:
            if(x in self.visited):
                self.tovisit.remove(x)
    def track(self,action):
        if (action == Action.GOFORWARD):
            if (self.oritation == Orientation.RIGHT):
                self.posx += 1
            elif (self.oritation == Orientation.LEFT):
                self.posx -= 1
            elif (self.oritation == Orientation.UP):
                self.posy += 1
            elif (self.oritation == Orientation.DOWN):
                self.posy -= 1
        if (action == Action.TURNRIGHT):
            if (self.oritation == Orientation.RIGHT):
                self.oritation = Orientation.DOWN
            elif (self.oritation == Orientation.LEFT):
                self.oritation = Orientation.UP
            elif (self.oritation == Orientation.UP):
                self.oritation = Orientation.RIGHT
            elif (self.oritation == Orientation.DOWN):
                self.oritation = Orientation.LEFT
        if (action == Action.TURNLEFT):
            if (self.oritation == Orientation.RIGHT):
                self.oritation = Orientation.UP
            elif (self.oritation == Orientation.LEFT):
                self.oritation = Orientation.DOWN
            elif (self.oritation == Orientation.UP):
                self.oritation = Orientation.LEFT
            elif (self.oritation == Orientation.DOWN):
                self.oritation = Orientation.RIGHT
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
