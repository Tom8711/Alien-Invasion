import pygame
from pygame.sprite import Sprite

class Shield(Sprite):
	"""A class to manage shields against bullets"""

	def __init__(self, ai_game):
		"""Initiate a single shield"""
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings

		# Initiate a single shield at (0, 0)
		self.rect = pygame.Rect(0, 0, self.settings.shield_width,
				self.settings.shield_height)

	def draw_shield(self):
		"""Draw the shield on the screen"""
		pygame.draw.rect(self.screen, self.settings.shield_color, self.rect)