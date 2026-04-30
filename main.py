from Game import Game, Directions

def print_game(game: Game):
    (width, height) = game.size

    for y in range(height + 2):
        for x in range(width + 2):
            char = '  '

            if x < 1 or y < 1 or x > width or y > height:
                # char = '██'
                char = '🧱'

            game_pos = (x - 1, y - 1)

            if game_pos in game.snake:
                char = '🟢'
            if game_pos == game.snake[0]:
                char = '🤢'

            if game_pos in game.green_apples:
                char = '🍏'

            if game_pos in game.red_apples:
                char = '🍎'

            print(char, end='')
        print()

def main():
    game = Game()
    print_game(game)

if __name__ == '__main__':
    main()