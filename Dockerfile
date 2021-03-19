FROM python:3.9.2
RUN apt-get update \
	&& apt-get install -y python3-pip \
	&& ln -s /usr/bin/python3 python 

RUN mkdir /app
WORKDIR /app

COPY report/ /app 
WORKDIR /app/
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install urllib3
RUN pip install beautifulsoup4
RUN pip install lxml
RUN pip install gspread
RUN pip install oauth2client

EXPOSE 3004

CMD python main.py