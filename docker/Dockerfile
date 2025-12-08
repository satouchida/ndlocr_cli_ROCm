FROM rocm/pytorch:rocm6.4.3_ubuntu24.04_py3.12_pytorch_release_2.3.0
FROM rocm/dev-ubuntu-24.04:6.4.2
RUN groupadd -g 109 render && groupadd -g 109 video && useradd -g 109 -ms /bin/bash root

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


COPY docker/setup.sh /root/setup.sh
RUN chmod +x /root/setup.sh && /root/setup.sh

RUN pip install --upgrade pip


# Create constraints file to prevent PyTorch upgrade
# Using PyTorch 2.3.0 provided by the base image
RUN echo "torch==2.3.0" > /root/constraints.txt \
    && echo "torchvision" >> /root/constraints.txt

# Force reinstall torch from ROCm wheel to ensure GPU support (must be before mmcv build)

RUN pip install mmengine ninja
# Set constraint file for build steps
ENV PIP_CONSTRAINT=/root/constraints.txt

RUN git clone https://github.com/open-mmlab/mmcv.git -b v2.2.0 \
    && cd mmcv \
    && MAX_JOBS=2 MMCV_WITH_OPS=1 FORCE_CUDA=1 CXXFLAGS="-std=c++17" pip install --no-build-isolation . \
    && cd .. \
    && rm -rf mmcv
RUN git clone https://github.com/open-mmlab/mmdetection.git -b v3.3.0 \
    && cd mmdetection \
    && pip install -r requirements/build.txt \
    && MAX_JOBS=2 FORCE_CUDA=1 CXXFLAGS="-std=c++17" pip install --no-build-isolation . \
    && cd .. \
    && rm -rf mmdetection



# Fix for ROCm/PyTorch library naming mismatch
# Path updated for Python 3.12 in ROCm 6.2+ image
RUN cd /opt/conda/envs/py_3.12/lib/python3.12/site-packages/torch/lib \
    && (test -e libc10_hip.so || ln -s libc10_cuda.so libc10_hip.so) \
    && (test -e libtorch_hip.so || ln -s libtorch_cuda.so libtorch_hip.so) \
    && (test -e libtorch_hip_linalg.so || ln -s libtorch_cuda_linalg.so libtorch_hip_linalg.so)

ENV LD_LIBRARY_PATH="/opt/conda/envs/py_3.12/lib/python3.12/site-packages/torch/lib:${LD_LIBRARY_PATH}"

COPY cli ${PROJECT_DIR}/cli
COPY main.py ${PROJECT_DIR}
COPY README.md ${PROJECT_DIR}
COPY requirements.all.txt ${PROJECT_DIR}
COPY docker/requirements.pre.txt ${PROJECT_DIR}
COPY config.yml ${PROJECT_DIR}
COPY eval_config.yml ${PROJECT_DIR}
COPY verify_rocm.py ${PROJECT_DIR}


RUN set -x     && pip install --no-cache-dir --verbose -c /root/constraints.txt -r ${PROJECT_DIR}/requirements.pre.txt
RUN set -x     && pip install --no-cache-dir --verbose -c /root/constraints.txt -r ${PROJECT_DIR}/requirements.all.txt

COPY submodules/deskew_HT ${PROJECT_DIR}/submodules/deskew_HT
COPY submodules/ndl_layout ${PROJECT_DIR}/submodules/ndl_layout
COPY submodules/ocr_line_eval_script ${PROJECT_DIR}/submodules/ocr_line_eval_script
COPY submodules/reading_order ${PROJECT_DIR}/submodules/reading_order
COPY submodules/ruby_prediction ${PROJECT_DIR}/submodules/ruby_prediction
COPY submodules/separate_pages_mmdet ${PROJECT_DIR}/submodules/separate_pages_mmdet
COPY submodules/text_recognition_lightning ${PROJECT_DIR}/submodules/text_recognition_lightning




WORKDIR ${PROJECT_DIR}
