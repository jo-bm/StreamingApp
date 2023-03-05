import requests,random


def test_local():
    response = requests.get('http://localhost/')
    assert response.status_code == 200


def test_file_list():
    response = requests.get('http://localhost/file_list/AOT')
    assert response.status_code == 200

    for i in range(5):
        episode_num = str(random.randint(1, 10)).zfill(2)
        episode_name = f'Attack_on_Titan_S01E{episode_num}.mp4'
        episode_name = bytes(episode_name, 'utf-8')
        assert episode_name in response.content


def error():
    response = requests.get('http://localhost/homer_simpson')
    assert response.status_code == 404
