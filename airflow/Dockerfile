ARG AIRFLOW_IMAGE_NAME
FROM ${AIRFLOW_IMAGE_NAME}

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR $AIRFLOW_HOME

USER root

# Cập nhật danh sách gói và cài đặt các gói cần thiết
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        vim \
        python3-pip \
        default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập JAVA_HOME và cập nhật PATH
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Kiểm tra phiên bản Java để xác nhận cài đặt thành công
RUN java --version

# Sao chép và cài đặt các phụ thuộc Python
COPY requirements.txt .

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --no-cache-dir -r requirements.txt

# Sao chép các script và thiết lập quyền thực thi
COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID
