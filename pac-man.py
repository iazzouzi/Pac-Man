from parser import Parser

def main():

    config = Parser.configSetter()
    print(config.highscore_filename)
    print(config.level)
    print(config.lives)
    print(config.points_per_pacgum)
    print(config.points_per_super_pacgum)
    print(config.points_per_ghost)
    print(config.level_max_time)

main()