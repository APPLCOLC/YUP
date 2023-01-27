import pygame


#The default bullet simply travels to the other side of the stage and then gets deleted.
#It also deletes itself if it touches a bullet.
class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("./assets/images/bullets/bananas.png"),(100,25)).convert_alpha()
    screen_rect = pygame.Rect(0,0,450,600)

    def __init__(self, sound=None, img=None, args={"center":(0,0)}):

        pygame.sprite.Sprite.__init__(self)
        self.health = 1

        if sound is not None:
            sound.play()

        self.rect = pygame.mask.from_surface(Bullet.image).get_rect()
        #This tells the bullet to spawn in the x coordinate of arg1 and the y coordinate of arg2.
        #These are, typically, fed with YUP's coordinates.
        self.rect.center = args["center"]

    def update(self):
    #Every frame, the bullet travels 15 pixels and deletes itself if it goes out of bounds.
        self.rect.y -= 15
        if not self.on_screen() or self.health <= 0: self.kill()   
    
    def on_screen(self) -> bool: return Bullet.screen_rect.colliderect(self.rect)  