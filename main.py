import requests
import time


class OverflowSearch:
    def __init__(self):
        pass

    def make_search(self, tag: str, hours=1):
        """Поиск по тегу за последние hours часов. За день набегает многовато вопросов, решил в часах квантовать"""
        endpoint = 'https://api.stackexchange.com/2.2/search'
        now = int(time.time())
        from_date = str(now - 60 * 60 * hours)
        numpage = 1
        the_tag = self.check_tag(tag)
        if the_tag is None:
            print(f'There is no {tag} in tags')
            return [{'title': None}]

        parameters = {'site': 'stackoverflow',
                      'tagged': tag,
                      'fromdate': from_date,
                      'sort': 'creation',
                      'pagesize': '100',
                      'page': str(numpage)
                      }
        has_it_more = True
        list_of_things = ['Spam!']
        print('Collecting pages:')
        while has_it_more:
            response = requests.get(endpoint, params=parameters)
            response.raise_for_status()
            print(numpage)
            time.sleep(1)  # чтобы не забанили
            list_of_things += response.json()['items']
            has_it_more = response.json()['has_more']
            numpage += 1
            parameters['page'] = str(numpage)

        list_of_things.pop(0)
        output = tuple(list_of_things)
        return output

    def check_tag(self, tag: str):
        endpoint = f'https://api.stackexchange.com/2.2/tags/{tag}/info'
        parameters = {'site': 'stackoverflow'}
        response = requests.get(endpoint, params=parameters)
        if response.json()['items']:
            its_name = response.json()['items'][0]['name']
        else:
            its_name = None

        return its_name


def the_search():
    my_tag = input('Введите тэг для поиска запросов, например Python:\n')
    string_hours = input('За сколько последних часов?\n')  # За два дня больно много вопросов, но можно искать 48 часов
    if string_hours.isdigit():
        for_hours = int(string_hours.strip())
    else:
        print(f'{string_hours} - это не время в часах')
        return

    searcher = OverflowSearch()
    my_search = searcher.make_search(my_tag, for_hours)
    print(f'Запросы по тегу {my_tag} за {for_hours} часа(ов):')
    for count, thing in enumerate(my_search):
        print(f'{count}. {thing["title"]}')


if __name__ == '__main__':
    the_search()
