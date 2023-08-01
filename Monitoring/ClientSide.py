import json


class ClientSide(object):
    @staticmethod
    def update_data_for_monitoring(value: dict, file_name: str):
        with open(fr'C:\PycharmProjects\runeScape_bot\Monitoring\{file_name}.json', 'w') as file:
            json.dump(value, file)
