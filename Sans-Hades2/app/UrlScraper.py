from bs4 import BeautifulSoup  # Web scraper lib
import requests  # Url Requester lib
from datetime import datetime  # Todays date lib
import json  # Json converter lib
from urllib.parse import urlparse  # Get Domain from URLS
import json  # Json Responses
from datetime import datetime  # TimeStamps

time_now = datetime.now()
# url = 'https://www.eldiariodechihuahua.mx/local/judicializadas-2675-denuncias-en-caso-aras-20230706-2073545.html'
url = ''


def multi_url_identifier(url):
    url_array = []
    if type(url) is list:
        url_array = url
    elif type(url) is (str):
        url_array = [url]

    return url_array


def domain_identifier(url):
    url_domain = []
    url_array = multi_url_identifier(url)
    for Url in url_array:
        domain = urlparse(Url, scheme='', allow_fragments=False)
        url_domain.append(["https://" + domain.netloc])
    return url_domain


def slash_assigner(url):  # Al final de cada Href sin Dominio necesita un Slash
    if not url.startswith("/"):
        return "/" + url
    else:
        return url


def half_tag_finder(url, domain_true, domain_urls):  # Aun no se habilita la version con POWER , para eso exite domain_urls
    domain_list = domain_identifier(url)  # Obtenemos nuestros url Dominio
    returner = []
    loop_counter = 0
    for U in domain_list:  # Por cada url Dominio , obtener una Sopa
        returner.append([loop_counter])
        url_smart_list = []
        soup = None
        page = requests.get(U[0])
        soup = BeautifulSoup(page.text, 'html.parser')
        for link in soup.find_all('a'):  # Por cada Sopa obtener todos los links
            half_link = str(link.get('href'))
            half_link = slash_assigner(half_link)
            full_link = ''
            if 'http' not in half_link:  # asegurar que el link sea a la mitad
                full_link = U[0] + half_link
                if full_link not in url_smart_list:  # concatenar si no existe
                    url_smart_list.append(str(full_link))
        returner[loop_counter].append(url_smart_list)
        loop_counter += 1
    return returner


def full_tag_finder(url, domain_true, domain_urls):
    domain_list = domain_identifier(url)
    returner = []
    loop_counter = 0
    for U in domain_list:
        returner.append([loop_counter])
        url_smart_list = []
        soup = None
        page = requests.get(U[0])
        soup = BeautifulSoup(page.text, 'html.parser')
        for link in soup.find_all('a'):
            half_link = str(link.get('href'))
            if 'http' in half_link and U[
                0] in half_link:  # Ignoramos que sea un link completo  y que el dominio se encuentre en el link
                full_link = half_link
                if full_link not in url_smart_list:
                    url_smart_list.append(str(full_link))
        returner[loop_counter].append(url_smart_list)
        loop_counter += 1
    return returner


def enlistator(list):
    new_list = []
    for l in list:
        new_list.append([l])
    print(new_list)

    return new_list


def append_list(list1, list2):
    suma = {}
    for i in range(len(list1)):
        new_list = list1[i][1] + list2[i][1]
        suma[i] = enlistator(new_list)

    return suma


def half_full_concatenator(url, domain_true, domain_url):
    a = half_tag_finder(url, domain_true, domain_url)
    b = full_tag_finder(url, domain_true, domain_url)
    c = append_list(a, b)

    return c


def body_reader(links, time_now):
    for main_url in links:
        print(main_url)
        for i in range(len(links[main_url])):
            page = requests.get(links[main_url][i][0])
            soup = BeautifulSoup(page.content, 'lxml')
            soupon = str(soup.prettify().encode('utf-8'))
            json_data = str(time_now) + str(json.dumps(soupon))
            links[main_url][i].append(json_data)

    return links
