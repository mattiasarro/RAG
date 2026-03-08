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

## 4. Configure via the UI

* Profile > Admin Panel > Settings > Connections > OpenAI API - `disable` 
  * (Otherwise there will be an error about missing API token in the logs)
* Profile > Admin Panel > Settings > Documents > Embedding
  * Embedding Model Engine: `Ollama`
  * Embedding Model: `qwen3-embedding`
* Profile > Admin Panel > Settings > Documents > Retrieval
  * Hybrid Search: `enable`
  * Reranking Engine: `Default (SentenceTransformers)`
  * Reranking Model: `jinaai/jina-reranker-v2-base-multilingual`
      * This causes CrossEncoder: cannot import name 'create_position_ids_from_input_ids' due to incompatible transformers model.
      * So for now, set the value to be empty, which skips reranking.

## 5. Check that GPU(s) are being used

Run the following command (and keep it running in a separate terminal tab/pane when running the subsequent commands). Check the numbers under "Volatile GPU-Util" and "GPU Memory Usage". When creating the knowledge base (and calculating embedding vectors) or running a RAG pipeline (calculating embedding vectors, generating output based on RAG prompt), these numbers should rise.

```
watch nvidia-smi
```

## 6. Create a knowledge base

* Workspace > Knowledge > + New Knowledge > [fill out fields] > Create Knowledge
* + > Upload Directory > [select data/et_wiki_100]

## 7. Test out the RAG model

* Wait for embedding of data/et_wiki_100 to complete.
* New Chat
* Select qwen3.5:35b from the top-left dropdown.
* Write "Milline Twitteri kasutaja lõi NAFO?" to the text box (do NOT attach knowledge) and send the message. This executes the language model qwen3.5:35b without doing RAG over the added knowledge base, and is not able to answer the question.
* Write "Milline Twitteri kasutaja lõi NAFO?" to the text box (DO attach the knowledge base you just created via the + sign) and send the message. This runs a full RAG pipeline over the knowledge base we added and is able to answer the question.

## 8. Python environment setup (uv)

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (and ensure the uv executable is in PATH):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Scripts in `scripts/` use [PEP 723](https://peps.python.org/pep-0723/) inline dependency metadata, so `uv run` automatically creates an isolated virtual environment and installs the required packages — no manual `pip install` or `venv` setup needed.

If you prefer a traditional venv:

```bash
uv venv
source .venv/bin/activate
uv pip install httpx
```

## 9. Upload files to knowledge base via API

Instead of uploading files through the UI (step 6), you can use the `scripts/upload_to_knowledge.py` script to bulk-upload a directory of files to an Open WebUI knowledge base.

```bash
uv run scripts/upload_to_knowledge.py data/et_wiki_100 \
    --api-key $(uv run scripts/get_token.py --email user@example.com --password secret)
```

You can also omit `--password` to be prompted interactively.

This will create a knowledge base named `et_wiki_100` (after the directory), upload all files, wait for embedding to complete, and add them to the knowledge base.

Options:

```
--knowledge-name NAME   Custom knowledge base name (default: directory name)
--base-url URL          Open WebUI URL (default: http://localhost:3000)
```
