class GameLevel:
    def __init__(self, level_number, enemy_count):
        self.level_number = level_number
        self.enemy_count = enemy_count

    def start_level(self):
        # Initialize enemies, player position, etc.
        # Display level number or other indicators
        pass

    def update(self):
        # Update game state (e.g., player movement, enemy AI)
        # Check for level completion conditions
        pass

    def is_level_complete(self):
        # Check if all enemies are defeated or other conditions met
        pass

    def next_level(self):
        # Prepare for the next level
        pass

# Example usage
current_level = 1
levels = [
    GameLevel(1, 10),  # Level 1 with 10 enemies
    GameLevel(2, 15),  # Level 2 with 15 enemies
    # Add more levels as needed
]

# Game loop
while True:
    current_level_instance = levels[current_level - 1]
    current_level_instance.start_level()

    while not current_level_instance.is_level_complete():
        # Game update logic (player movement, enemy AI, collision detection)
        current_level_instance.update()

    current_level_instance.next_level()
    current_level += 1
