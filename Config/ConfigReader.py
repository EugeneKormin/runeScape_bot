import configparser


config = configparser.ConfigParser()
config.sections()
config.read(r'C:\PycharmProjects\runeScape_bot\Config\config.ini')

window_name: str = config["window"]["name"]
