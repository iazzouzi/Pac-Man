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
          if len(sys.argv) != 2:
               raise SystemExit("Error: Invalid number of arguments")
          file = sys.argv[1]
          Parser.filePreprocess(file)
          try:
               with open(file) as file:
                    data = json.load(file)
          except json.JSONDecodeError as e:
               raise SystemExit(e)
          print(data)
