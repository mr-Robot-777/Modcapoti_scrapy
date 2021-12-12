from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class ParserjobPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.ParserJobVacancyBase

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]

        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.hh_process_salary(item['salary'])
        else:
            item['min'], item['max'], item['cur'] = self.sj_process_salary(item['salary'])

        del (item['salary'])
        try:
            collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
        except DuplicateKeyError as e:
            print(e)

    @staticmethod
    def hh_process_salary(salary):
        if len(salary) > 1:
            if salary[2] == ' до ':
                salary_min = int(salary[1].replace('\xa0', ''))
                salary_max = int(salary[3].replace('\xa0', ''))
                currency = salary[5]
            elif salary[0] == 'до ':
                salary_min, salary_max, currency = None, int(salary[1].replace('\xa0', '')), salary[3]
            else:
                salary_min, salary_max, currency = int(salary[1].replace('\xa0', '')), None, salary[3]
        else:
            salary_min, salary_max, currency = None, None, None
        return salary_min, salary_max, currency

    @staticmethod
    def sj_process_salary(salary):
        if len(salary) > 1:
            if len(salary) > 3:
                salary_min = int(salary[0].replace('\xa0', ''))
                salary_max = int(salary[4].replace('\xa0', ''))
                currency = salary[6]
            elif salary[0] == 'от':
                salary_and_curr = salary[2].split('\xa0')
                salary_min = int(salary_and_curr[0] + salary_and_curr[1])
                salary_max = None
                currency = salary_and_curr[2]
            elif salary[0] == 'до':
                salary_and_curr = salary[2].split('\xa0')
                salary_min = None
                salary_max = int(salary_and_curr[0] + salary_and_curr[1])
                currency = salary_and_curr[2]
            else:
                sal = int(salary[0].replace('\xa0', ''))
                salary_min, salary_max, currency = sal, sal, salary[2]
        else:
            salary_min, salary_max, currency = None, None, None
        return salary_min, salary_max, currency
