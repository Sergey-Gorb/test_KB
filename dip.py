import json
import requests
from pathlib import Path


URL = 'https://jsonplaceholder.typicode.com'


def getintinput(msg, min_int, max_int, def_int=5):
    while True:
        inp = input(msg)
        if inp:
            try:
                int_inp = int(inp)
                if int_inp < min_int or int_inp > max_int:
                    print(f'Value {int_inp} out margin!')
                else:
                    return int_inp
            except ValueError:
                print('Bad value', inp)
        else:
            return def_int
        print('Try again!')


def get_user_info(user_id=1, part='posts'):
    s_req = f'{URL}/users/{user_id}/{part}'
    res = requests.get(s_req)
    return json.loads(res.text)


if __name__ == '__main__':
    msg = 'Введите <user_id> для JSONPlaceholder пользователя: '
    jp_user = getintinput(msg, 1, 10, def_int=5)
    s_req = f'{URL}/users/{jp_user}'
    resp = requests.get(s_req)
    if resp.status_code == 200:
        file_spec = Path.cwd() / f'JSONInfo{jp_user}'
        with open(f'{file_spec}', 'wt') as file:
            data = json.loads(resp.text)
            wcontent = f'User_id: {jp_user} Name: {data["name"]}\n'
            file.write(wcontent)
            posts = get_user_info(user_id=jp_user)
            wcontent = ', '.join(str(post['id']) for post in posts)
            file.write(f'PostIDs = {wcontent}\n')
            for post in posts:
                wcontent = f'PostID: {post["id"]} Title: {post["title"]}'
                file.write(f'{wcontent}\n')

        albums = get_user_info(user_id=jp_user, part='albums')
        album_id = albums[0]['id']
        s_req = f'{URL}/albums/{album_id}/photos'
        resp = requests.get(s_req)
        if resp.status_code == 200:
            photos = json.loads(resp.text)
            photo_url = photos[0]['url']
            photo_id = photos[0]['id']
            # print(f'Photo URL: {photo_url} photo id {photo_id}')
            api = requests.get(photo_url)
            file_spec = Path.cwd() / f'Album{album_id}photo{photo_id}'
            with open(f'{file_spec}', 'wb') as file:
                file.write(api.content)
                # print(f'Зарисан файл {file_spec}')
    else:
        print(f'Проблема с JSONPlaceholder пользователем <{jp_user}>')
