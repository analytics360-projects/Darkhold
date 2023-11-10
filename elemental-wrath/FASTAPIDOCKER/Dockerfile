FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
LABEL maintainer="Edgar Martinez [edgarmartinezanchondo@gmail.com]"


RUN pip install facebook-scraper
COPY ./app /app
EXPOSE 80