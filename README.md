# Fork DeepFaceLab

## Enverment

| Lib   | Version           |
|-------|-------------------|
| cuda  | 10.2.89           |
| cuda  | 11.8.0            |
| cudnn | 7.6.5.32_cuda10.2 |
| cudnn | 8.9.7.29_cuda11   |

## StartUp

1. Install

```bash
git clone https://github.com/BiBiNotFly/Fork_DeepFaceLab.git

cd Fork_DeepFaceLab

python3.7 -m venv venv

source ./venv/bin/activate 

pip install -r ./requirements.txt
```

2. Edit `env.sh`

```bash
vim scripts_linux/env.sh
```

change  **CUDA PATH** and **CUDNN PATH** for your.

```text
export CUDA_HOME_10=/DATA/sdk/cuda/cuda-10.2.89_440.33.01
export CUDNN_HOME_10=/DATA/sdk/cudnn/cudnn-7.6.5.32_cuda10.2

export CUDA_HOME_11=/DATA/sdk/cuda/cuda-11.8.0_520.61.05
export CUDNN_HOME_11=/DATA/sdk/cudnn/cudnn-8.9.7.29_cuda11
```

3. Test tensorflow

```bash
python test_torch_gpu.py 
```

4. Test torch

```bash
python test_torch_gpu.py 
```
