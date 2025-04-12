# Sử dụng image chính thức của Ubuntu 22.04
FROM ubuntu:22.04 AS builder


# Thiết lập biến môi trường để tránh các thông báo trong quá trình cài đặt
ENV DEBIAN_FRONTEND=noninteractive


# Cập nhật danh sách các gói và cài đặt các gói cần thiết
RUN apt-get update && \
    apt-get install -y \
        wget \
        python3 \
        python3-pip \
        git \
        nano \
        htop \
        pkg-config \
        default-libmysqlclient-dev \
        libnss3 \
        libxss1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libgbm-dev \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libdrm2 \
        libu2f-udev \
        libvulkan1 \
        fonts-liberation \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome.deb && \
    rm google-chrome.deb

# Thiết lập thư mục làm việc trong container
WORKDIR /_app_

# Sao chép toàn bộ mã nguồn vào container
COPY . /_app_


# Cài đặt các gói yêu cầu
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir --upgrade -r /_app_/requirements.txt

# Xóa thư mục .venv nếu có
RUN rm -rf /_app_/venv-api-base-public || true


# Lệnh để chạy ứng dụng
CMD ["python3", "run_api.py"]