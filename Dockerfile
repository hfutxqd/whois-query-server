FROM python:3.7

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y redis-server

WORKDIR /app

COPY . .

RUN mkdir -p $HOME/.config/pip
RUN cat ./pip.conf > $HOME/.config/pip/pip.conf
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["bash"]
CMD ["start.sh"]