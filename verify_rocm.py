import torch
import mmcv
import os
import sys

def verify():
    print(f"PyTorch Version: {torch.__version__}")
    print(f"PyTorch Debug Build: {torch.version.debug}")
    
    # Check ROCm/HIP status
    if hasattr(torch.version, 'hip'):
        print(f"ROCm/HIP Version: {torch.version.hip}")
    else:
        print("ROCm/HIP Version: None (This looks like a CPU or CUDA-only build!)")

    print(f"CUDA Available (mapped to HIP): {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device Count: {torch.cuda.device_count()}")
        print(f"Device Name: {torch.cuda.get_device_name(0)}")
    
    try:
        from mmcv.ops import get_compiler_version, get_compiling_cuda_version
        print(f"MMCV Compiler: {get_compiler_version()}")
        print(f"MMCV Compiled against CUDA/ROCm: {get_compiling_cuda_version()}")
    except ImportError:
        print("ERROR: MMCV Ops not available! MMCV might be installed without GPU support.")
    except Exception as e:
        print(f"Error checking MMCV: {e}")

    # Check for library files
    torch_lib_path = os.path.join(os.path.dirname(torch.__file__), 'lib')
    print(f"Checking libraries in {torch_lib_path}:")
    for lib in ['libc10_hip.so', 'libtorch_hip.so', 'libc10_cuda.so', 'libtorch_cuda.so']:
        path = os.path.join(torch_lib_path, lib)
        exists = os.path.exists(path)
        is_link = os.path.islink(path) if exists else False
        print(f"  {lib}: {'Found' if exists else 'Missing'} {'(Symlink)' if is_link else ''}")

    print("\n--- Environment Variables ---")
    for key in ['HSA_OVERRIDE_GFX_VERSION', 'ROCM_PATH', 'LD_LIBRARY_PATH', 'HIP_VISIBLE_DEVICES']:
        print(f"{key}: {os.environ.get(key, 'Not Set')}")

    print("\n--- Device Checks ---")
    print(f"/dev/dxg exists: {os.path.exists('/dev/dxg')}")
    print(f"/dev/kfd exists: {os.path.exists('/dev/kfd')}")
    print(f"/dev/dri exists: {os.path.exists('/dev/dri')}")

    print("\n--- rocminfo ---")
    try:
        os.system("rocminfo | grep 'Name:' | head -n 5")
    except:
        print("Failed to run rocminfo")

if __name__ == "__main__":
    verify()
