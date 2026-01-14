import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



bullet_list =[]
enemy_list = []


grid_size= 500
player_speed= 5
enemy_spead= .1
max_missed_bullet=10
bullet_speed= 10

camera_height= 150.0
camera_angle =0.0
first_persion_camera_mode =False

player_position=[0,0]
player_rotation_angle=90.0
player_life_counter=5
game_score_conter=0
missed_bullets_conter=0
game_over_flag =False
player_fall_angle =0


cheat_mode_flag =False
cheat_camera_view =False

########camera/view setup function#########


def camera_setup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1.25, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_persion_camera_mode:
        if cheat_mode_flag and cheat_camera_view:
            # V key active: Camera FIXED at a good viewing position
            # Camera positioned in front and to the side of player, looking at player
            gluLookAt(
                player_position[0] + 50, 80, player_position[1] + 50,  # Camera position (front-right, elevated)
                player_position[0], 35, player_position[1],  # Look at player center
                0, 1, 0
            )
        else:
            # Normal first-person: Camera rotates WITH player
            r = math.radians(player_rotation_angle)
            gluLookAt(
                player_position[0] + 6.50 * math.sin(r), 50, player_position[1] + 6.50 * math.cos(r),
                player_position[0] + 6.50 * math.sin(r) + 80 * math.sin(r), 50, player_position[1] + 6.50 * math.cos(r) + 80 * math.cos(r),
                0, 1, 0
            )
    else:
        r = math.radians(camera_angle)
        gluLookAt(
            350 * math.sin(r), camera_height, 350 * math.cos(r),
            0, 0, 0,
            0, 1, 0
        )


def draw_bounddary_wall():
    wall_h = 60

    glColor3f(0,1,0)
    glBegin(GL_QUADS)
    glVertex3f(grid_size,0,-grid_size)
    glVertex3f(grid_size,0,grid_size)
    glVertex3f(grid_size,wall_h,grid_size)
    glVertex3f(grid_size,wall_h,-grid_size)
    glEnd()


    glColor3f(0,0.8,0.8)
    glBegin(GL_QUADS)
    glVertex3f(-grid_size,0,-grid_size)
    glVertex3f(grid_size,0,-grid_size)
    glVertex3f(grid_size,wall_h,-grid_size)
    glVertex3f(-grid_size,wall_h,-grid_size)
    glEnd()


    glColor3f(0,0,1)
    glBegin(GL_QUADS)
    glVertex3f(-grid_size,0,-grid_size)
    glVertex3f(-grid_size,0,grid_size)
    glVertex3f(-grid_size,wall_h,grid_size)
    glVertex3f(-grid_size,wall_h,-grid_size)
    glEnd()


    # glColor3f(1,1,0)
    # glBegin(GL_QUADS)
    # glVertex3f(-grid_size,0,grid_size)
    # glVertex3f(grid_size,0,grid_size)
    # glVertex3f(grid_size,wall_h,grid_size)
    # glVertex3f(-grid_size,wall_h,grid_size)
    # glEnd()


def draw_grid_floor():
    tile_size = 30
    for i in range(-grid_size,1000,tile_size):
        for j in range(-grid_size,grid_size,tile_size):
            if (i//tile_size + j//tile_size) % 2 == 0:
                glColor3f(1,1,1)
            else:
                glColor3f(0.8,0.7,1.0)
            glBegin(GL_QUADS)
            glVertex3f(i,0,j)
            glVertex3f(i+tile_size,0,j)
            glVertex3f(i+tile_size,0,j+tile_size)
            glVertex3f(i,0,j+tile_size)
            glEnd()


def draw_player():
    glPushMatrix()
    #  player movement and rotation
    glTranslatef(player_position[0], 25, player_position[1])
    glRotatef(player_rotation_angle, 0, 1, 0)
    if game_over_flag:
        glRotatef(player_fall_angle, 1, 0, 0)
    q = gluNewQuadric()
    
    # body
    glColor3f(0.35, 0.48, 0.28)
    glPushMatrix()
    glTranslatef(0, 8, 0)
    glScalef(2.3, 3.1, 1.5)
    glutSolidCube(10)
    glPopMatrix()
    
    # head
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 26, 0)
    gluSphere(q, 7.5, 22, 22)
    glPopMatrix()
    
    # neck/torso
    glColor3f(0.68, 0.72, 0.68)
    glPushMatrix()
    glTranslatef(0, 13, 10)
    gluCylinder(q, 4.2, 4.2, 19, 18, 18)
    glTranslatef(0, 0, 19)
    gluCylinder(q, 3.8, 0, 6.5, 18, 18)
    glPopMatrix()
    
    # left arm
    glColor3f(0.98, 0.83, 0.72)
    glPushMatrix()
    glTranslatef(-11.5, 13, 5)
    gluCylinder(q, 4.2, 4.2, 16, 12, 12)
    glPopMatrix()
    
    # right arm
    glColor3f(0.98, 0.83, 0.72)
    glPushMatrix()
    glTranslatef(11.5, 13, 5)
    gluCylinder(q, 4.2, 4.2, 16, 12, 12)
    glPopMatrix()
    
    # left leg
    glColor3f(0, 0, 0.75)
    glPushMatrix()
    glTranslatef(-8.5, -3, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(q, 5.2, 5.2, 24, 12, 12)
    glPopMatrix()
    
    # right leg
    glPushMatrix()
    glTranslatef(8.5, -3, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(q, 5.2, 5.2, 24, 12, 12)
    glPopMatrix()
    
    glPopMatrix()



    
def draw_enemies():
    for e in enemy_list:
        glPushMatrix()
        glTranslatef(e['enemy_position'][0], e['enemy_position'][1], e['enemy_position'][2])
        glScalef(e['enemy_size'], e['enemy_size'], e['enemy_size'])
        q = gluNewQuadric()
        glColor3f(1, 0, 0)        
        body_radius = 10
        gluSphere(q, body_radius, 30, 30)
        glColor3f(0, 0, 0)      
        glPushMatrix()
        glTranslatef(0, body_radius + 5, 0) 
        gluSphere(q, 5, 20, 20)
        glPopMatrix()
        glPopMatrix()




def draw_gun():
    glPushMatrix()
    # --- follow player position ---
    glTranslatef(player_position[0], 25, player_position[1])
    # --- follow player rotation ---
    glRotatef(player_rotation_angle, 0, 1, 0)
    # --- optional: fall animation ---
    if game_over_flag:
        glRotatef(player_fall_angle, 1, 0, 0)
    # --- gun offset relative to player (right hand) ---
    glTranslatef(12, 10, -10)   # x = right, y = up, z = forward
    glRotatef(-10, 0, 1, 0)
    q = gluNewQuadric()

    # barrel
    glColor3f(0.7, 0.7, 0.7)
    gluCylinder(q, 2.5, 2.5, 30, 16, 16)

    # barrel tip
    glPushMatrix()
    glTranslatef(0, 0, 30)
    gluCylinder(q, 2.5, 0, 8, 16, 16)
    glPopMatrix()

    # left hand grip
    glColor3f(1, 0.85, 0.7)
    glPushMatrix()
    glTranslatef(3, -3, 5)
    gluSphere(q, 4, 16, 16)
    glPopMatrix()

    # right hand grip
    glPushMatrix()
    glTranslatef(-3, -3, 5)
    gluSphere(q, 4, 16, 16)
    glPopMatrix()

    glPopMatrix()



def draw_bullets():
    glColor3f(1,1,0)
    for k in bullet_list:
        glPushMatrix()
        glTranslatef(k['bullet_position'][0],k['bullet_position'][1],k['bullet_position'][2])
        glutSolidCube(4)
        glPopMatrix()



########## GAME INTIALIZATION FUNCTIONS #############
def reset_game():
    global player_position,player_rotation_angle,player_life_counter,game_score_conter,missed_bullets_conter,game_over_flag,player_fall_angle,cheat_mode_flag,cheat_camera_view
    player_rotation_angle = 90
    game_score_conter = 0
    missed_bullets_conter = 0
    player_position = [0,0]
    bullet_list.clear()
    enemy_list.clear()
    game_over_flag = False
    cheat_mode_flag = False 
    cheat_camera_view = False 
    player_life_counter = 5
    player_fall_angle = 0
    for i in range(5):
        spawn_enemy()



def spawn_enemy(i = None):
    global enemy_list
    new_enemy = {
        "enemy_position":[random.uniform(-grid_size,grid_size),10,random.uniform(-grid_size,grid_size)],
        "enemy_size":1.3,
        "size_direction":1
    }
    if i!=None and i<len(enemy_list):
        enemy_list[i] = new_enemy
    else:
        enemy_list.append(new_enemy)




############ INPUT HANDLERS #############
def keyboard_input(k, x, y):
    global player_rotation_angle, cheat_mode_flag, cheat_camera_view

    if game_over_flag:
        if k.lower() == b'r':
            reset_game()
        return

    r = math.radians(player_rotation_angle)
    nx = player_position[0]
    nz = player_position[1]

    key = k.lower() 

    if key == b'w':
        nx += player_speed * math.sin(r)
        nz += player_speed * math.cos(r)

    if key == b's':
        nx -= player_speed * math.sin(r)
        nz -= player_speed * math.cos(r)

    if -grid_size < nx < grid_size and -grid_size < nz < grid_size:
        player_position[0] = nx
        player_position[1] = nz

    if key == b'a':
        player_rotation_angle = (player_rotation_angle + 5) % 360

    if key == b'd':
        player_rotation_angle = (player_rotation_angle - 5) % 360

    if key == b'c':
        cheat_mode_flag = not cheat_mode_flag

    if key == b'v':
        if cheat_mode_flag:
            cheat_camera_view = not cheat_camera_view
        else:
            cheat_camera_view = False  # Auto-disable if cheat mode is off

def mouse_listner(b,s,x,y):
    global first_persion_camera_mode

    if not game_over_flag:
        if b==GLUT_LEFT_BUTTON and s==GLUT_DOWN:
            r = math.radians(player_rotation_angle)
            bullet_list.append({
                "bullet_position":[player_position[0] +36 * math.sin(r),37,player_position[1] + 36 * math.cos(r)],
                "bullet_direction":[math.sin(r),math.cos(r)],
                "timespan":100
            })
    if b==GLUT_RIGHT_BUTTON and s==GLUT_DOWN:
        first_persion_camera_mode = not first_persion_camera_mode


def special_key_input(k,x,y):
    global camera_height,camera_angle
    if k==GLUT_KEY_LEFT:
        camera_angle -= 2
    if k==GLUT_KEY_RIGHT:
        camera_angle += 2
    if k==GLUT_KEY_UP:
        camera_height += 3
    if k==GLUT_KEY_DOWN:
        camera_height -= 3
        if camera_height < 50:    
          camera_height = 50









########### MAIN LOOP FUNCTIONS/game logic #############
def update_bullets():
    global missed_bullets_conter
    rm = []
    for i, b in enumerate(bullet_list):
        b['bullet_position'][0] += b['bullet_direction'][0] * bullet_speed
        b['bullet_position'][2] += b['bullet_direction'][1] * bullet_speed
        b['timespan'] -= 1

        # Remove bullets that expire or go out of bounds
        if b['timespan'] <= 0 or not (-grid_size < b['bullet_position'][0] < grid_size and -grid_size < b['bullet_position'][2] < grid_size):
            rm.append(i)
            missed_bullets_conter += 1

    for i in sorted(rm, reverse=True):
        del bullet_list[i]


def update_enemies():
    for e in enemy_list:
        dx = player_position[0] - e['enemy_position'][0]
        dz = player_position[1] - e['enemy_position'][2]
        dist = math.sqrt(dx*dx + dz*dz)
        if dist != 0:
            e['enemy_position'][0] += dx / dist * enemy_spead
            e['enemy_position'][2] += dz / dist * enemy_spead

        # Enemy size oscillation
        e['enemy_size'] += e['size_direction'] * 0.02
        if e['enemy_size'] > 1.5 or e['enemy_size'] < 0.5:
            e['size_direction'] *= -1


def handle_bullet_enemy_collisions():
    global game_score_conter
    rm = []
    respawn_indices = []

    for i, b in enumerate(bullet_list):
        for j, e in enumerate(enemy_list):
            if j in respawn_indices:
                continue
            dist = math.sqrt((b['bullet_position'][0] - e['enemy_position'][0])**2 +
                             (b['bullet_position'][2] - e['enemy_position'][2])**2)
            if dist < 10 * e['enemy_size']:
                if i not in rm:
                    rm.append(i)
                respawn_indices.append(j)
                game_score_conter += 1

    # Remove hit bullets
    for i in sorted(rm, reverse=True):
        if i < len(bullet_list):
            del bullet_list[i]

    # Respawn hit enemies
    for j in set(respawn_indices):
        spawn_enemy(j)


def handle_player_enemy_collisions():
    global player_life_counter, game_over_flag
    hit_indices = []

    for j, e in enumerate(enemy_list):
        dist = math.sqrt((player_position[0] - e['enemy_position'][0])**2 +
                         (player_position[1] - e['enemy_position'][2])**2)
        if dist < 20:
            player_life_counter -= 1
            hit_indices.append(j)
            if player_life_counter <= 0:
                game_over_flag = True
                break

    if not game_over_flag:
        for j in set(hit_indices):
            spawn_enemy(j)


def cheat_mode_actions():
    if not cheat_mode_flag or game_over_flag:
        return

    global player_rotation_angle
    player_rotation_angle = (player_rotation_angle + 2) % 360

    for e in enemy_list:
        dx = e['enemy_position'][0] - player_position[0]
        dz = e['enemy_position'][2] - player_position[1]
        angle_to_enemy = math.degrees(math.atan2(dx, dz)) % 360
        dif = abs(player_rotation_angle - angle_to_enemy)

        if min(dif, 360 - dif) < 5 and random.random() < 0.1:
            r = math.radians(player_rotation_angle)
            sx = player_position[0] + 36 * math.sin(r)
            sz = player_position[1] + 36 * math.cos(r)
            bullet_list.append({
                "bullet_position": [sx, 37, sz],
                "bullet_direction": [math.sin(r), math.cos(r)],
                "timespan": 100
            })


def idle():
    global game_over_flag, player_fall_angle

    if game_over_flag:
        if player_fall_angle < 90:
            player_fall_angle += 1
        glutPostRedisplay()
        return

    update_bullets()
    update_enemies()
    handle_bullet_enemy_collisions()
    handle_player_enemy_collisions()
    cheat_mode_actions()

    if missed_bullets_conter >= max_missed_bullet or player_life_counter <= 0:
        game_over_flag = True

    glutPostRedisplay()


########### MAIN DISPLAY/RENDERING FUNCTION #############

def writing_text(x,y,s,f = GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0,1000,0,800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x,y)
    for ch in s:
        glutBitmapCharacter(f,ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    camera_setup()
    draw_grid_floor()
    draw_bounddary_wall()

    draw_player()  
    
    # Only draw extra gun when in normal first-person (not cheat camera view)
    if first_persion_camera_mode and not (cheat_mode_flag and cheat_camera_view):
        draw_gun()  

    draw_enemies()
    draw_bullets()

    if not game_over_flag:
        writing_text(10,770,"Player Life Remaining: " + str(max(0,player_life_counter)))
        writing_text(10,740,"Game Score: " + str(game_score_conter))
        writing_text(10,710,"Player Bullet Missed: " + str(missed_bullets_conter))

    if game_over_flag:
        writing_text(10,770,"Game is Over. Your Score is " + str(game_score_conter) + ".",GLUT_BITMAP_HELVETICA_18)
        writing_text(10,740,'Press "R" to Restart the Game',GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()



############ MAIN FUNCTION #############
def main():
    glutInit()
    reset_game()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000,800)
    glutInitWindowPosition(100,100)
    glutCreateWindow(b"Bullet Frenzy")

    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard_input)
    glutSpecialFunc(special_key_input)
    glutMouseFunc(mouse_listner)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__=="__main__":
    main()



