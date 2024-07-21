import json

config = None
try:
    with open(file='../config.json') as f:
        config = json.load(f)
except OSError:
    print('Не удалось найти конфигурационный файл')
except json.JSONDecodeError:
    print('Не удалось прочитать файл конфигурации, возможно он повреждён')

