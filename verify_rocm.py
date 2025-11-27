import torch
import mmcv
import mmdet
from mmcv.ops import get_compiler_version, get_compiling_cuda_version

def check_rocm():
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device count: {torch.cuda.device_count()}")
        print(f"Device name: {torch.cuda.get_device_name(0)}")
        try:
            print(f"ROCm version: {torch.version.hip}")
        except AttributeError:
            print("ROCm version: Not found (might be CUDA)")
    else:
        print("WARNING: CUDA/ROCm not available!")

def check_mmcv():
    print(f"\nMMCV version: {mmcv.__version__}")
    try:
        from mmcv.ops import nms_rotated
        print("MMCV Ops: Available")
    except ImportError:
        print("ERROR: MMCV Ops not available! MMCV might be installed without CUDA/ROCm support.")
    
    print(f"MMCV Compiler: {get_compiler_version()}")
    print(f"MMCV Compiling CUDA/ROCm version: {get_compiling_cuda_version()}")

def check_mmdet():
    print(f"\nMMDet version: {mmdet.__version__}")

if __name__ == "__main__":
    print("=== Checking ROCm Environment ===")
    check_rocm()
    check_mmcv()
    check_mmdet()
    print("=== Check Complete ===")
