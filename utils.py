import sqlite3

from flask import jsonify

# with sqlite3.connect("netflix.db") as connection:
#     cursor = connection.cursor()
#     cursor.execute("""SELECT * FROM netflix""")
#     cursor.fetchall()

"""Создаем подключение к БД с помощью метода sqlite3.connect"""

def get_all(query: str):
    #подключение к БД
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = []
        #цикл проходящий по всем строкам и добовляет значение в словарь
        for item in connection.execute(query).fetchall():
            s = dict(item)
            result.append(s)

        return result


def get_one(query: str):
    #возвращаем одно слово
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchone()
        return dict(result)


#Напишем функцию, которая получает в качестве аргумента имена двух актеров,
# сохраняет всех актеров из колонки cast и возвращает список тех,
# кто играет с ними в паре больше 2 раз.

def search_by_cast(name1: str = 'Rose McIver', name2: str = 'Ben Lamb'):
    query = f"""
    SELECT * FROM netflix
    WHERE "cast" like '%{name1}%' and "cast" like '%{name2}%'
    """

    result = get_all(query)
    all_actors = []
    actors = []
#создаем общий список актеров
    for item in result:
        #делаем список актеров
        item = ''.join(item)
        #разделяем актеров
        item = item.split(', ')
        #добавим каждого актера в список
        for item_list in item:
            all_actors.append(item_list)
    #список кто сыграл более 2 раз
    for actor in all_actors:
        count = 0
        for item in all_actors:
            if item == actor:
                count += 1
        if count > 2:
            actors.append(actor)

    #избавимся от повторений
    actors = set(actors)

    return actors

#Напишем функцию, с помощью которой можно будет передавать тип картины
#и получать на выходе список названий картин с их описаниями в JSON.
def get_movie_by_type(type: str, release_year, genre: str):
    query = """
    SELECT * FROM netflix
    WHERE 'type' = '{type}'
    AND 'release_year' = '{release_year}'
    AND 'listed_in' = '{genre}'
    """

    result = get_all(query)
    result = []

    for item in result:
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )

    return jsonify(result)





# def search_name():
#     """Реализация поиска по названию."""
#     with sqlite3.connect("netflix.db") as connection:
#         cursor = connection.cursor()
#         sqlite_query = "SELECT * FROM netflix"
#         result = cursor.execute(sqlite_query)
#         for row in result:
#             print(row)

