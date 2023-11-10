## Darkhold Api Factory
Darkhold permite consumir API , enviando 4 parametros necesarios para ello

Url     =   ''
Headers =   {}
ReqType =   ''
Body    =   ''

Darkhold permite consumir API de aplicaciones externas
(Ver test.ipynb para mayor descripcion del programa)

## elemental-wrath

Contenido
APP FASTAPI que incluye la Api fb-scrap para puros grupos abiertos * si hay un privado tiene una probabilidad de tronar el resultado

Requiere abrir el docker.

docker build . -t fbscraper

docker run -p 80:80 -d --name facebook-scraper fbscraper


## eye-of-god

El input es una URL 
Debe contener el protocolo o Http o Https para que pueda hacer la consulta
el scrapper (BeautifulSoup4)

El Output de la API genera lo siguiente
Un string del dia en que se genera la consulta  con su hora 
Lxml del contenido de la pagina visitada

## Sans-Hades2

El input es una URL o multiples URL, el scraper se enfoca en encontrar todos los link del dominio (solo los del mismo dominio base) y extrae info de cada link encontrado (no repetidos).
Puede ocacionalmente (depende del formato de la pagina en concreto) no extraer el link entregado como INPUT (por lo que se soluciona con eye of god)

Contiene la aplicacion elemental wrath y tambien carga con el detector de palabras , insertar ,etc en bd.