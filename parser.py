from config import Config
import json
import sys
import os

class Parser:
     @staticmethod
     def filePreprocess(file: str) -> None:
          if not file.endswith('.json'):
               raise SystemExit("Error: File must be a .json file")
          try:
               with open(file) as infile, open('temp.json', 'w') as outfile:
                    for line in infile:
                         if line.count('#') or line.count('//'):
                              continue
                         else:
                              outfile.write(line)
               os.replace('temp.json', file)
          except OSError as e:
               raise SystemExit(e)
          except Exception as e:
               raise SystemExit(e)

     @staticmethod
     def configInit() -> Config:
          levels = [(16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
                   (21, 21), (22, 22), (23, 23), (24, 24), (25, 25)]
          config = Config("highscore.json", levels, 3, 10, 50, 200, 60.0)
          return config

     @staticmethod
     def configSetter():
          if len(sys.argv) != 2:
               raise SystemExit("Error: Invalid number of arguments")
          file = sys.argv[1]
          Parser.filePreprocess(file)
          try:
               with open(file) as file:
                    data = json.load(file)
          except json.JSONDecodeError as e:
               raise SystemExit(e)
          config = Parser.configInit()

          if "highscore_filename" in data:
               heightscore_filename = data["highscore_filename"]
               if not heightscore_filename:
                    print("Error: Highscore filename cannot be empty")
               elif not heightscore_filename.endswith('.json'):
                    print("Error: Highscore file must be a .json file")
               else:
                    config.highscore_filename = heightscore_filename

          if "levels" in data:
               levels = data["levels"]
               if not levels:
                    print("Error: Level cannot be empty")
               elif len(levels) < 10:
                    print("Error: Level must contain 10 levels or more")
               elif isinstance(levels, list) and all(isinstance(l, list) and len(l) == 2 for l in levels):
                    for width, height in levels:
                         if not isinstance(width, int) or not isinstance(height, int):
                              print("Error: Level dimensions must be integers")
                              break
                         if width < 16 or width > 30 or height < 16 or height > 30:
                              print("Error: Level dimensions must be between 16 and 30")
                              break
                    else:
                         config.levels = levels
               else:
                    print("Error: Level must be a list of lists of two integers")

          if "lives" in data:
               lives = data["lives"]
               if not lives:
                    print("Error: Lives cannot be empty")
               elif isinstance(lives, int) and 0 < lives <= 10:
                    config.lives = lives
               else:
                    print("Error: Lives must be a positive integer between 1 and 10")

          if "points_per_pacgum" in data:
               points_per_pacgum = data["points_per_pacgum"]
               if not points_per_pacgum:
                    print("Error: Points per pacgum cannot be empty")
               elif isinstance(points_per_pacgum, int) and 0 < points_per_pacgum <= 1000:
                    config.points_per_pacgum = points_per_pacgum
               else:
                    print("Error: Points per pacgum must be a positive integer between 1 and 1000")

          if "points_per_super_pacgum" in data:
               points_per_super_pacgum = data["points_per_super_pacgum"]
               if not points_per_super_pacgum:
                    print("Error: Points per super pacgum cannot be empty")
               elif isinstance(points_per_super_pacgum, int) and 0 < points_per_super_pacgum <= 1000:
                    config.points_per_super_pacgum = points_per_super_pacgum
               else:
                    print("Error: Points per super pacgum must be a positive integer between 1 and 1000")

          if "points_per_ghost" in data:
               points_per_ghost = data["points_per_ghost"]
               if not points_per_ghost:
                    print("Error: Points per ghost cannot be empty")
               elif isinstance(points_per_ghost, int) and 0 < points_per_ghost <= 1000:
                    config.points_per_ghost = points_per_ghost
               else:
                    print("Error: Points per ghost must be a positive integer between 1 and 1000")

          if "level_max_time" in data:
               level_max_time = data["level_max_time"]
               if not level_max_time:
                    print("Error: Level max time cannot be empty")
               elif isinstance(level_max_time, float) and  0.0 < level_max_time <= 600.0:
                    config.level_max_time = level_max_time
               else:
                    print("Error: Level max time must be a positive float between 0.0 and 600.0")

          return config
