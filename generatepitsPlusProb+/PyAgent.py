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
        self.pits=[]
        self.lowest=1
        self.lolocation=[]

    def Initialize(self):
        # Works only for test world.
        # You won't initially know safe locations or world size.
        self.searchEngine.AddSafeLocation(1,1)
        self.agentHasGold = False
        self.actionList = []
        self.visited.append([1,1])

    # Input percept is a dictionary [perceptName: boolean]
    def Process(self, stench, breeze, glitter, bump, scream):
        if (bool(breeze)):
            if (not [self.posx, self.posy] in self.breezes):
                self.breezes.append([self.posx, self.posy])
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

        for i in self.breezes:
            print("breezes: " + str(i))
            x = i[0]
            y = i[1]
            # print("x: "+str(x)+" y: "+str(y))
            if ((not [x + 1, y] in self.visited) and (not [x + 1, y] in self.tovisit) and (not [x + 1, y] in self.breezes) and (
            not [x + 1, y] in self.pits) and x + 1 <= 4):
                self.pits.append([x + 1, y])
            if ((not [x - 1, y] in self.visited) and (not [x - 1, y] in self.tovisit) and (not [x - 1, y] in self.breezes) and (
            not [x - 1, y] in self.pits) and x - 1 >= 1):
                self.pits.append([x - 1, y])
            if ((not [x, y + 1] in self.visited) and (not [x, y + 1] in self.tovisit) and (not [x, y + 1] in self.breezes) and (
            not [x, y + 1] in self.pits) and y + 1 <= 4):
                self.pits.append([x, y + 1])
            if ((not [x, y - 1] in self.visited) and (not [x, y - 1] in self.tovisit) and (not [x, y - 1] in self.breezes) and (
            not [x, y - 1] in self.pits) and y - 1 >= 1):
                self.pits.append([x, y - 1])

        for x in self.pits:
            print("possible pits: " + str(x))
        if len(self.pits) >= 3:
            self.getProb()

    def getProb(self):
        num = 0.00
        denom = 0.00
        pit = .2
        noPit = .8
        num=[]
        denom=[]
        itteration=0

        temp_breeze = list(self.breezes)
        for i in self.pits:
            x=i[0]
            y=i[1]
            if ([x + 1, y] in temp_breeze):
                temp_breeze.remove([x + 1, y])

            if ([x - 1, y] in temp_breeze):
                temp_breeze.remove([x - 1, y])

            if ([x, y + 1] in temp_breeze):
                temp_breeze.remove([x, y + 1])

            if ([x, y - 1] in temp_breeze):
                temp_breeze.remove([x, y - 1])

            if (temp_breeze.__len__() == 0):
                num.append( pit * (noPit ** (len(self.pits)-4)))
                denom.append( pit * (noPit ** (len(self.pits)-4)))
                itteration+=1
            else:
                num.append(0)
                denom.append(0)
            # print("nums: "+str(len(num)))

            temp_breeze = list(self.breezes)

        # 2 trues
        itteration=0
        for i in self.pits:
            x=i[0]
            y=i[1]
            for o in self.pits:
                x2=o[0]
                y2=o[1]
                if(not x==x2 and not y==y2):
                    if ([x + 1, y] in temp_breeze):
                        temp_breeze.remove([x + 1, y])
                    if ([x2 + 1, y2] in temp_breeze):
                        temp_breeze.remove([x2 + 1, y2])
                    if ([x - 1, y] in temp_breeze):
                        temp_breeze.remove([x - 1, y])
                    if ([x2 - 1, y2] in temp_breeze):
                        temp_breeze.remove([x2 - 1, y2])
                    if ([x, y - 1] in temp_breeze):
                        temp_breeze.remove([x, y - 1])
                    if ([x2, y2 - 1] in temp_breeze):
                        temp_breeze.remove([x2, y2 - 1])
                    if ([x, y + 1] in temp_breeze):
                        temp_breeze.remove([x, y + 1])
                    if ([x2, y2 + 1] in temp_breeze):
                        temp_breeze.remove([x2, y2 + 1])
                    if len(temp_breeze) == 0:
                        num[itteration] += (pit ** 2) * (noPit ** (len(self.pits)-2))
                        denom[itteration] += (pit ** 2) * (noPit ** (len(self.pits)-2))
                    temp_breeze = list(self.breezes)
            itteration+=1

        # 3 trues
        itteration=0
        for i in self.pits:
            x=i[0]
            y=i[1]
            for o in self.pits:
                x2=o[0]
                y2=o[0]
                if (not x == x2 and not y == y2):
                    for n in self.pits:
                        x3=n[0]
                        y3=n[1]
                        if (not x == x3 and not y == y3 and not x2 == x3 and y2 == y3):
                            if [x - 1, y] in temp_breeze:
                                temp_breeze.remove([x - 1, y])
                            if [x2 - 1, y2] in temp_breeze:
                                temp_breeze.remove([x2 - 1, y2])
                            if [x3 - 1, y3] in temp_breeze:
                                temp_breeze.remove([x3 - 1, y3])

                            if [x + 1, y] in temp_breeze:
                                temp_breeze.remove([x + 1, y])
                            if [x2 + 1, y2] in temp_breeze:
                                temp_breeze.remove([x2 + 1, y2])
                            if [x3 + 1, y3] in temp_breeze:
                                temp_breeze.remove([x3 + 1, y3])

                            if [x, y - 1] in temp_breeze:
                                temp_breeze.remove([x, y - 1])
                            if [x2, y2 - 1] in temp_breeze:
                                temp_breeze.remove([x2, y2 - 1])
                            if [x3, y3 - 1] in temp_breeze:
                                temp_breeze.remove([x3, y3 - 1])

                            if [x, y + 1] in temp_breeze:
                                temp_breeze.remove([x, y + 1])
                            if [x2, y2 + 1] in temp_breeze:
                                temp_breeze.remove([x2, y2 + 1])
                            if [x3, y3 + 1] in temp_breeze:
                                temp_breeze.remove([x3, y3 + 1])

                            if len(temp_breeze) == 0:
                                num[itteration] += pit ** 3 * noPit ** (len(self.pits)-3)
                                denom[itteration] += pit ** 3 * noPit ** (len(self.pits)-3)
                            # print("num3 " + str(num) + " DEnom " + str(denom))
                            temp_breeze = list(self.breezes)
            itteration+=1

        # 4 trues
        if len(self.pits) >= 4:
            itteration=0
            for i in self.pits:
                x = i[0]
                y = i[1]
                for o in self.pits:
                    x2 = o[0]
                    y2 = o[0]
                    if (not x == x2 and not y == y2):
                        for n in self.pits:
                            x3 = n[0]
                            y3 = n[1]
                            if(not x==x3 and not y==y3 and not x2==x3 and y2==y3):
                                for r in self.pits:
                                    x4=r[0]
                                    y4=r[1]
                                    if(not x==x4 and not y==y4 and not x2==x4 and not y2==y4 and not x3==x4 and not y3==y4):
                                        if [x - 1, y] in temp_breeze:
                                            temp_breeze.remove([x - 1, y])
                                        if [x2 - 1, y2] in temp_breeze:
                                            temp_breeze.remove([x2 - 1, y2])
                                        if [x3 - 1, y3] in temp_breeze:
                                            temp_breeze.remove([x3 - 1, y3])
                                        if [x4 - 1, y4] in temp_breeze:
                                            temp_breeze.remove([x4 - 1, y4])

                                        if [x + 1, y] in temp_breeze:
                                            temp_breeze.remove([x + 1, y])
                                        if [x2 + 1, y2] in temp_breeze:
                                            temp_breeze.remove([x2 + 1, y2])
                                        if [x3 + 1, y3] in temp_breeze:
                                            temp_breeze.remove([x3 + 1, y3])
                                        if [x4 + 1, y4] in temp_breeze:
                                            temp_breeze.remove([x4 + 1, y4])

                                        if [x, y - 1] in temp_breeze:
                                            temp_breeze.remove([x, y - 1])
                                        if [x2, y2 - 1] in temp_breeze:
                                            temp_breeze.remove([x2, y2 - 1])
                                        if [x3, y3 - 1] in temp_breeze:
                                            temp_breeze.remove([x3, y3 - 1])
                                        if [x4, y4 - 1] in temp_breeze:
                                            temp_breeze.remove([x4, y4 - 1])

                                        if [x, y + 1] in temp_breeze:
                                            temp_breeze.remove([x, y + 1])
                                        if [x2, y2 + 1] in temp_breeze:
                                            temp_breeze.remove([x2, y2 + 1])
                                        if [x3, y3 + 1] in temp_breeze:
                                            temp_breeze.remove([x3, y3 + 1])
                                        if [x4, y4 + 1] in temp_breeze:
                                            temp_breeze.remove([x4, y4 + 1])

                                        if len(temp_breeze) == 0:
                                            num[itteration] += pit ** 4 * noPit ** (len(self.pits)-4)
                                            denom[itteration] += pit ** 4 * noPit ** (len(self.pits)-4)
                                        # print("num3 " + str(num) + " DEnom " + str(denom))
                                        temp_breeze = list(self.breezes)
            itteration += 1

        #1 false 1 true
        itteration = 0
        for i in self.pits:
            x = i[0]
            y = i[1]
            for o in self.pits:
                x2 = o[0]
                y2 = o[1]
                if (not x == x2 and not y == y2):
                    if ([x2 + 1, y2] in temp_breeze):
                        temp_breeze.remove([x2 + 1, y2])

                    if ([x2 - 1, y2] in temp_breeze):
                        temp_breeze.remove([x2 - 1, y2])

                    if ([x2, y2 - 1] in temp_breeze):
                        temp_breeze.remove([x2, y2 - 1])

                    if ([x2, y2 + 1] in temp_breeze):
                        temp_breeze.remove([x2, y2 + 1])

                    if len(temp_breeze) == 0:
                        denom[itteration] += (pit ** 1) * noPit ** (len(self.pits)-1)
                    temp_breeze = list(self.breezes)
            itteration += 1

        # 1 false 2 trues
        itteration = 0
        for i in self.pits:
            x = i[0]
            y = i[1]
            for o in self.pits:
                x2 = o[0]
                y2 = o[0]
                if (not x == x2 and not y == y2):
                    for n in self.pits:
                        x3 = n[0]
                        y3 = n[1]
                        if (not x == x3 and not y == y3 and not x2 == x3 and y2 == y3):
                            if [x2 - 1, y2] in temp_breeze:
                                temp_breeze.remove([x2 - 1, y2])
                            if [x3 - 1, y3] in temp_breeze:
                                temp_breeze.remove([x3 - 1, y3])

                            if [x2 + 1, y2] in temp_breeze:
                                temp_breeze.remove([x2 + 1, y2])
                            if [x3 + 1, y3] in temp_breeze:
                                temp_breeze.remove([x3 + 1, y3])

                            if [x2, y2 - 1] in temp_breeze:
                                temp_breeze.remove([x2, y2 - 1])
                            if [x3, y3 - 1] in temp_breeze:
                                temp_breeze.remove([x3, y3 - 1])

                            if [x2, y2 + 1] in temp_breeze:
                                temp_breeze.remove([x2, y2 + 1])
                            if [x3, y3 + 1] in temp_breeze:
                                temp_breeze.remove([x3, y3 + 1])

                            if len(temp_breeze) == 0:
                                denom[itteration] += (pit ** 2) * noPit ** (len(self.pits)-2)

                            # print("num3 " + str(num) + " DEnom " + str(denom))
                            temp_breeze = list(self.breezes)
            itteration += 1

        # one false 3 true
        if len(self.pits) >= 4:
            itteration = 0
            for i in self.pits:
                x = i[0]
                y = i[1]
                for o in self.pits:
                    x2 = o[0]
                    y2 = o[0]
                    if (not x == x2 and not y == y2):
                        for n in self.pits:
                            x3 = n[0]
                            y3 = n[1]
                            if (not x == x3 and not y == y3 and not x2 == x3 and y2 == y3):
                                for r in self.pits:
                                    x4 = r[0]
                                    y4 = r[1]
                                    if (not x == x4 and not y == y4 and not x2 == x4 and not y2 == y4 and not x3 == x4 and not y3 == y4):
                                        if [x2 - 1, y2] in temp_breeze:
                                            temp_breeze.remove([x2 - 1, y2])
                                        if [x3 - 1, y3] in temp_breeze:
                                            temp_breeze.remove([x3 - 1, y3])
                                        if [x4 - 1, y4] in temp_breeze:
                                            temp_breeze.remove([x4 - 1, y4])

                                        if [x2 + 1, y2] in temp_breeze:
                                            temp_breeze.remove([x2 + 1, y2])
                                        if [x3 + 1, y3] in temp_breeze:
                                            temp_breeze.remove([x3 + 1, y3])
                                        if [x4 + 1, y4] in temp_breeze:
                                            temp_breeze.remove([x4 + 1, y4])


                                        if [x2, y2 - 1] in temp_breeze:
                                            temp_breeze.remove([x2, y2 - 1])
                                        if [x3, y3 - 1] in temp_breeze:
                                            temp_breeze.remove([x3, y3 - 1])
                                        if [x4, y4 - 1] in temp_breeze:
                                            temp_breeze.remove([x4, y4 - 1])

                                        if [x2, y2 + 1] in temp_breeze:
                                            temp_breeze.remove([x2, y2 + 1])
                                        if [x3, y3 + 1] in temp_breeze:
                                            temp_breeze.remove([x3, y3 + 1])
                                        if [x4, y4 + 1] in temp_breeze:
                                            temp_breeze.remove([x4, y4 + 1])

                                        if len(temp_breeze) == 0:
                                            denom[itteration] += (pit ** 3) * noPit ** (len(self.pits) - 3)
                                        # print("num3 " + str(num) + " DEnom " + str(denom))
                                        temp_breeze = list(self.breezes)
            itteration += 1
        # testing
        prob=1.0
        lolocation=[]
        for x in range(0,len(num)):
            top=num[x]
            bottom=denom[x]
            if(not bottom==0):
                ans=top/bottom
                if(prob>ans):
                    prob=ans
                    lolocation=self.pits[x]

        if(prob<.5):
            self.searchEngine.AddSafeLocation(lolocation[0],lolocation[1])
            if(not lolocation in self.tovisit):
                self.tovisit.append(lolocation)


    def check(self):
        for x in self.tovisit:
            if(x in self.visited):
                self.tovisit.remove(x)
            if(x in self.pits):
                self.pits.remove(x)
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
