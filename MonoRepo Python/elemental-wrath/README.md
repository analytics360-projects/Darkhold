# elemental-wrath FB Scraper DV1 
DEMO VERSION 1
Edgar Martinez Anchondo <edgarmartinezanchondo@gmail.com>

Contenido
APP FASTAPI que incluye la Api fb-scrap para puros grupos abiertos * si hay un privado tiene una probabilidad de tronar el resultado

Requiere abrir el docker.

docker build . -t fbscraper

docker run -p 80:80 -d --name facebook-scraper fbscraper


