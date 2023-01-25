import pygame,random
from characters import shared

 
class Char(shared.Char):

    #loading images
    idle,chomp = [],[]
    for i in range(3):
        idle.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/FIHS/FIHS-"+str(i+1)+".png"),(40,40)).convert_alpha())
    for i in range(4):
        chomp.append(pygame.transform.scale(pygame.image.load("./assets/images/characters/FIHS/FIHS-"+str(i+4)+".png"),(40,40)).convert_alpha())

    def __init__(self,args :dict):
        
        shared.Char.__init__(self,args)
        
        self.scorevalue = 200

        #PIRAHNA-SPECIFIC CODE
        self.player = args["player"] #THIS is to get positions for when the sprite is in attack state
        self.direction = "right"
        self.x_momentum = 0

        #IMAGE CODE
        self.image = Char.chomp[self.animation_frame]
        self.rect = self.image.get_rect()

        self.rect.center = (0,0)
        #the entrance state will move in a cubic function, although x won't move 


    def animation_update(self):
        #FRAME UPDATING
        self.animation_frame_counter += 1

        if self.animation_frame_counter >= 6:  # updates frame if enough time has passed
            self.animation_frame_counter = 0
            self.animation_frame += 1

            if self.state=="idle" or self.state=="enter":
                #RESETTING FRAME
                if self.animation_frame >= len(Char.idle) - 1: self.animation_frame = 0
                #SETTING IMAGE
                self.image = Char.idle[self.animation_frame]

            elif self.state == "attack" or self.state == "return":
                #RESETTING FRAME
                if self.animation_frame >= len(Char.chomp) - 1: self.animation_frame = 0
                #SETTING IMAGE
                self.image = Char.chomp[self.animation_frame]
                #FLIPPING IMAGE BASED ON DIRECTION
                if self.direction=="left": self.image=pygame.transform.flip(self.image,True,False)

    def state_enter(self):
        #jump down code
        self.frames_in_state += 1

        self.rect.center = (
            self.idlePos[0],
            (-0.125*(self.frames_in_state-100) )**3 + 590
        )
        # print(self.rect.center)

        if (30)>(self.idlePos[1]-self.rect.center[1])>(-30):
            self.rect.center = self.idlePos
            self.frames_in_state = 0
            self.state = "idle"

    def state_attack(self):
        self.rect.center = (
            self.rect.center[0],
            (-1/9) * ( (self.frames_in_state - 60) **2) + 475
        )

        #changing direction
        if (self.player.rect.x-self.rect.x)>10 and abs(self.x_momentum)<2:
            self.x_momentum+=0.1
            self.direction="right"
        elif (self.player.rect.x-self.rect.x)<-10 and abs(self.x_momentum)<2:
            self.x_momentum-=0.1
            self.direction = "left"
        #moving
        self.rect.x+=self.x_momentum

        #CHANGING STATE TO RETURN STATE
        if self.frames_in_state >= 120: #ends early to show the character turning around and coming back
            self.x_momentum = 0
            self.frames_in_state = 0
            self.state="idle_search" #return state does nothing now, as it is a parabola function
        
        #updating frame
        self.frames_in_state += 1

   