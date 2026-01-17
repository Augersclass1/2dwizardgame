import pygame
import sys
import random
import math
#run with python c:/Users/felix/OneDrive/Desktop/2dwizardgame/2dminecraft.py

# =====================
# INITIAL SETUP
# =====================
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("wizard open world game")

clock = pygame.time.Clock()
FPS = 60

# =====================
# CONSTANTS
# =====================
TILE_SIZE = 40
CHUNK_SIZE = 16

AIR = 0
DIRT_TILE = 1
STONE_TILE = 2

WHITE = (255, 255, 255)
DIRT_COLOR = (139, 69, 19)
STONE_COLOR = (110, 110, 110)
PLAYER_COLOR = (0, 0, 255)
debug = False
selected_block = DIRT_TILE
# =====================
# WORLD STORAGE
# =====================
world = {}  # {(chunk_x, chunk_y): 2D tile list}
font = pygame.font.SysFont(None, 20)
def get_tile_from_mouse(cam_x, cam_y):
    mx, my = pygame.mouse.get_pos()
    world_x = mx + cam_x
    world_y = my + cam_y

    tile_x = world_x // TILE_SIZE
    tile_y = world_y // TILE_SIZE

    return int(tile_x), int(tile_y)
def draw_placement_preview(surface, cam_x, cam_y, player):
    tx, ty = get_tile_from_mouse(cam_x, cam_y)
    if not can_place(player, tx, ty):
        return

    rect = pygame.Rect(
        tx * TILE_SIZE - cam_x,
        ty * TILE_SIZE - cam_y,
        TILE_SIZE,
        TILE_SIZE,
    )

    pygame.draw.rect(surface, (0, 255, 0), rect, 2)

def place_block(tile_x, tile_y, block_type):
    
    cx = tile_x // CHUNK_SIZE
    cy = tile_y // CHUNK_SIZE

    chunk = get_chunk(cx, cy)

    lx = tile_x % CHUNK_SIZE
    ly = tile_y % CHUNK_SIZE

    if 0 <= lx < CHUNK_SIZE and 0 <= ly < CHUNK_SIZE:
        chunk[ly][lx] = block_type
def can_place(player, tile_x, tile_y, max_dist=5):
    px = player.rect.centerx // TILE_SIZE
    py = player.rect.centery // TILE_SIZE

    dx = tile_x - px
    dy = tile_y - py

    return dx * dx + dy * dy <= max_dist * max_dist

def get_height(global_x):
    # Controls
    base_height = 8
    hill_height = 2
    hill_width = 10  # bigger = smoother hills

    return int(
        8 +
        4 * math.sin(global_x / hill_width) +
        2 * math.sin(global_x / hill_height)
    )
def generate_chunk(cx, cy):
    tiles = [[AIR for _ in range(CHUNK_SIZE)] for _ in range(CHUNK_SIZE)]
    

    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            global_x = cx * CHUNK_SIZE + x
            global_y = cy * CHUNK_SIZE + y
            ground_height = get_height(global_x)
            if global_y > ground_height:
                if global_y > ground_height + 4:
                    tiles[y][x] = STONE_TILE if random.random() > 0.05 else DIRT_TILE
                else:
                   tiles[y][x] = STONE_TILE if random.random() < 0.35 else DIRT_TILE
 
            #ground_level += random.randint(-1,1)

    return tiles


def get_chunk(cx, cy):
    if (cx, cy) not in world:
        world[(cx, cy)] = generate_chunk(cx, cy)
    return world[(cx, cy)]


# =====================
# TILE COLLISION HELPERS
# =====================
def get_nearby_tiles(rect):
    tiles = []

    start_x = rect.left // TILE_SIZE - 1
    end_x = rect.right // TILE_SIZE + 1
    start_y = rect.top // TILE_SIZE - 1
    end_y = rect.bottom // TILE_SIZE + 1

    for ty in range(start_y, end_y):
        for tx in range(start_x, end_x):
            cx = tx // CHUNK_SIZE
            cy = ty // CHUNK_SIZE
            chunk = get_chunk(cx, cy)

            lx = tx % CHUNK_SIZE
            ly = ty % CHUNK_SIZE

            if 0 <= lx < CHUNK_SIZE and 0 <= ly < CHUNK_SIZE:
                if chunk[ly][lx] != AIR:
                    tiles.append(
                        pygame.Rect(
                            tx * TILE_SIZE,
                            ty * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE,
                        )
                    )
    return tiles


# =====================
# PLAYER
# =====================
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 30, 50)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x = -5
        if keys[pygame.K_RIGHT]:
            self.vel_x = 5
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = -12
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += 0.6
        if self.vel_y > 12:
            self.vel_y = 12

    def move(self):
        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0)

        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y)

    def collide(self, dx, dy):
        for tile in get_nearby_tiles(self.rect):
            if self.rect.colliderect(tile):
                if dx > 0:
                    self.rect.right = tile.left
                if dx < 0:
                    self.rect.left = tile.right
                if dy > 0:
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                if dy < 0:
                    self.rect.top = tile.bottom
                    self.vel_y = 0

    def draw(self, surface, cam_x, cam_y):
        pygame.draw.rect(
            surface,
            PLAYER_COLOR,
            pygame.Rect(
                self.rect.x - cam_x,
                self.rect.y - cam_y,
                self.rect.width,
                self.rect.height,
            ),
        )

def draw_debug(surface, player, cam_x, cam_y, clock):
    lines = [
        f"FPS: {int(clock.get_fps())}",
        f"Player X: {player.rect.x}",
        f"Player Y: {player.rect.y}",
        f"Chunk X: {player.rect.centerx // (TILE_SIZE * CHUNK_SIZE)}",
        f"Chunk Y: {player.rect.centery // (TILE_SIZE * CHUNK_SIZE)}",
        f"Loaded Chunks: {len(world)}",
    ]

    y = 10
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        surface.blit(text, (10, y))
        y += 18

# =====================
# RENDERING
# =====================
def draw_world(surface, cam_x, cam_y):
    start_x = cam_x // TILE_SIZE - 1
    end_x = (cam_x + WIDTH) // TILE_SIZE + 1
    start_y = cam_y // TILE_SIZE - 1
    end_y = (cam_y + HEIGHT) // TILE_SIZE + 1

    for ty in range(start_y, end_y):
        for tx in range(start_x, end_x):
            cx = tx // CHUNK_SIZE
            cy = ty // CHUNK_SIZE
            chunk = get_chunk(cx, cy)

            lx = tx % CHUNK_SIZE
            ly = ty % CHUNK_SIZE

            if 0 <= lx < CHUNK_SIZE and 0 <= ly < CHUNK_SIZE:
                tile = chunk[ly][lx]
                if tile == DIRT_TILE:
                    color = DIRT_COLOR
                elif tile == STONE_TILE:
                    color = STONE_COLOR
                else:
                    continue

                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(
                        tx * TILE_SIZE - cam_x,
                        ty * TILE_SIZE - cam_y,
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
                )


# =====================
# MAIN LOOP
# =====================
def main():
    player = Player()
    running = True

    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    global debug
                    debug = not debug
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    tx, ty = get_tile_from_mouse(cam_x, cam_y)
                    if can_place(player, tx, ty):
                        place_block(tx, ty, selected_block)


        player.handle_input()
        player.apply_gravity()
        player.move()

        cam_x = player.rect.centerx - WIDTH // 2
        cam_y = player.rect.centery - HEIGHT // 2

        screen.fill(WHITE)
        draw_world(screen, cam_x, cam_y)
        player.draw(screen, cam_x, cam_y)
        draw_placement_preview(screen, cam_x, cam_y, player)
        if debug:
            draw_debug(screen, player, cam_x, cam_y, clock)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
