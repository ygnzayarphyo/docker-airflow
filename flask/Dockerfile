FROM python:3.6
COPY . /flask
WORKDIR /flask
# Change docker time_zone
ENV TZ="Asia/Tokyo"
RUN date
# linking mysql socket
RUN ln -s /private/var/mysql/mysql.sock /tmp/mysql.sock

WORKDIR /flask
RUN pip install -r requirements.txt
EXPOSE 5006
CMD python ./flask/app.py
RUN date