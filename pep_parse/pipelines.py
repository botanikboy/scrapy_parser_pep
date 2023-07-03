from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def __init__(self):
        self.__peps = {}

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.__peps[item['status']] = self.__peps.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{timestamp}.csv'
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        file_path = results_dir / filename
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status, count in self.__peps.items():
                f.write(f'{status},{count}\n')
            f.write(f'Total,{sum(self.__peps.values())}\n')
