import json

class GameStats:
	"""Track statistics for Alien Invasion"""

	def __init__(self, ai_game):
		"""Initialize statistics."""
		self.settings = ai_game.settings
		self.reset_stats()

		# Start Alien Invasion in an inactive state.
		self.game_active = False

		# High score should never be reset.
		self._get_highscore()

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		self.ship_left = self.settings.ship_limit
		self.score = 0
		self.level = 1

	def _get_highscore(self):
		"""Read the current highscore. If there is none, set it to 0."""
		filename = "highscore.json"
		try:
			with open(filename, "r") as f:
				self.high_score = json.load(f)
		except FileNotFoundError:
			self.high_score = 0