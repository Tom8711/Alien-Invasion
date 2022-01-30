class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 10
        self.alien_bullet_speed = 0.3

        # Shield settings
        self.shield_width = 100
        self.shield_height = 30
        self.shield_color = (0, 0, 255)

        # How quickly the game speeds up.
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # How quickly the fire rate increases.
        self.fire_rate_scale = 1.05

        self.initialize_dynamic_medium_settings()

    def initialize_dynamic_medium_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.6
        self.alien_points = 50
        # Based on random number pick. The higher the number the less frequent
        # the bullets fire
        self.alien_fire_rate = 20000

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        # Number of shields per column
        self.no_shields = 1

    def initialize_dynamic_easy_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.3
        self.alien_points = 20
        self.alien_fire_rate = 25000

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        # Number of shields per column
        self.no_shields = 2

    def initialize_dynamic_hard_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1
        self.alien_points = 80
        self.alien_fire_rate = 15000

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        # Number of shields per column
        self.no_shields = 0

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_fire_rate *= round(self.fire_rate_scale)

        self.alien_points = int(self.alien_points * self.score_scale)
