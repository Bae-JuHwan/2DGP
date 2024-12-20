import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Sky
from menu import Menu

class Level:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()

		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.reset, self.player)

		# sky
		self.sky = Sky()

		# shop
		self.menu = Menu(self.player, self.toggle_shop, self)
		self.shop_active = False

		# music
		self.success = pygame.mixer.Sound('../audio/success.wav')
		self.success.set_volume(0.3)
		self.music = pygame.mixer.Sound('../audio/music.mp3')
		self.music.play(loops = -1)

	def setup(self):
		tmx_data = load_pygame('../data/map.tmx')

		# 그룹 생성
		self.floor_sprites = pygame.sprite.Group()  # 확장할 바닥 타일
		self.wall_sprites = pygame.sprite.Group()  # 고정된 벽 타일
		self.furniture_sprites = pygame.sprite.Group()

		# 바닥 타일
		for layer in ['HouseFloor']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				sprite = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.floor_sprites, LAYERS['house bottom'])
				self.floor_sprites.add(sprite)
				self.all_sprites.add(sprite)

		# 벽 타일
		for layer in ['HouseWalls']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				sprite = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.wall_sprites, LAYERS['house top'])
				self.wall_sprites.add(sprite)
				self.all_sprites.add(sprite)

		# 가구
		for layer in ['HouseFurnitureBottom', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				sprite = Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.furniture_sprites, LAYERS['house top'])
				self.furniture_sprites.add(sprite)
				self.all_sprites.add(sprite)

		# fence
		for x,y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

		# water
		water_frames = import_folder('../graphics/water')
		for x,y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

		# trees
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y),
				surf = obj.image,
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
				name = obj.name,
				player_add = self.player_add
			)

		# wildflowers
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		# collision tiles
		for x,y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		# player
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x, obj.y),
					group = self.all_sprites,
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer,
					toggle_shop = self.toggle_shop
				)

			if obj.name == 'Bed':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Trader':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def player_add(self, item):
		self.player.item_inventory[item] += 1
		self.success.play()

	def expand_house(self, expansion_factor):
		# 확장 크기 계산
		expansion_offset = TILE_SIZE * expansion_factor

		# 바닥 타일 확장
		new_floor_sprites = pygame.sprite.Group()
		for sprite in self.floor_sprites:
			x, y = sprite.rect.topleft

			# 기존 바닥 타일 삭제
			sprite.kill()

			# 확장된 바닥 영역 생성
			for i in range(expansion_factor + 1):  # x 방향 확장
				for j in range(expansion_factor + 1):  # y 방향 확장
					new_x = x + (i * TILE_SIZE)
					new_y = y + (j * TILE_SIZE)

					# 새로운 바닥 스프라이트 생성
					new_sprite = Generic(
						(new_x, new_y), sprite.image, [self.all_sprites, self.floor_sprites], sprite.z
					)
					new_floor_sprites.add(new_sprite)

		# 기존 바닥 그룹 비우기 및 새 바닥 추가
		self.floor_sprites.empty()
		self.floor_sprites.add(*new_floor_sprites)

		# 바닥의 확장된 외곽 경계 계산
		min_x = min(tile.rect.x for tile in self.floor_sprites)
		max_x = max(tile.rect.x for tile in self.floor_sprites) + TILE_SIZE
		min_y = min(tile.rect.y for tile in self.floor_sprites)
		max_y = max(tile.rect.y for tile in self.floor_sprites) + TILE_SIZE

		# 벽 타일 이동
		for sprite in self.wall_sprites:
			x, y = sprite.rect.topleft

			# 상단 벽 이동
			if y < min_y:
				sprite.rect.y = min_y - TILE_SIZE

			# 하단 벽 이동
			if y >= max_y:
				sprite.rect.y = max_y

			# 좌측 벽 이동
			if x < min_x:
				sprite.rect.x = min_x - TILE_SIZE

			# 우측 벽 이동
			if x >= max_x:
				sprite.rect.x = max_x

	def toggle_shop(self):
		self.shop_active = not self.shop_active

	def reset(self):
		# plants
		self.soil_layer.update_plants()

		#soil
		self.soil_layer.remove_water()

		# apples on the trees
		for tree in self.tree_sprites.sprites():
			for apple in tree.apple_sprites.sprites():
				apple.kill()
			tree.create_fruit()

		# sky
		self.sky.start_color = [255,255,255]

	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def run(self,dt):
		# drawing logic
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)

		# updates
		if self.shop_active:
			self.menu.update()
		else:
			self.all_sprites.update(dt)
			self.plant_collision()

		# weather
		self.overlay.display()

		# daytime
		self.sky.display(dt)

		# transition overlay
		if self.player.sleep:
			self.transition.play()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)

					# if sprite == player:
					# 	pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
					# 	hitbox_rect = player.hitbox.copy()
					# 	hitbox_rect.center = offset_rect.center
					# 	pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
					# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
					# 	pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)