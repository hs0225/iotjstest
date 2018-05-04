### How to use remote test for Tizen Service App
  1. Connect sdb (sdb connect <your ip>)
  2. Flash service app to your target board with tizen studio.
  3. Modify `appid` and `iotjs_path` in `config.json`.
  5. run `tester.py`.