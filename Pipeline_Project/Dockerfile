FROM apache/airflow:2.2.3

USER root

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install openjdk-11-jdk -y && \
    apt-get install ant -y && \
    apt-get install iputils-ping -y && \
    apt install nano -y && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

USER airflow

RUN pip install pyspark \
    pip install apache-airflow-providers-apache-spark \
    pip install apache-airflow-providers-amazon \
    pip install --no-cache-dir apache-airflow-providers-docker==2.1.0 \
    pip install apache-airflow-providers-cncf-kubernetes \
    pip install pymysql \
    pip install minio \
    pip install xlrd \
    pip install openpyxl \
    pip install boto3 \