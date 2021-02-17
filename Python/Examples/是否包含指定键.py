dict_data = {
            "type": "follow",
            "name": "\u5173\u6ce8",
            "sub_type": 0,
            "params":{},
        }

print(dict_data.__contains__("params"))

a = dict_data.get('params')
if not a is None:
    print("sss")

if dict_data.get('params').__contains__("uid"):
    print(dict_data.get('params'))