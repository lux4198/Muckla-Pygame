import pygame, sys, random

pygame.init()

gravity = 1

pancake_objects = []

koriander_objects = []
koriander_ground_score = []

apfelmus_objects = []

pancake_score = 0 

screen = pygame.display.set_mode((620, 600))
clock = pygame.time.Clock()
game_font = pygame.font.Font(r'04B_19.ttf', 40)

Spawn_pancake = pygame.USEREVENT
pygame.time.set_timer(Spawn_pancake, 1000)

Spawn_Koriander = pygame.USEREVENT
pygame.time.set_timer(Spawn_Koriander, 1500)

def create_pancake(pancake_objects):
    xvariable = random.choice([100, 200, 300, 400, 550])
    rect = pancake_surface.get_rect(center = (xvariable, 0))
    pancake_objects.append(rect)
    return rect

def create_koriander(koriander_objects):
    xvariable = random.choice([50, 156, 265, 415, 500])
    rect = koriander_surface.get_rect(center = (xvariable, 0))
    koriander_objects.append(rect)
    return rect

def create_apfelmus(apfelmus_objects, muckla_staff_pos):
    rect = apfelmus_surface.get_rect(topright = muckla_staff_pos)
    apfelmus_objects.append(rect)
    return rect

def move_apfelmus(apfelmus_objects):
    for i in range(len(apfelmus_objects)):
        apfelmus_objects[i].centery -= 5

def display_apfelmus(apfelmus_objects):
    for i in range(len(apfelmus_objects)):
        screen.blit(apfelmus_surface, apfelmus_objects[i])

def check_koriander_collision(koriander_objects):
    for i in range(len(koriander_objects)):
        if muckla_colliderect.colliderect(koriander_objects[i]):
            return False
    return True

def check_koriander_ground(koriander_objects):
    for i in range(len(koriander_objects)):
        if koriander_objects[i].bottom >= 590:
            koriander_ground_score.append(i)

def check_koriander_apfelmus_collision(koriander_objects, apfelmus_objects):
    for i in range(len(koriander_objects)):
        for j in range(len(apfelmus_objects)):
            if koriander_objects[i].colliderect(apfelmus_objects[j]):
                return i, j
            

def check_pancake_collision(pancake_objects):
    for i in range(len(pancake_objects)):
        if muckla_colliderect.colliderect(pancake_objects[i]):
            pancake_objects.remove(pancake_objects[i])
            return True

def score_display(pancake_score):
    score_surface = game_font.render(str(int(pancake_score)),True,(255,255,255))
    score_rect = score_surface.get_rect(center = (300,50))
    screen.blit(score_surface, score_rect)



bg_surface = pygame.image.load(r'Muckla\bg.jpg').convert()
bg_surface = pygame.transform.scale(bg_surface, (620,600))

muckla_surface = pygame.image.load(r'Muckla\mucklaa.png')
muckla_surface = pygame.transform.scale(muckla_surface, (150, 200))
muckla_rect = muckla_surface.get_rect(bottom = (600))
muckla_colliderect = pygame.rect.Rect((0,0), (75, 150))

pancake_surface = pygame.image.load(r'Muckla\pancake.png')
pancake_surface = pygame.transform.scale(pancake_surface, (50, 20))
pancake_rect = pancake_surface.get_rect(center = (300,300))

koriander_surface = pygame.image.load(r'Muckla\koriander1.png')
koriander_surface = pygame.transform.scale(koriander_surface, (50,50))
koriander_rect = koriander_surface.get_rect(center = (310,300))

apfelmus_surface = pygame.image.load(r'Muckla\apfelmus.png')
apfelmus_surface = pygame.transform.scale(apfelmus_surface, (40,40))
apfelmus_rect = apfelmus_surface.get_rect(center = (300, 300))



while True:

    keys = pygame.key.get_pressed()

    pancake_movement = 2 * gravity

    koriander_movement = gravity

    muckla_staff_pos = muckla_rect.topright

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == Spawn_pancake:
            create_pancake(pancake_objects)
        
        if event.type == Spawn_Koriander:
            create_pancake(koriander_objects)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                create_apfelmus(apfelmus_objects, muckla_staff_pos)

    screen.blit(bg_surface, (0,0))

    # Muckla

    if keys[pygame.K_LEFT]:
        muckla_rect.centerx -= 5
        if muckla_rect.left <= -15:
            muckla_rect.left = -15
    elif keys[pygame.K_RIGHT]:
        muckla_rect.centerx += 5
        if muckla_rect.right >= 620:
            muckla_rect.right = 620
    
    # Apfelmus

    if len(apfelmus_objects) != 0:
        move_apfelmus(apfelmus_objects)
        display_apfelmus(apfelmus_objects)

    # Collision 
 
    if not check_koriander_collision(koriander_objects):
        pygame.quit()
        sys.exit()

    if check_pancake_collision(pancake_objects):
        pancake_score += 1

    if check_koriander_apfelmus_collision(koriander_objects, apfelmus_objects) != None:
        i = check_koriander_apfelmus_collision(koriander_objects, apfelmus_objects)[0]
        j = check_koriander_apfelmus_collision(koriander_objects, apfelmus_objects)[1]
        koriander_objects.remove(koriander_objects[i])
        apfelmus_objects.remove(apfelmus_objects[j])

    # Muckla 

    muckla_colliderect.midbottom = muckla_rect.midbottom
    screen.blit(muckla_surface, muckla_rect)

    # Pancake  
    
    for i in range(len(pancake_objects)):
        screen.blit(pancake_surface, pancake_objects[i])
        pancake_objects[i].centery += pancake_movement

    # Koriander 

    check_koriander_ground(koriander_objects)
    for i in koriander_ground_score:
        koriander_objects.remove(koriander_objects[koriander_ground_score[i]])
    koriander_ground_score.clear()

    for i in range(len(koriander_objects)):
        screen.blit(koriander_surface, koriander_objects[i])
        koriander_objects[i].centery += koriander_movement

    


    # Score 

    score_display(pancake_score)







    pygame.display.update()
    clock.tick(120)




pygame.quit()