RENDER_ARGS=""
if [ -e /dev/dri/renderD128 ]; then
    RENDER_ARGS="--group-add $(stat -c '%g' /dev/dri/renderD128)"
fi

sudo docker run --device /dev/dxg --device /dev/dri --mount type=bind,src=/usr/lib/wsl,dst=/usr/lib/wsl \
    --security-opt seccomp=unconfined -d --rm --shm-size=8g --name ocr_cli_runner \
    --cap-add=SYS_PTRACE \
    --ipc=host \
    -v /mnt/d/sator/documents/ocr-refine/宗教・カルト・法/宗教・カルト・法.jpeg:/root/input.jpeg \
    -e LD_LIBRARY_PATH=/usr/lib/wsl/lib:/opt/venv/lib/python3.12/site-packages/torch/lib:/opt/ompi/lib:/opt/rocm/lib:/usr/local/lib \
    -e HSA_OVERRIDE_GFX_VERSION=11.0.0 \
    --group-add video \
    --group-add render \
    $RENDER_ARGS \
    ocr-v2-cli-radeon-py312:latest tail -f /dev/null
