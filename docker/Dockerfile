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


COPY docker/setup.sh /root/setup.sh
RUN chmod +x /root/setup.sh && /root/setup.sh

RUN pip install --upgrade pip

# Create constraints file to prevent PyTorch upgrade
RUN echo "torch==2.0.1" > /root/constraints.txt \
    && echo "torchvision==0.15.2" >> /root/constraints.txt

# Force reinstall torch from ROCm wheel to ensure GPU support (must be before mmcv build)
RUN pip install --pre --force-reinstall torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/rocm5.4.2
RUN pip install mmengine ninja
# Set constraint file for build steps
ENV PIP_CONSTRAINT=/root/constraints.txt

RUN git clone https://github.com/open-mmlab/mmcv.git -b v2.1.0 \
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
RUN cd /opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib \
    && ln -sf libc10_cuda.so libc10_hip.so \
    && ln -sf libtorch_cuda.so libtorch_hip.so \
    && ln -sf libtorch_cuda_linalg.so libtorch_hip_linalg.so

ENV LD_LIBRARY_PATH="/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib:${LD_LIBRARY_PATH}"

COPY cli ${PROJECT_DIR}/cli
COPY main.py ${PROJECT_DIR}
COPY README.md ${PROJECT_DIR}
COPY requirements.all.txt ${PROJECT_DIR}
COPY docker/requirements.pre.txt ${PROJECT_DIR}
COPY config.yml ${PROJECT_DIR}
COPY eval_config.yml ${PROJECT_DIR}
COPY verify_rocm.py ${PROJECT_DIR}


RUN set -x     && pip install --no-cache-dir --verbose -c /root/constraints.txt -r ${PROJECT_DIR}/requirements.pre.txt
RUN set -x     && pip install --no-cache-dir --verbose -c /root/constraints.txt -r ${PROJECT_DIR}/requirements.all.txt --extra-index-url https://download.pytorch.org/whl/rocm5.4.2

COPY submodules/deskew_HT ${PROJECT_DIR}/submodules/deskew_HT
COPY submodules/ndl_layout ${PROJECT_DIR}/submodules/ndl_layout
COPY submodules/ocr_line_eval_script ${PROJECT_DIR}/submodules/ocr_line_eval_script
COPY submodules/reading_order ${PROJECT_DIR}/submodules/reading_order
COPY submodules/ruby_prediction ${PROJECT_DIR}/submodules/ruby_prediction
COPY submodules/separate_pages_mmdet ${PROJECT_DIR}/submodules/separate_pages_mmdet
COPY submodules/text_recognition_lightning ${PROJECT_DIR}/submodules/text_recognition_lightning




WORKDIR ${PROJECT_DIR}
