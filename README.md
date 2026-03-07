# RAG with Ollama & Open WebUI

## 1. Clone the repo

```bash
git clone git@github.com:andresgavriljuk/RAG.git
cd RAG
```

## 2. Install NVIDIA drivers (Ubuntu)

```bash
sudo apt update
sudo apt install -y nvidia-driver-560
sudo reboot
```

After reboot, verify the driver is working:

```bash
nvidia-smi
```

Install the NVIDIA Container Toolkit so Docker can access the GPU:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## 3. Start the services

```bash
docker compose up -d
```

Pull the required models:

```bash
docker compose exec ollama ollama pull qwen3.5:35b
docker compose exec ollama ollama pull qwen3-embedding
```

Open WebUI is now available at [http://localhost:3000](http://localhost:3000).
