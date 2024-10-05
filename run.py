from game.games import ClassicGame, WithEnemiesGame, Environment


if __name__ == "__main__":
    game = WithEnemiesGame()
    # game = ClassicGame()
    game = Environment()
    game.play()
