import requests
from bs4 import BeautifulSoup
from re import findall
from wget import download
from json import loads
from sys import argv

def up(filename):
    files = {
        'file': open(filename, 'rb'),
    }

    response = requests.post('https://api.bayfiles.com/upload', files=files)

    return(loads(response.text.replace('\\',''))['data']['file']['metadata']['id'])


def dl(id):
    file = requests.get(f'https://bayfiles.com/{id}')    
    soup = BeautifulSoup(file.content,'html.parser')
    link = soup.find('a',{'id':'download-url'})
    link = findall('href="(.*)" id',link.decode())[0]
    download(link)

if argv[1] == 'up':
    print('please wait ...')
    print(f'file code : {up(argv[2])}')
elif argv[1] == 'dl':
    print('please wait ...\n')
    dl(argv[2])
