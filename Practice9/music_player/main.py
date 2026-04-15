import pygame
import sys
from player import MusicPlayer

SCREEN_WIDTH  = 1366
SCREEN_HEIGHT = 720
FPS           = 165

COLOR_BG        = (6,6,6)
COLOR_PANEL     = (3,  30,  50)
COLOR_ACCENT    = (255,255,255)
COLOR_WHITE     = (240, 240, 240)
COLOR_GRAY      = (150, 150, 170)
COLOR_DARK_GRAY = (80,  80,  100)
COLOR_RED       = (220, 60,  60)
COLOR_YELLOW    = (255, 220, 0)


def draw_progress_bar(screen, x, y, width, height, position_sec, color_fill, color_bg):
    
    pygame.draw.rect(screen, color_bg, (x, y, width, height), border_radius=6)
    
    fill = min(position_sec % 100, 100) / 100 * width
    if fill > 0:
        pygame.draw.rect(screen, color_fill, (x, y, int(fill), height), border_radius=6)
    pygame.draw.rect(screen, COLOR_GRAY, (x, y, width, height), 2, border_radius=6)


def draw_controls_legend(screen, font, x, y):
    controls = [
        ("P:", "Play"),
        ("S:", "Stop"),
        ("SPACE:", "Pause/Resume"),
        ("N:", "Next Track"),
        ("B:", "Previous Track"),
        ("Escape:", "Quit"),
    ]
    for i, (key, action) in enumerate(controls):
        col = x + (i % 2) * 500
        row = y + (i // 2) * 100
        key_surf  = font.render(key, True, COLOR_ACCENT)
        act_surf  = font.render(f"  {action}", True, COLOR_WHITE)
        screen.blit(key_surf, (col, row))
        screen.blit(act_surf, (col + key_surf.get_width(), row))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    font_title  = pygame.font.Font("C:/Users/ernur/Desktop/myproject/python_base/Practice9/music_player/ponts/circular-std-4.ttf", 40)
    font_track  = pygame.font.Font("C:/Users/ernur/Desktop/myproject/python_base/Practice9/music_player/ponts/circular-std-4.ttf", 26, )
    font_status = pygame.font.Font("C:/Users/ernur/Desktop/myproject/python_base/Practice9/music_player/ponts/circular-std-4.ttf", 22)
    font_info   = pygame.font.Font("C:/Users/ernur/Desktop/myproject/python_base/Practice9/music_player/ponts/circular-std-4.ttf", 18)

    player = MusicPlayer(music_folder="music")

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_SPACE:
                    player.pause_resume()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()


        player.update()

        screen.fill(COLOR_BG)

        
        title_surf = font_title.render("Music Player By okapinosik", True, COLOR_ACCENT)
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 45)))

        
        """ pygame.draw.line(screen, COLOR_DARK_GRAY, (0, 75), (SCREEN_WIDTH , 75), 2) """

        
        panel_rect = pygame.Rect(40, 100, SCREEN_WIDTH - 80, 130)
        pygame.draw.rect(screen, COLOR_PANEL, panel_rect, border_radius=30)

        if player.get_total_tracks() > 0:
            track_name = player.get_track_name()
            if len(track_name) > 38:
                track_name = track_name[:35] + "..."
            track_surf = font_track.render(track_name, True, COLOR_WHITE)
            screen.blit(track_surf, track_surf.get_rect(center=(SCREEN_WIDTH // 2, 125)))

            counter_str = f"Track {player.current_index + 1} / {player.get_total_tracks()}"
            counter_surf = font_info.render(counter_str, True, COLOR_GRAY)
            screen.blit(counter_surf, counter_surf.get_rect(center=(SCREEN_WIDTH // 2, 152)))


            pos = player.get_position_seconds()
            draw_progress_bar(screen, 70, 172, SCREEN_WIDTH - 140, 14,
                              pos, COLOR_ACCENT, COLOR_DARK_GRAY)


            pos_label = font_info.render(f"{pos // 60:02d}:{pos % 60:02d}", True, COLOR_GRAY)
            screen.blit(pos_label, (70, 190))
        else:
            no_tracks = font_track.render("No tracks found in folder", True, COLOR_RED)
            screen.blit(no_tracks, no_tracks.get_rect(center=(SCREEN_WIDTH // 2, 145)))

        
        status_surf = font_status.render(player.get_status(), True, COLOR_YELLOW)
        screen.blit(status_surf, status_surf.get_rect(center=(SCREEN_WIDTH // 2, 250)))

        pygame.draw.line(screen, COLOR_DARK_GRAY, (40, 272), (SCREEN_WIDTH - 40, 272), 2)

        
        legend_title = font_info.render("KEYBOARD CONTROLS", True, COLOR_GRAY)
        screen.blit(legend_title, (55, 285))
        draw_controls_legend(screen, font_info, 55, 310)

        pygame.draw.line(screen, COLOR_DARK_GRAY, (40, 550), (SCREEN_WIDTH - 40, 550), 2)

        """ hint_surf = font_info.render("Add files to the music folder", True, COLOR_DARK_GRAY) """
        """ screen.blit(hint_surf, hint_surf.get_rect(center=(SCREEN_WIDTH // 2, 445))) """

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()