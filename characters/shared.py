import pygame,random

#IMAGES
class SHARECHAR():
    hats = {
        "sunglasses":pygame.image.load("./assets/images/SHARED/HATS/SunglassHat.png").convert_alpha(),
        "owo": pygame.image.load("./assets/images/SHARED/HATS/OwOHat.png").convert_alpha(),
        "hardhat": pygame.image.load("./assets/images/SHARED/HATS/HardHat.png").convert_alpha(),
        "eye": pygame.image.load("./assets/images/SHARED/HATS/EyeHat.png").convert_alpha(),
        "void": pygame.image.load("./assets/images/SHARED/HATS/VoidHat.png").convert_alpha()
    }
    deathPop=[];deathBoom=[]
    for i in range(3):deathPop.append(pygame.transform.scale(pygame.image.load("./assets/images/SHARED/POP/Death_Pop-"+(str(i+1))+".png"),(60,60)).convert_alpha()) #creates,resizes,and appends
    for i in range(17):deathBoom.append(pygame.image.load("./assets/images/SHARED/BOOM/Death_Explosion-" + str(i+1) + ".png").convert_alpha()) #creates, doesn't resize
    hurtBullet=pygame.image.load("./assets/images/bullets/hurtBullet.png").convert_alpha()

#UNIVERSAL SPRITES
class charHat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        pass
class diePop(pygame.sprite.Sprite):
    def __init__(self,coordCENTER=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = SHARECHAR.deathPop[self.index]
        self.rect = self.image.get_rect(); self.rect.center = coordCENTER
        self.frame_counter = 0
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= 6:
            self.index += 1
            self.frame_counter = 0
        if self.index>2:
            self.index=0
            self.kill()
        self.image = SHARECHAR.deathPop[self.index]
class dieBoom(pygame.sprite.Sprite):
    def __init__(self,coordCENTER=(0,0),size=None):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = SHARECHAR.deathBoom[self.index]
        self.rect = self.image.get_rect(); self.rect.center = coordCENTER
        self.frame_counter = 0
        self.size=size
        self.coordCENTER=coordCENTER
    def update(self):
        self.frame_counter += 1

        if self.frame_counter >= 1:
            self.index += 1
            self.frame_counter = 0

        if self.index>16:
            self.index=0
            self.kill()

        self.image = SHARECHAR.deathBoom[self.index]

        if self.size is not None:
            self.image=pygame.transform.scale(self.image,self.size)
        self.rect=self.image.get_rect()
        self.rect.center=self.coordCENTER


class Bullet (pygame.sprite.Sprite):

    image = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(image, "red", (5, 5), 5)
    screen_rect = pygame.Rect(0,0,450,600)
    
    def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2, speed: float = 5) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.direction = direction.normalize()
        self.speed = speed
        self.rect = Bullet.image.get_rect(center=self.pos)
        
    def update(self) -> None:
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        
        if not self.on_screen(): 
            # print("killed")
            self.kill()
        
    def on_screen(self) -> bool:
        return Bullet.screen_rect.colliderect(self.rect)

class Char(pygame.sprite.Sprite):
    #default image if unchanged
    image = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(image, "red", (15, 15), 15)
    
    def __init__(self,args :dict):
        #initializes sprite code
        pygame.sprite.Sprite.__init__(self)
        
        #TAKING ARGUMENTS
        self.groups = args["groups"]
        self.player = args["player"]
        self.level = args["level"]
        self.offset = args["offset"]

        #default character code
        self.state="enter" #current behavior patterns
        self.health=1 #Health for characters
        self.scorevalue=10 #Score given to player
        self.idlePos = [(args["formation_position"][0]+self.offset[0]),(args["formation_position"] [1]+self.offset[1])] # current position in idle
        

        #IMAGE CODE
        self.animation_frame=0
        self.animation_frame_counter=0
        self.image = Char.image
        self.rect = self.image.get_rect()
    
        #SHOOT CODE    
        self.shoot_times = [] #the maximum amount will be like 10, which would only be achieved after level 100 or so
        #shoot times are not generated by default

        #STATE CODE
        self.frames_in_state = 0 #counter for states. reset at the end of every state, but risen every frame, whether used or not.

        #entrance code
        #[put entrance code here]


    def update(self):
        self.state_update()
        self.collision_update()
        self.animation_update()

    def animation_update(self):
        pass

    def state_update(self):
        if self.state=="enter": self.state_enter()
        if self.state=="idle_search": self.state_idle_search()
        if self.state=="idle": self.state_idle()
        if self.state=="attack": self.state_attack()
        if self.state=="return": self.state_return()

    def state_enter(self):
        #The entrance state will transition into the "idle search" state usually when the entrance animation is finished
        #"idle search" just drags the character slowly to the title screen 
        self.frames_in_state += 1
        if True: #change end condition later, just a default
            self.state = "idle_search"
            self.frames_in_state = 0

    def state_idle_search(self):
        self.frames_in_state += 1
        #Slowly dragging the character to the title screen
        horizontal_condition_met = abs(self.idlePos[0] - self.rect.center[0]) <= 10
        vertical_condition_met = abs(self.idlePos[1] - self.rect.center[1]) <= 10
        if not horizontal_condition_met or not vertical_condition_met:
            if not horizontal_condition_met:
                if self.idlePos[0] < self.rect.center[0]:
                    self.rect.x -= 5
                elif self.idlePos[0] > self.rect.center[0]:
                    self.rect.x += 5
            if not vertical_condition_met:
                if self.idlePos[1] < self.rect.center[1]:
                    self.rect.y -= 3
                elif self.idlePos[1] > self.rect.center[1]:
                    self.rect.y += 3
        else: 
            self.state = 'idle'
            self.frames_in_state = 0

    def state_idle(self):
        #this is the only state that does not have a frame counter
        #this is because it does not automatically exit
        self.rect.center=self.idlePos

    def state_attack(self):
        #same default as state_enter
        self.frames_in_state += 1
        if True: 
            self.frames_in_state = 0
            self.state = "return" 

    def state_return(self):
        self.frames_in_state += 1
        if True:
            self.frames_in_state = 0
            self.state = "idle_search" #or 'idle'  

    def collision_update(self):
        #collision with bullets. 
        bullet_hit = pygame.sprite.spritecollide(self, self.groups["bullet"], False, collided=pygame.sprite.collide_mask)
        for item in bullet_hit:
            #subtracts health
            item.health -= 1
            self.health -= 1
            if self.health < 1:
                #kill code
                self.groups["universal"].add(diePop(self.rect.center)) #death effect
                self.player.score += self.scorevalue #score rising
                self.state = "dead" #alerting death
                self.kill() #removing from sprite groups

    def formationUpdate(self,formationPos):
        #following formation
        self.idlePos = [
            (formationPos[0] + self.offset[0]),
            (formationPos[1] + self.offset[1])]

    def shoot(self):
        #default shoot
        pos,player_pos = pygame.Vector2(self.rect.center),pygame.Vector2(self.player.rect.center) #position arguments 
        bullet=Bullet(pos = pos , direction = (player_pos - pos))
        self.groups["universal"].add(bullet)
        self.groups["enemy"].add(bullet)
        del pos,player_pos
                         
    #picking shoot times for the first time
    def generate_shoot_times(level,starttime=1,endtime=45,bullet_cap=5):
        shoot_times = []
        min,max = level // 10 , 1 + level // 5
        if min > bullet_cap: min = bullet_cap
        if max > bullet_cap: max = bullet_cap
        for i in range(random.randint((level // 10), (1 + level // 5))):
            shoot_times.append(random.randint(starttime,endtime))
        shoot_times.sort()   
        return shoot_times
         

