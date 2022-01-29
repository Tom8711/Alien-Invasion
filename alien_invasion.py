import sys
import json
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        #   and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Initiate the ship, bullet and alien classes
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create the first fleet.
        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Initiate the different difficulty buttons.
        self._make_difficulty_buttons()  

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()

    def _make_difficulty_buttons(self):
        """Initiate the difficulty buttons"""
        # Easy
        self.easy_button = Button(self, "Easy")
        self.easy_button.rect.topleft = self.screen.get_rect().topleft
        self.easy_button.rect.y = 520
        self.easy_button.msg_image_rect.center = self.easy_button.rect.center

        # Medium is set as default
        self.medium_button = Button(self, "Medium")
        self.medium_button.rect.top = self.screen.get_rect().top
        medium_rect = self.medium_button.msg_image_rect
        self.medium_button.rect.y = 520
        medium_rect.center = self.medium_button.rect.center
        self.medium_button.change_button_color("Medium", "red")

        # Hard
        self.hard_button = Button(self, "Hard")
        self.hard_button.rect.topright = self.screen.get_rect().topright
        self.hard_button.rect.y = 520
        self.hard_button.msg_image_rect.center = self.hard_button.rect.center

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._write_highscore_to_file()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_difficulty_button(mouse_pos)
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _write_highscore_to_file(self):
        """Write the current highscore to a separate file"""
        filename = "highscore.json"
        with open (filename, "w") as f:
            json.dump(self.stats.high_score, f)

    def _check_difficulty_button(self, mouse_pos):
        """Select difficulty by pressing the buttons"""
        easy_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        if easy_clicked and not self.stats.game_active:
            # Change the collors of all the buttons
            self.easy_button.change_button_color("Easy", "red")
            self.medium_button.change_button_color("Medium", "green")
            self.hard_button.change_button_color("Hard", "green")

            # Change dynamic settings to easy.
            self.settings.initialize_dynamic_easy_settings()

        medium_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        if medium_clicked and not self.stats.game_active:
            # Change the collors of all the buttons
            self.easy_button.change_button_color("Easy", "green")
            self.medium_button.change_button_color("Medium", "red")
            self.hard_button.change_button_color("Hard", "green")

            # Change dynamic settings to medium (default)
            self.settings.initialize_dynamic_medium_settings()

        hard_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if hard_clicked and not self.stats.game_active:
            # Change the collors of all the buttons
            self.easy_button.change_button_color("Easy", "green")
            self.medium_button.change_button_color("Medium", "green")
            self.hard_button.change_button_color("Hard", "red")

            # Change dynamic settings to hard.
            self.settings.initialize_dynamic_hard_settings()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self._start_game()

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._write_highscore_to_file()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and self.stats.game_active == False:
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game(self):
        """Reset game stats and start a new game"""
        # Reset the game statistics
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining alines and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        self.stats.game_active = True



    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        #Update bullet position.
        self.bullets.update()
        
        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Remove any aliens and bullets that have collided
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ship_left > 0:
            # Decrement ships left and update scoreboard.
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # Determine the number of aliens fit in one row.
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropiately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()

if __name__ == "__main__":
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()