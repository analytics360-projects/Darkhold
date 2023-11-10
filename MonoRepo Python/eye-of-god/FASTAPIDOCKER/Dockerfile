FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
LABEL maintainer="Edgar Martinez [edgarmartinezanchondo@gmail.com]"


RUN pip install beautifulsoup4
RUN pip install uvicorn
RUN pip install fastapi
COPY ./app /app
EXPOSE 80