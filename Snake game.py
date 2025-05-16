import pygame
import random
import sys

class SnakeGame:
    def __init__(self, width=800, height=600):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption('Snake Game')
        
        # Screen setup
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Game variables
        self.grid_size = 20
        self.grid_width = self.width // self.grid_size
        self.grid_height = self.height // self.grid_size

        # Snake setup
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.snake_direction = (1, 0)
        self.snake_length = 1
        
        # Food setup
        self.food_position = self.generate_food()
        
        # Score
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # Game state
        self.game_over = False

    def generate_food(self):
        """Generate food at a random location not occupied by snake"""
        while True:
            food_pos = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            if food_pos not in self.snake:
                return food_pos

    def draw_grid(self):
        """Draw grid lines for visual reference"""
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (self.width, y))

    def draw_snake(self):
        """Draw snake segments"""
        for segment in self.snake:
            rect = pygame.Rect(
                segment[0] * self.grid_size, 
                segment[1] * self.grid_size, 
                self.grid_size - 1, 
                self.grid_size - 1
            )
            pygame.draw.rect(self.screen, self.GREEN, rect)

    def draw_food(self):
        """Draw food"""
        rect = pygame.Rect(
            self.food_position[0] * self.grid_size, 
            self.food_position[1] * self.grid_size, 
            self.grid_size - 1, 
            self.grid_size - 1
        )
        pygame.draw.rect(self.screen, self.RED, rect)

    def move_snake(self):
        """Move snake and handle growth"""
        # Calculate new head position
        head = (
            self.snake[0][0] + self.snake_direction[0],
            self.snake[0][1] + self.snake_direction[1]
        )

        # Check wall collision
        if (head[0] < 0 or head[0] >= self.grid_width or 
            head[1] < 0 or head[1] >= self.grid_height):
            self.game_over = True
            return

        # Check self-collision
        if head in self.snake:
            self.game_over = True
            return

        # Add new head
        self.snake.insert(0, head)

        # Check food collision
        if head == self.food_position:
            self.score += 1
            self.food_position = self.generate_food()
            self.snake_length += 1
        else:
            # Remove tail if no food eaten and snake hasn't grown
            if len(self.snake) > self.snake_length:
                self.snake.pop()

    def display_score(self):
        """Display current score"""
        score_text = self.font.render(f'Score: {self.score}', True, self.WHITE)
        self.screen.blit(score_text, (10, 10))

    def game_over_screen(self):
        """Display game over screen"""
        self.screen.fill(self.BLACK)
        game_over_text = self.font.render('Game Over', True, self.WHITE)
        score_text = self.font.render(f'Final Score: {self.score}', True, self.WHITE)
        restart_text = self.font.render('Press R to Restart', True, self.WHITE)
        
        # Center text
        self.screen.blit(game_over_text, (self.width//2 - game_over_text.get_width()//2, 
                                           self.height//2 - 100))
        self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 
                                       self.height//2))
        self.screen.blit(restart_text, (self.width//2 - restart_text.get_width()//2, 
                                         self.height//2 + 100))
        pygame.display.flip()

    def reset_game(self):
        """Reset game to initial state"""
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.snake_direction = (1, 0)
        self.snake_length = 1
        self.food_position = self.generate_food()
        self.score = 0
        self.game_over = False

    def run(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Handle key presses
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                    else:
                        if event.key == pygame.K_UP and self.snake_direction != (0, 1):
                            self.snake_direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.snake_direction != (0, -1):
                            self.snake_direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.snake_direction != (1, 0):
                            self.snake_direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.snake_direction != (-1, 0):
                            self.snake_direction = (1, 0)

            if not self.game_over:
                # Clear screen
                self.screen.fill(self.BLACK)
                
                # Draw game elements
                self.draw_grid()
                self.move_snake()
                self.draw_snake()
                self.draw_food()
                self.display_score()
                
                # Update display
                pygame.display.flip()
                
                # Control game speed
                self.clock.tick(5)
            else:
                # Game over screen
                self.game_over_screen()
                
                # Wait for restart
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.reset_game()

def main():
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()