import pygame
import sys
import random
import time

pygame.init()

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)
PURPLE = (120, 80, 230)

# 폰트 설정
capsule_font = pygame.font.Font('DNFBitBitv2.ttf', 25)
popup_font = pygame.font.Font(None, 36)

# 현재 모니터의 해상도를 얻어 화면 설정
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('행원제 아이티스 캡슐 뽑기 게임')

# 이미지 로드
machine_img = pygame.image.load('machine.jpg')
capsule_pink_img = pygame.image.load('capsule_pink.png')
capsule_purple_img = pygame.image.load('capsule_purple.png')
capsule_green_img = pygame.image.load('capsule_green.png')

# 머신 이미지 비율 축소
m_width, m_height = machine_img.get_size()
m_new_width = int(m_width / 5.5)
m_new_height = int(m_height / 5.5)
machine_img = pygame.transform.scale(machine_img, (m_new_width, m_new_height))

# 머신 이미지 중앙 배치
m_x = (screen_width - m_new_width) // 2
m_y = (screen_height - m_new_height) // 2

# 그리드 개수 설정
grid_rows = 7
grid_cols = 10

# 그리드 간격 설정
grid_margin_x = 4.7
grid_margin_y = 21.5

# 그리드 좌표 설정
grid_start_x = m_x + 599
grid_start_y = m_y + 87
grid_width = m_new_width - 655
grid_height = m_new_height - 170
cell_width = (grid_width - (grid_cols - 1) * grid_margin_x) // grid_cols
cell_height = (grid_height - (grid_rows - 1) * grid_margin_y) // grid_rows

# 현재 위치 설정
current_row = 0
current_col = 0

# 캡슐 배치 확률 설정
capsule_probabilities = {
    capsule_green_img: 0.4,
    capsule_pink_img: 0.2,
    capsule_purple_img: 0.4,
}

# 캡슐 이미지 리스트 생성
capsule_imgs = []
for capsule_img, prob in capsule_probabilities.items():
    capsule_imgs.extend([capsule_img] * int(prob * 100))

# 그리드에 배치할 캡슐 이미지 리스트 생성
grid_capsules = random.choices(capsule_imgs, k=grid_rows * grid_cols)

# 각 캡슐 이미지에 색상 매핑
capsule_colors = {
    capsule_green_img: GREEN,
    capsule_pink_img: PINK,
    capsule_purple_img: PURPLE,
}

# 선택된 캡슐 위치와 시간 저장 변수
selected_capsule = None
selection_time = None

# 모서리 테두리 그리기 함수
def draw_corner_rect(surface, color, rect, thickness):
    pygame.draw.line(surface, color, rect.topleft, (rect.topleft[0] + thickness * 6, rect.topleft[1]), thickness)
    pygame.draw.line(surface, color, rect.topleft, (rect.topleft[0], rect.topleft[1] + thickness * 6), thickness)
    pygame.draw.line(surface, color, rect.topright, (rect.topright[0] - thickness * 6, rect.topright[1]), thickness)
    pygame.draw.line(surface, color, rect.topright, (rect.topright[0], rect.topright[1] + thickness * 6), thickness)
    pygame.draw.line(surface, color, rect.bottomleft, (rect.bottomleft[0] + thickness * 6, rect.bottomleft[1]), thickness)
    pygame.draw.line(surface, color, rect.bottomleft, (rect.bottomleft[0], rect.bottomleft[1] - thickness * 6), thickness)
    pygame.draw.line(surface, color, rect.bottomright, (rect.bottomright[0] - thickness * 6, rect.bottomright[1]), thickness)
    pygame.draw.line(surface, color, rect.bottomright, (rect.bottomright[0], rect.bottomright[1] - thickness * 6), thickness)

# 팝업 창 그리기 함수
def draw_popup(surface, text, color, rect, font):
    pygame.draw.rect(surface, WHITE, rect)
    pygame.draw.rect(surface, color, rect, 2)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_col = (current_col - 1) % grid_cols
            elif event.key == pygame.K_RIGHT:
                current_col = (current_col + 1) % grid_cols
            elif event.key == pygame.K_UP:
                current_row = (current_row - 1) % grid_rows
            elif event.key == pygame.K_DOWN:
                current_row = (current_row + 1) % grid_rows
            elif event.key == pygame.K_RETURN:
                selected_capsule = (current_row, current_col)
                selection_time = time.time()  # 선택된 시간 저장

    # 화면 그리기
    screen.fill(WHITE)
    screen.blit(machine_img, (m_x, m_y))

    for row in range(grid_rows):
        for col in range(grid_cols):
            x = grid_start_x + col * (cell_width + grid_margin_x)
            y = grid_start_y + row * (cell_height + grid_margin_y)

            # 캡슐 이미지 배치
            capsule_img = grid_capsules[row * grid_cols + col]
            if capsule_img is not None:
                resized_capsule_img = pygame.transform.scale(capsule_img, (cell_width, cell_height))
                screen.blit(resized_capsule_img, (x, y))

                # 캡슐에 따른 색상으로 텍스트 생성 및 배치
                number = row * grid_cols + col + 1
                capsule_num_color = capsule_colors[capsule_img]
                capsule_num = capsule_font.render(str(number), True, capsule_num_color)
                capsule_num_rect = capsule_num.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                screen.blit(capsule_num, capsule_num_rect)

            # 현재 위치의 모서리 테두리 배치
            rect = pygame.Rect(x, y, cell_width, cell_height)
            if row == current_row and col == current_col:
                draw_corner_rect(screen, RED, rect, 3)

    if selected_capsule:
        # 선택된 캡슐의 행과 열 인덱스를 가져옴
        selected_row, selected_col = selected_capsule
        
        # 선택된 캡슐의 번호를 계산 (1부터 시작)
        selected_number = selected_row * grid_cols + selected_col + 1
        
        # 팝업 창의 위치와 크기를 설정
        popup_rect = pygame.Rect(screen_width // 2 - 200 , screen_height // 2 - 200 , 400, 400)
        
        # 팝업 창을 그리는 함수 호출
        draw_popup(screen, f'캡슐 선택: {selected_number}', RED, popup_rect, popup_font)
        
        # 선택된지 3초가 지났는지 확인
        if time.time() - selection_time >= 3:
            grid_capsules[selected_row * grid_cols + selected_col] = None  # 선택된 캡슐 제거
            selected_capsule = None  # 선택된 캡슐 초기화
            selection_time = None  # 선택 시간 초기화

    pygame.display.flip()

pygame.quit()
sys.exit()