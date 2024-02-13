import pypokedex
from hangulInputBox import *
import pandas as pd
from PIL import Image
import requests
import pygame
import os, sys, time


pygame.init()

pygame.display.set_caption("Pokedex")
title_icon = pygame.image.load("./assets/pokedex_icon.png")  
pygame.display.set_icon(title_icon) 

width, height = 700, 600
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))

running = True
start_screen = True
main_screen = False
rotation = False
flash = False

name_kr = ''
pokemon_front_img_load = False
pokemon_back_img_load = False
pokemon_name_load = False

type_dic = {'normal':'노말', 'fire':'불꽃', 'water':'물', 'electric':'전기', 'grass':'풀', 'ice':'얼음', 'fighting':'격투', 'poison':'독', 'ground':'땅', 'flying':'비행', 'psychic':'에스퍼', 'bug':'벌레', 'ghost':'고스트', 'dark':'악', 'dragon':'드래곤', 'steel':'강철', 'fairy':'페어리'}
type_color_dic = {'노말':'255, 255, 255', '불꽃':'225, 127, 0', '물':'0, 127, 255', '전기':'247, 230, 0', '풀':'0, 141, 98', '얼음':'80, 188, 223', '격투':'193, 58, 14', '독':'147, 112, 219', '땅':'198, 138, 18', '비행':'121, 159, 191', '에스퍼':'255, 51, 153', '벌레':'128, 128, 0', '고스트':'75, 0, 130', '악':'72, 61, 139', '드래곤':'83, 83, 236', '강철':'102, 102, 102', '페어리':'128, 0, 128'}


def rotation_animation(): # 포켓볼 회전 애니메이션 함수
    global rotation
    global flash

    original_background = screen.copy()
    offset = pygame.math.Vector2(0, 0)
    icon_rect.x, icon_rect.y = 700, 62
    angle = 200
    angle_speed = 19.27
    move_speed = 8

    for i in range(28):
        screen.blit(original_background, (0, 0)) 

        offset_rotated = offset.rotate(angle)
        icon_rect.x -= move_speed # 이동
        img = pygame.transform.rotozoom(pokeball_icon, angle, 1) # 회전
        rect = img.get_rect(center= icon_rect.center + offset_rotated) # offset 계산

        screen.blit(img, rect)
        angle += angle_speed

        time.sleep(0.05)
        pygame.display.flip()

    rotation = False
    flash = True

    clock.tick(60)


def name_load_animation(dex, name): # 포켓몬 이름 출력 애니메이션
    global pokemon_dex_name_text
    global pokemon_name_load
    while True:
        pokemon_dex_name_text = str(dex) + " - " + name
        if pk_current_index < len(pokemon_dex_name_text): # 한글자 씩 출력
                pokemon_text = pokemon_text_font_rate.render(text[:pk_current_index + 1], True, (255, 255, 255))
                pk_current_index += 1
        elif pk_current_index == len(pokemon_dex_name_text):
            break

    screen.fill((0, 0, 0))

    screen.blit(pokemon_text, pokemon_text_rect)
    pygame.time.delay(typing_speed)

    pokemon_name_load = False


def flash_effect(duration=900, fade_duration=400): # 플래시 이펙트
    global flash

    start_time = pygame.time.get_ticks()

    original_background = screen.copy()

    while pygame.time.get_ticks() - start_time < duration:

        elapsed_time = pygame.time.get_ticks() - start_time

        if elapsed_time < duration - fade_duration:
            alpha = 255
        else:
            alpha = int(255 * (duration - elapsed_time) / fade_duration)


        screen.blit(original_background, (0, 0)) 


        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        color = (255, 255, 255, alpha)
        pygame.draw.rect(surface, color, (0, 0, width, height))
        screen.blit(surface, (0, 0))


        pygame.display.flip()

        clock.tick(60)

    flash = False


path = "./assets"
df = pd.read_csv(os.path.join(path, "poke_names.csv"))

# Pokedex 로고
label_text_font_size = int(width/10)
text = "Pokedex"
label_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), label_text_font_size)
label_text = label_text_font_rate.render("", True, (255, 255, 255))
label_text_rect = (225, 30)
typing_speed = 200  # 글자당 표시 시간 (밀리초)
current_index = 0  # 현재까지 표시된 글자의 인덱스

# 포켓볼
pokeball_icon = pygame.image.load(os.path.join(path, "pokeball.png"))
pokeball_icon = pygame.transform.scale(pokeball_icon, (width * 1/28, height * 1/28))
icon_width, icon_height = pokeball_icon.get_size()
icon_rect = pokeball_icon.get_rect()

# 리셋 아이콘
reset_icon = pygame.image.load(os.path.join(path, "reset.png"))
reset_icon = pygame.transform.scale(reset_icon, (width * 1/20, height * 1/20))
reset_icon_width, reset_icon_height = reset_icon.get_size()
reset_icon_rect = pygame.Rect((10, 10), (icon_width, icon_height))

# 안내문
warning_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), int(width/43))
warning_text = warning_text_font_rate.render("한/영 전환 토글 키 [Left-Shift + Space]", True, (255, 255, 255))
warning_text_rect = (8, 580)

# 검색창
box = HangulInputBox(os.path.join(path, "font.ttf"), 20, 8,'white', 'black')

# 포켓몬 이름
pokemon_text_font_size = int(width/30)
pokemon_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), pokemon_text_font_size)
pokemon_text = pokemon_text_font_rate.render("", True, (255, 255, 255))
pokemon_text_rect = (50, 390)
pk_typing_speed = 125  # 글자당 표시 시간 (밀리초)
pk_current_index = 0  # 현재까지 표시된 글자의 인덱스

# 타입
type_text_color = ["", ""]
type1_color = ()
type2_color = ()
type_text_1_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), int(width/35))
type_text_1 = type_text_1_font_rate.render("", True, [255, 255, 255])
type_text_1_rect = (420, 390)
type_text_2_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), int(width/35))
type_text_2 = type_text_2_font_rate.render("", True, [255, 255, 255])
type_text_2_rect = (490, 390)

# 능력치
hp_text_font_size = int(width/36)
hp_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), hp_text_font_size)
hp_text = hp_text_font_rate.render("", True, (255, 255, 255))

attack_text_font_size = int(width/36)
attack_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), attack_text_font_size)
attack_text = attack_text_font_rate.render("", True, (255, 255, 255))

defense_text_font_size = int(width/36)
defense_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), defense_text_font_size)
defense_text = defense_text_font_rate.render("", True, (255, 255, 255))

sp_attack_text_font_size = int(width/36)
sp_attack_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), sp_attack_text_font_size)
sp_attack_text = sp_attack_text_font_rate.render("", True, (255, 255, 255))

sp_defense_text_font_size = int(width/36)
sp_defense_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), sp_defense_text_font_size)
sp_defense_text = sp_defense_text_font_rate.render("", True, (255, 255, 255))

speed_text_font_size = int(width/36)
speed_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), speed_text_font_size)
speed_text = speed_text_font_rate.render("", True, (255, 255, 255))

ability_text_font_size = int(width/36)
ability_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), ability_text_font_size)
ability_text = ability_text_font_rate.render("", True, (255, 255, 255))

hidden_ability_text_font_size = int(width/36)
hidden_ability_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), hidden_ability_text_font_size)
hidden_ability_text = hidden_ability_text_font_rate.render("", True, (255, 255, 255))

weight_text_font_size = int(width/36)
weight_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), weight_text_font_size)
weight_text = weight_text_font_rate.render("", True, (255, 255, 255))

height_text_font_size = int(width/36)
height_text_font_rate = pygame.font.Font(os.path.join(path, "font.ttf"), height_text_font_size)
height_text = height_text_font_rate.render("", True, (255, 255, 255))


clock = pygame.time.Clock()

while running:
    keyEvent = None
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

        if i.type == pygame.MOUSEBUTTONDOWN:
            if reset_icon_rect.collidepoint(i.pos): # 리셋 버튼 클릭
                main_screen = False
                screen.fill((0, 0, 0))

                name_kr = ''
                pokemon_front_img_load = False
                pokemon_back_img_load = False
                pokemon_name_load = False
                pokemon_text = pokemon_text_font_rate.render('', True, (255, 255, 255))
                pk_name_kr = ''
                pk_name_en = ''
                pk_dex = ''
                pk_type = ''
                pk_hp = ''
                pk_attack = ''
                pk_defense = ''
                pk_sp_attack = ''
                pk_sp_defense = ''
                pk_speed = ''
                hp_text = hp_text_font_rate.render("", True, (255, 255, 255))
                attack_text = attack_text_font_rate.render("", True, (255, 255, 255))
                defense_text = defense_text_font_rate.render("", True, (255, 255, 255))
                sp_attack_text = sp_attack_text_font_rate.render("", True, (255, 255, 255))
                sp_defense_text = sp_defense_text_font_rate.render("", True, (255, 255, 255))
                speed_text = speed_text_font_rate.render("", True, (255, 255, 255))
                ability_text = ability_text_font_rate.render("", True, (255, 255, 255))
                hidden_ability_text = hidden_ability_text_font_rate.render("", True, (255, 255, 255))
                weight_text = weight_text_font_rate.render("", True, (255, 255, 255))
                height_text = height_text_font_rate.render("", True, (255, 255, 255))
                type_text_1 = type_text_1_font_rate.render("", True, (255, 255, 255))
                type_text_2 = type_text_2_font_rate.render("", True, (255, 255, 255))

                box = HangulInputBox(os.path.join(path, "font.ttf"), 20, 8,'white', 'black')

                main_screen = True

        if i.type == pygame.KEYDOWN:
            if i.mod == pygame.KMOD_LSHIFT and i.key == pygame.K_r: # 리셋 단축키 (LShift + R)
                main_screen = False
                screen.fill((0, 0, 0))

                name_kr = ''
                pokemon_front_img_load = False
                pokemon_back_img_load = False
                pokemon_name_load = False
                pokemon_text = pokemon_text_font_rate.render('', True, (255, 255, 255))
                pk_name_kr = ''
                pk_name_en = ''
                pk_dex = ''
                pk_type = ''
                pk_hp = ''
                pk_attack = ''
                pk_defense = ''
                pk_sp_attack = ''
                pk_sp_defense = ''
                pk_speed = ''
                hp_text = hp_text_font_rate.render("", True, (255, 255, 255))
                attack_text = attack_text_font_rate.render("", True, (255, 255, 255))
                defense_text = defense_text_font_rate.render("", True, (255, 255, 255))
                sp_attack_text = sp_attack_text_font_rate.render("", True, (255, 255, 255))
                sp_defense_text = sp_defense_text_font_rate.render("", True, (255, 255, 255))
                speed_text = speed_text_font_rate.render("", True, (255, 255, 255))
                ability_text = ability_text_font_rate.render("", True, (255, 255, 255))
                hidden_ability_text = hidden_ability_text_font_rate.render("", True, (255, 255, 255))
                weight_text = weight_text_font_rate.render("", True, (255, 255, 255))
                height_text = height_text_font_rate.render("", True, (255, 255, 255))
                type_text_1 = type_text_1_font_rate.render("", True, (255, 255, 255))
                type_text_2 = type_text_2_font_rate.render("", True, (255, 255, 255))

                box = HangulInputBox(os.path.join(path, "font.ttf"), 20, 8,'white', 'black')

                main_screen = True
            
            else:
                keyEvent = i

        if i.type == pygame.USEREVENT: # 포켓몬 이름 검색시
            if i.name == 'enterEvent': 
                name_kr = i.text
                
                if len(df.loc[df['name_ko'] == name_kr, 'name_en']) != 0: # 한글로 검색했을때
                    name_en = df.loc[df['name_ko'] == name_kr, 'name_en'].item()
                elif len(df.loc[df['name_en'] == name_kr, 'name_en']) != 0: # 영어로 검색했을때
                    name_en = df.loc[df['name_en'] == name_kr, 'name_en'].item()
                    print("영어")
                else:
                    continue

                p = pypokedex.get(name=name_en) # 영어 이름으로 검색
                
                pk_name_kr = name_kr
                pk_name_en = p.name
                pk_dex = p.dex
                pk_type = p.types
                pk_hp = p.base_stats.hp
                pk_attack = p.base_stats.attack
                pk_defense = p.base_stats.defense
                pk_sp_attack = p.base_stats.sp_atk
                pk_sp_defense = p.base_stats.sp_def
                pk_speed = p.base_stats.speed
                pk_weight = p.weight
                pk_height = p.height
                pk_current_index = 0
                pk_ability = p.abilities


                # 타입 한국어로 변환 + 색깔 반환
                for i in range(len(pk_type)):
                    pk_type[i] = type_dic.get(str(pk_type[i]))
                    type_text_color[i] =  type_color_dic.get(str(pk_type[i]))

                type_text_1 = type_text_1_font_rate.render(str(pk_type[0]), True, list(map(int, type_text_color[0].split(","))))
                if len(pk_type) == 2: # 타입이 2개라면
                    type_text_2 = type_text_2_font_rate.render(str(pk_type[1]), True, list(map(int, type_text_color[1].split(","))))
                else:
                    type_text_2 = type_text_2_font_rate.render("", True, (255, 255, 255))

                # 특성
                start_index = str(pk_ability[0]).find("'") + 1
                end_index = str(pk_ability[0]).find("'", start_index)
                extracted_part = str(pk_ability[0])[start_index:end_index]

                if len(pk_ability) == 2:
                    hd_start_index = str(pk_ability[1]).find("'") + 1
                    hd_end_index = str(pk_ability[1]).find("'", hd_start_index)
                    hd_extracted_part = str(pk_ability[1])[hd_start_index:hd_end_index]
                else: # 숨겨진 특성이 없을 때
                    hd_extracted_part = "없음"

                # 포켓몬 스프라이트
                front_img_url = p.sprites.front['default']
                pokemon_front_sprite = Image.open(requests.get(front_img_url, stream=True).raw).convert('RGBA')
                pokemon_front_sprite.save(os.path.join(path,"pokemon_front.png"),'PNG')

                pokemon_front_img = pygame.image.load(os.path.join(path,"pokemon_front.png"))
                front_img_width, front_img_height = pokemon_front_img.get_size()
                pokemon_front_img = pygame.transform.scale(pokemon_front_img, (front_img_width * 2, front_img_height * 2))
                pokemon_front_img_load = True

                back_img_url = p.sprites.back['default']
                pokemon_back_sprite = Image.open(requests.get(back_img_url, stream=True).raw).convert('RGBA')
                pokemon_back_sprite.save(os.path.join(path,"pokemon_back.png"),'PNG')

                pokemon_back_img = pygame.image.load(os.path.join(path,"pokemon_back.png"))
                back_img_width, back_img_height = pokemon_back_img.get_size()
                pokemon_back_img = pygame.transform.scale(pokemon_back_img, (back_img_width * 2, back_img_height * 2))
                pokemon_back_img_load = True

                # 능력치, 스펙, 특성
                hp_text = hp_text_font_rate.render("Hp : " + str(pk_hp), True, (255, 255, 255))
                attack_text = attack_text_font_rate.render("공격 : " + str(pk_attack), True, (255, 255, 255))
                defense_text = defense_text_font_rate.render("방어 : " + str(pk_defense), True, (255, 255, 255))
                sp_attack_text = sp_attack_text_font_rate.render("특수공격 : " + str(pk_sp_attack), True, (255, 255, 255))
                sp_defense_text = sp_defense_text_font_rate.render("특수방어 : " + str(pk_sp_defense), True, (255, 255, 255))
                speed_text = speed_text_font_rate.render("스피드 : " + str(pk_speed), True, (255, 255, 255))
                ability_text = ability_text_font_rate.render("특성 : " + extracted_part.replace("'", ""), True, (255, 255, 255))
                hidden_ability_text = hidden_ability_text_font_rate.render("숨겨진 특성 : " + hd_extracted_part.replace("'", ""), True, (255, 255, 255))
                height_text = height_text_font_rate.render("키 : " + str(pk_height / 10) + "m", True, (255, 255, 255))
                weight_text = weight_text_font_rate.render("몸무게 : " + str(pk_weight / 10) + "kg", True, (255, 255, 255))


    mouse_x, mouse_y = pygame.mouse.get_pos()


    if start_screen == True:
        # Pokedex 글자 출력 애니메이션
        if current_index < len(text): # 한글자 씩 출력
            label_text = label_text_font_rate.render(text[:current_index + 1], True, (255, 255, 255))
            current_index += 1
        elif current_index == len(text):
            rotation = True

        screen.fill((0, 0, 0))

        screen.blit(label_text, label_text_rect)
        pygame.time.delay(typing_speed)

        # 포켓볼 회전 애니메이션
        if rotation == True:
            rotation_animation()

        # 플래시 애니메이션
        if flash == True:
            time.sleep(0.3)
            flash_effect()
            original_background = screen.copy()
            start_screen = False
            main_screen = True

        pygame.display.flip()



    elif main_screen == True:
        screen.fill((0, 0, 0))
        screen.blit(label_text, label_text_rect)
        screen.blit(pokeball_icon, (476, 62))

        screen.blit(warning_text, warning_text_rect)

        # reset 아이콘
        if reset_icon_rect.collidepoint(mouse_x, mouse_y):
                zoomed_icon = pygame.transform.scale(reset_icon, (int(reset_icon_width * 1.1), int(reset_icon_height * 1.1)))
        else:
            zoomed_icon = reset_icon

        screen.blit(zoomed_icon, (10, 10))


        # 포켓몬 이름 입력 받는 칸
        namebar_surface = pygame.Surface((180, 35))
        namebar_surface.fill((0, 0, 0))
        pygame.draw.rect(namebar_surface, (255, 255, 255), (0, 0, 180, 35), 2)
        screen.blit(namebar_surface, (50, 120))

        box.update(keyEvent)
        screen.blit(box.image, (55, 127))

        # 포켓몬 스프라이트
        if pokemon_front_img_load == True and pokemon_back_img_load == True:
            screen.blit(pokemon_front_img, (100, 170))
            screen.blit(pokemon_back_img, (400, 170))
            pokemon_name_load = True


        # 포켓몬 이름
        if pokemon_name_load == True:
            pokemon_dex_name_text = "No." + str(pk_dex) + " - " + pk_name_kr + " [" + pk_name_en + "]"

            if pk_current_index < len(pokemon_dex_name_text): # 한글자 씩 출력
                    pokemon_text = pokemon_text_font_rate.render(pokemon_dex_name_text[:pk_current_index + 1], True, (255, 255, 255))
                    pk_current_index += 1
            elif pk_current_index == len(pokemon_dex_name_text):
                pokemon_name_load = False

            screen.blit(pokemon_text, pokemon_text_rect)
            pygame.time.delay(pk_typing_speed)

        screen.blit(pokemon_text, pokemon_text_rect)
        

        if pokemon_name_load == False:
            # 포켓몬 타입
            screen.blit(type_text_1, type_text_1_rect)
            screen.blit(type_text_2, type_text_2_rect)

            # 포켓몬 인적사항
            screen.blit(hp_text, (50, 430))
            screen.blit(attack_text, (50, 452))
            screen.blit(defense_text, (50, 474))
            screen.blit(sp_attack_text, (50, 496))
            screen.blit(sp_defense_text, (50, 518))
            screen.blit(speed_text, (50, 540))
            screen.blit(ability_text, (400, 430))
            screen.blit(hidden_ability_text, (400, 452))
            screen.blit(height_text, (400, 496))
            screen.blit(weight_text, (400, 518))


        pygame.display.flip()


    clock.tick(60)


pygame.quit()
sys.exit()