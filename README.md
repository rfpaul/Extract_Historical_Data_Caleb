# About
This repo stores the Python scripting tools to facilitate the digitization of historical documents directly into machine-readable formats such as JSON or CSV using Microsoft's Phi-3.5-Vision-Instruct vision language model.

# Installation Instructions for Phi-3.5-Vision-Instruct
## (Windows 11, CUDA v12):

Download and unzip `vips-dev-w64-all-8.16.1.zip` from <https://github.com/libvips/build-win64-mxe/releases/tag/v8.16.1>

Move the `vips-dev-8.16` directory to a convenient, permanent place on your C drive. Search your computer from the Windows menu for `Edit environmental variables for your account.` Add the `…\vips-dev-8.16\bin` directory in your Windows Path variables.

Download and install Miniconda from <https://www.anaconda.com/download/success>, then, in the Anaconda Power Shell:

```powershell
conda create -n Miniconda-Phi3_5-Viz pytorch einops torchvision torchaudio cudatoolkit transformers=4.49.0 einops accelerate pillow ninja pytorch-cuda=12.1 python=3.11 -c pytorch -c nvidia -c conda-forge
```

After the CUDA env creation:

```powershell
conda activate Miniconda-Phi3_5-Viz
pip install pyvips
```

Download `flash_attn-2.7.4.post1+cu124torch2.5.1cxx11abiFALSE-cp311-cp311-win_amd64.whl` (n.b., this specific build of Flash Attention is compatible on Windows 11 64-bit with CUDA version 12, Python version 3.11, and PyTorch version 2.5.1; check your version numbers with the commands `conda list` and `nvidia-smi` if it doesn't work)  from <https://github.com/kingbri1/flash-attention/releases>, then

```powershell
pip install C:\Users\[your_username]\Downloads\flash_attn-2.7.4.post1+cu124torch2.5.1cxx11abiFALSE-cp311-cp311-win_amd64.whl
```

As is typical for a Microsoft product, Phi-3.5-Vision-Instruct ships with bugs. Also, since this specific model is marked as deprecated, it's unlikely that they'll ever fix it. I forked Microsoft's original code and model weights on HuggingFace to [my own HF repo](https://huggingface.co/rfpaul/Phi-3.5-vision-instruct) with the bug fix for `modeling_phi3_v.py` per <https://huggingface.co/microsoft/Phi-3.5-vision-instruct/discussions/39/files>.

And you're finally ready to go! Make sure you run your scripts in the Miniconda-Phi3_5-Viz conda env; they won't work otherwise.

Tested and working for Windows 11/CUDA 12.8 on an NVIDIA RTX A2000 12GB