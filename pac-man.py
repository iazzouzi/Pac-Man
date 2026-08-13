from parser import Parser
from engine import Engine

def main():

    config = Parser.configSetter()
    engine = Engine(config)
    engine.gameLoop()

main()