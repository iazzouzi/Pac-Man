from parser import Parser
from engine import Engine
from GUI_engine import GameScreen

def main():

    config = Parser.configSetter()
    engine = Engine(config)
    engine.start_next_level()
    game = GameScreen(engine)
    game.run()

main()