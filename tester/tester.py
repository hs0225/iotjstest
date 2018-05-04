#!/usr/bin/env python

from api.runner import Runner
from api import util

def main():
  config  = util.read_json_file("config.json")
  # run iotjs test
  runner = Runner(config)

  runner.run()


if __name__ == '__main__':
  main()