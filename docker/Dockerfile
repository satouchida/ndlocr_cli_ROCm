FROM rocm/pytorch:rocm5.7_ubuntu22.04_py3.10_pytorch_2.0.1

ENV PROJECT_DIR=/root/ocr_cli

RUN set -x \
    && apt update \
    && apt upgrade -y

RUN set -x \
    && apt update \
    && apt -y install locales \
    && locale-gen ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8


RUN set -x     && apt-get update && apt-get install -y libgl1-mesa-dev libglib2.0-0 zip git python3-pip wget cmake curl
RUN ln -sf /usr/bin/python3 /usr/bin/python

ENV TZ=Asia/Tokyo
ENV PATH="/root/.cargo/bin:${PATH}"
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone




RUN set -x \
    && wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz \
    && tar xzvf kytea-0.4.7.tar.gz \
    && cd kytea-0.4.7 \
    && ./configure \
    && make \
    && make install \
    && ldconfig

COPY cli ${PROJECT_DIR}/cli
COPY main.py ${PROJECT_DIR}
COPY README.md ${PROJECT_DIR}
COPY requirements.txt ${PROJECT_DIR}
COPY config.yml ${PROJECT_DIR}
COPY eval_config.yml ${PROJECT_DIR}
RUN apt-get update && \
    apt-get install -y cmake
RUN set -x     && pip install --no-cache-dir --verbose -r ${PROJECT_DIR}/requirements.txt

COPY submodules/deskew_HT ${PROJECT_DIR}/submodules/deskew_HT
COPY submodules/ndl_layout ${PROJECT_DIR}/submodules/ndl_layout
COPY submodules/ocr_line_eval_script ${PROJECT_DIR}/submodules/ocr_line_eval_script
COPY submodules/reading_order ${PROJECT_DIR}/submodules/reading_order
COPY submodules/ruby_prediction ${PROJECT_DIR}/submodules/ruby_prediction
COPY submodules/separate_pages_mmdet ${PROJECT_DIR}/submodules/separate_pages_mmdet
COPY submodules/text_recognition_lightning ${PROJECT_DIR}/submodules/text_recognition_lightning


RUN set -x \
    && pip3 install mmdet==3.3.0\
    && pip3 install -r ${PROJECT_DIR}/submodules/ruby_prediction/requirements.txt



WORKDIR ${PROJECT_DIR}
