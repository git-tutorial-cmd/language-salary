from collections import defaultdict

from environs import Env
from terminaltables import DoubleTable

from parce_vacancies import parse_hh_vacancies, parce_sj_vacancies


def fetch_language_vacancies(source_site, secret_key):
    vacancies = {}
    languages = env.list(
        'LANGUAGES',
        [
            'JavaScript',
            'Java',
            'Python',
            'Ruby',
            'PHP',
            'C++',
            'C#',
            'Go',
            'TypeScript',
        ]
    )
    for language in languages:
        if source_site == 'hh':
            vacancies[language] = parse_hh_vacancies(language)
        elif source_site == 'sj':
            vacancies[language] = parce_sj_vacancies(language, secret_key)
    return vacancies


def predict_common_salary(salary_from, salary_to):
    if salary_from or salary_to:
        if not salary_from:
            return salary_to * 0.8
        elif not salary_to:
            return salary_from * 1.2
        return (salary_from + salary_to) / 2
    return None


def predict_rub_salary_hh(vacancy):
    if vacancy['salary']['currency'] == 'RUR':
        return predict_common_salary(
            vacancy['salary']['from'],
            vacancy['salary']['to'],
        )
    return None


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        return predict_common_salary(
            vacancy['payment_from'],
            vacancy['payment_to'],
        )
    return None


def get_predict_rub_salary(vacancy, source_site):
    if source_site == 'hh':
        return predict_rub_salary_hh(vacancy)
    elif source_site == 'sj':
        return predict_rub_salary_sj(vacancy)
    return None


def fetch_all_rub_salary(vacancies, source_site):
    all_salaries = []
    for vacancy in vacancies:
        vacancy_salary = get_predict_rub_salary(vacancy, source_site)
        if vacancy_salary:
            all_salaries.append(vacancy_salary)
    return all_salaries


def get_vacancies_statistic(source, secret_key=None):
    vacancies_statistic = defaultdict(str)
    for language, vacancies in fetch_language_vacancies(source,
                                                        secret_key).items():
        all_salaries = fetch_all_rub_salary(vacancies, source)
        if not all_salaries:
            continue
        average_salary = int(sum(all_salaries) / len(all_salaries))
        vacancies_statistic[language] = {
            'vacancies_found': len(vacancies),
            'vacancies_processed': len(all_salaries),
            'average_salary': average_salary
        }
    return vacancies_statistic


def print_terminaltable(statistic, title):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ],
    ]
    for language, statistic in statistic.items():
        table_line = [
            language,
            statistic['vacancies_found'],
            statistic['vacancies_processed'],
            statistic['average_salary'],
        ]
        table_data.append(table_line)

    title = 'SuperJob Moscow'
    table = DoubleTable(table_data, title)
    print(table.table)


def main():
    sj_secret_key = env('SUPERJOB_SECRET_KEY')

    vacancies_statistic_hh = get_vacancies_statistic('hh')
    vacancies_statistic_sj = get_vacancies_statistic('sj', sj_secret_key)

    print_terminaltable(vacancies_statistic_hh, 'HeadHunter Moscow')
    print_terminaltable(vacancies_statistic_sj, 'SuperJob Moscow')


if __name__ == '__main__':
    env = Env()
    env.read_env()
    main()
