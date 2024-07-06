def main(screen_width, screen_height):
    global player_pos, player_health, score, monsters, attacking, monsters_slain, wave_count, cooldown_start_time, cooldown_active
    global sword_durability, sword_max_durability, sword_regeneration_rate, sword_pos, sword_pos_offset

    # Initialize player
    player_pos = [screen_width // 2, screen_height - 2 * player_size]
    player_health = 500
    score = 0
    monsters = []
    attacking = False
    monsters_slain = 0

    # Initialize sword
    sword_durability = 1000
    sword_max_durability = 1000
    sword_regeneration_rate = 1
    sword_pos_offset = [40, -80]
    sword_pos = [0, 0]

    display_wave_number(wave_count)
    pygame.display.flip()
    pygame.time.delay(3000)

    game_active = True
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_size:
            player_pos[1] += player_speed

        if keys[pygame.K_SPACE]:
            attacking = True
            sword_pos = [player_pos[0] + sword_pos_offset[0], player_pos[1] + sword_pos_offset[1]]
            for monster in monsters:
                monster_rect = pygame.Rect(monster['pos'][0], monster['pos'][1], monster_size, monster_size)
                if pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(monster_rect):
                    monsters.remove(monster)
                    score += 1
                    monsters_slain += 1
                    sword_durability -= monster_damage
                    if sword_durability <= 0:
                        sword_durability = 0
                    sword_pos = [player_pos[0] + sword_pos_offset[0], player_pos[1] + sword_pos_offset[1]]

        else:
            attacking = False

        if sword_durability < sword_max_durability:
            sword_durability += sword_regeneration_rate

        if cooldown_active:
            if pygame.time.get_ticks() - cooldown_start_time > cooldown_time * 1000:
                cooldown_active = False
                wave_count += 1
                monsters_defeated = 0

                # Spawn healer at the end of the wave
                healer_pos = [random.randint(0, screen_width - healer_size), random.randint(0, screen_height - healer_size)]

        if not cooldown_active:
            monster_spawn_timer += 1
            if monster_spawn_timer >= monster_spawn_rate:
                monster_spawn_timer = 0
                spawn_monster()

        # Check for healer collision and heal player
        if pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(pygame.Rect(*healer_pos, healer_size, healer_size)):
            player_health += healer_health_restore
            if player_health > 500:
                player_health = 500

        if not update_monster_positions():
            game_active = False

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))

        for monster in monsters:
            pygame.draw.rect(screen, RED, (*monster['pos'], monster_size, monster_size))

        if attacking:
            screen.blit(sword_img, sword_pos)

        draw_health_bar(player_health, 10, 10, 200, 20, "Player Health")
        draw_sword_health_bar(sword_durability, sword_max_durability, 10, 40, 200, 20, "Sword Durability")
        draw_healer()
        display_monsters_slain(monsters_slain)

        pygame.display.flip()

        # Game over condition
        if player_health <= 0:
            game_active = False
            game_over_screen(score)

    wait_for_keypress()

if __name__ == "__main__":
    main(screen_width, screen_height)
