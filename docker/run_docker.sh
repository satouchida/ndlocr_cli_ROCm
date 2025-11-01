docker run --device=/dev/dxg --security-opt seccomp=unconfined -d --rm --name ocr_cli_runner --shm-size=256m  -i ocr-v2-cli-py310:latest
