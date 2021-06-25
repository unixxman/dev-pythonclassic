FROM python:3.9
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN apt-get update && apt-get -y install vim git
RUN git config --global user.name pythonclassic
RUN git config --global user.email clearsoft.studio@gmail.com
RUN pip install -r requirements.txt
RUN mkdir /root/.ssh
RUN mkdir /srv/git
RUN mv id_rsa /root/.ssh/id_rsa
RUN mv id_rsa.pub /root/.ssh/id_rsa.pub
CMD ["gunicorn", "-w", "9", "-b", "0.0.0.0:5000", "manage:app"]