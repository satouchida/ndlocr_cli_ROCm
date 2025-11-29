sudo docker run --device /dev/dxg --security-opt seccomp=unconfined -d --rm --shm-size=8g --name ocr_cli_runner \
    -v /usr/lib/wsl/lib:/usr/lib/wsl/lib \
    -v "/mnt/d/sator/documents/ocr-refine/宗教・カルト・法/宗教・カルト・法.jpeg":/root/input.jpeg \
    -e LD_LIBRARY_PATH=/usr/lib/wsl/lib:/opt/conda/envs/py_3.10/lib/python3.10/site-packages/torch/lib:/opt/ompi/lib:/opt/rocm/lib:/usr/local/lib \
    -e HSA_OVERRIDE_GFX_VERSION=10.3.0 \
    ocr-v2-cli-py310:latest tail -f /dev/null
