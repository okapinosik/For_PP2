import pygame, sys, math
from datetime import datetime

pygame.init()
W, H = 1100, 750
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

WHITE, BLACK, GRAY, DARK_GRAY, BLUE = (255,255,255), (0,0,0), (220,220,220), (180,180,180), (0,120,215)
PALETTE = [(255,0,0), (255,192,203), (255,165,0), (255,255,0), (0,255,0), (0,191,255), (0,0,255), (128,0,128), (0,0,0), (255,255,255)]
TOOLS = ['brush', 'line', 'rectangle', 'square', 'circle', 'right_triangle', 'equilateral_triangle', 'rhombus', 'fill', 'text', 'erase']
SIZES = [(2, '1', 'S'), (5, '2', 'M'), (10, '3', 'L')]

def draw_shape(surf, mode, p1, p2, col, th):
    x1, y1, x2, y2 = *p1, *p2
    w, h = abs(x2-x1), abs(y2-y1)
    if mode == 'line': pygame.draw.line(surf, col, p1, p2, th)
    elif mode == 'rectangle': pygame.draw.rect(surf, col, (min(x1,x2), min(y1,y2), w, h), th)
    elif mode == 'square': 
        s = max(w, h)
        pygame.draw.rect(surf, col, (min(x1,x2), min(y1,y2), s, s), th)
    elif mode == 'circle': pygame.draw.circle(surf, col, p1, int(math.hypot(x2-x1, y2-y1)), th)
    elif mode in ['right_triangle', 'equilateral_triangle', 'rhombus']:
        pts = [(x1,y1), (x1,y2), (x2,y2)] if mode == 'right_triangle' else \
              [(x1,y1), (x1-h/1.73, y2), (x1+h/1.73, y2)] if mode == 'equilateral_triangle' else \
              [(x1+ (x2-x1)/2, y1), (x2, y1+(y2-y1)/2), (x1+(x2-x1)/2, y2), (x1, y1+(y2-y1)/2)]
        pygame.draw.polygon(surf, col, pts, th)
def flood_fill(surf, pos, fill_color):
    x, y = pos

    # Не заливаем панель инструментов
    if y < 80:
        return

    target_color = surf.get_at(pos)
    fill_color = pygame.Color(*fill_color)

    if target_color == fill_color:
        return

    width, height = surf.get_size()
    pixels = [pos]

    while pixels:
        x, y = pixels.pop()


        if x < 0 or x >= width or y < 80 or y >= height:
            continue

        if surf.get_at((x, y)) != target_color:
            continue
        
        surf.set_at((x, y), fill_color)

        pixels.append((x + 1, y))
        pixels.append((x - 1, y))
        pixels.append((x, y + 1))
        pixels.append((x, y - 1))
def main():
    canvas = pygame.Surface((W, H)); canvas.fill(WHITE)
    font, font_draw = pygame.font.SysFont("Arial", 12, bold=True), pygame.font.SysFont("Arial", 24)
    cur_col, cur_th, mode, drawing, active_text, text_in = BLACK, 2, 'brush', False, False, ""
    p1 = last_pos = (0,0)

    while True:
        screen.fill(WHITE); screen.blit(canvas, (0, 0))
        m_pos = pygame.mouse.get_pos()
        ctrl = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if ctrl and event.key == pygame.K_s:
                    pygame.image.save(canvas, f"img_{datetime.now().strftime('%M%S')}.png")
                if active_text:
                    if event.key == pygame.K_RETURN: 
                        canvas.blit(font_draw.render(text_in, True, cur_col), p1)
                        active_text, text_in = False, ""
                    elif event.key == pygame.K_BACKSPACE: text_in = text_in[:-1]
                    else: text_in += event.unicode
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    cur_th = SIZES[int(event.unicode)-1][0]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if m_pos[1] < 80: 
                    for i, c in enumerate(PALETTE):
                        if pygame.Rect(10+(i%5)*35, 10+(i//5)*25, 30, 20).collidepoint(m_pos): cur_col = c
                    for i, m in enumerate(TOOLS):
                        if pygame.Rect(200+(i%6)*45, 10+(i//6)*32, 42, 28).collidepoint(m_pos): 
                            mode, active_text = m, False
                    for i, (val, key, lbl) in enumerate(SIZES):
                        if pygame.Rect(500 + i * 50, 10, 45, 45).collidepoint(m_pos): cur_th = val
                else:
                    p1 = last_pos = m_pos
                    if mode == 'text': active_text, text_in = True, ""
                    elif mode == 'fill':
                        flood_fill(canvas, event.pos, cur_col)
                    else: drawing = True

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    if mode not in ['brush', 'erase']: draw_shape(canvas, mode, p1, m_pos, cur_col, cur_th)
                    drawing = False
            
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'brush': 
                    pygame.draw.line(canvas, cur_col, last_pos, m_pos, cur_th); last_pos = m_pos
                elif mode == 'erase': pygame.draw.circle(canvas, WHITE, m_pos, 20)

        if drawing and mode not in ['brush', 'erase']: draw_shape(screen, mode, p1, m_pos, cur_col, cur_th)
        if active_text: screen.blit(font_draw.render(text_in + "|", True, cur_col), p1)
        
        pygame.draw.rect(screen, GRAY, (0, 0, W, 80))
        pygame.draw.line(screen, BLACK, (0, 80), (W, 80), 2)
        
        for i, c in enumerate(PALETTE):
            r = pygame.Rect(10+(i%5)*35, 10+(i//5)*25, 30, 20)
            pygame.draw.rect(screen, c, r)
            if c == cur_col: pygame.draw.rect(screen, BLACK, r, 2)
        
        for i, m in enumerate(TOOLS):
            r = pygame.Rect(200+(i%6)*45, 10+(i//6)*32, 42, 28)
            pygame.draw.rect(screen, BLUE if mode == m else DARK_GRAY, r, border_radius=4)
            txt = font.render(m[:5].upper(), True, WHITE if mode == m else BLACK)
            screen.blit(txt, txt.get_rect(center=r.center))

        for i, (val, key, lbl) in enumerate(SIZES):
            r = pygame.Rect(500 + i * 50, 10, 45, 45)
            pygame.draw.rect(screen, BLUE if cur_th == val else DARK_GRAY, r, border_radius=22)
            txt = font.render(lbl, True, WHITE)
            screen.blit(txt, txt.get_rect(center=r.center))

        pygame.display.flip(); clock.tick(120)

if __name__ == "__main__": main()