from parser import Parser
from engine import Engine
from gui import Game

def main():

    config = Parser.configSetter()
    engine = Engine(config)
    engine.start_next_level()
    game = Game(engine)
    game.run()

main()