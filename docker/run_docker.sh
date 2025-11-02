docker run --device=/dev/dxg --security-opt seccomp=unconfined -d --rm --name ocr_cli_runner --shm-size=256m -v /mnt/d/sator/documents/ocr-refine/宗教・カルト・法/宗教・カルト・法.jpeg -i ocr-v2-cli-py310:latest
