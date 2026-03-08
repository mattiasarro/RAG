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

## 10. Incremental knowledge base sync

Use `scripts/update_knowledge.py` to incrementally sync a versioned directory to a knowledge base. This avoids re-uploading unchanged files and is useful when documents are updated over time.

Expected directory structure:

```
data/versioned/et_wiki_10/
    2026-03-07/       # older snapshot
    2026-03-08/       # latest snapshot
    _sync_log.csv     # auto-generated sync history
```

Run the script:

```bash
uv run scripts/update_knowledge.py data/versioned/et_wiki_10 \
    --api-key $(uv run scripts/get_token.py --email user@example.com --password secret)
```

On the first run (no existing knowledge base), it creates one and uploads all files from the latest subdirectory.

On subsequent runs, it reads `_sync_log.csv` to find the last successfully synced directory and diffs it against the latest directory:

- **Added files** (in latest but not in previous) — uploaded and added
- **Removed files** (in previous but not in latest) — removed from knowledge base
- **Modified files** (same name, different md5 hash) — replaced in knowledge base
- **Unchanged files** — skipped

Each run appends a row to `_sync_log.csv` with the directory name, timestamp, and status (`completed` or `failed`).

You can test that this works with the following steps:

* Move one dir out `mv data/versioned/et_wiki_10/2026-03-08 2026-03-08`
* Run the above `update_knowledge.py` command.
* In OpenWebUI, ask the question "millal töötas Diego Maradonna Argentiina koondise peatreenerina?" (with et_wiki_10 attached as knowledge). The answer should be ~ "2008-2010".
* Move thr dir back `mv 2026-03-08 data/versioned/et_wiki_10/2026-03-08`
* Run the above `update_knowledge.py` command again. It should remove 3 documents and update one document "Diego Maradona.md".
* In OpenWebUI, ask the question "millal töötas Diego Maradonna Argentiina koondise peatreenerina?" (with et_wiki_10 attached as knowledge). The answer should be ~ "2006-2012".

## 11. Benchmark upload speed

To estimate how long it would take to upload an entire directory, use `scripts/benchmark_upload.py`. It samples `n` random files, uploads them to a temporary knowledge base, and extrapolates the total time.

```bash
uv run scripts/benchmark_upload.py data/et_wiki_100 --n 10 \
    --api-key $(uv run scripts/get_token.py --email user@example.com --password secret)
```

This will upload 10 random files from `data/et_wiki_100`, measure the elapsed time, and print the estimated time to process all files in the directory.

Options:

```
--n N               Number of files to sample (required)
--base-url URL      Open WebUI URL (default: http://localhost:3000)
```

The temporary knowledge base and temp directory are automatically cleaned up after the benchmark.

## 12. Scheduling sync with cron

To run `update_knowledge.py` on a schedule, set up a cron job.

### Store the API key

Create a file readable only by your user:

```bash
echo "YOUR_API_KEY_OR_JWT" > ~/.config/openwebui_api_key
chmod 600 ~/.config/openwebui_api_key
```

If you don't have an API key (API keys not enabled), you can store a long-lived JWT instead. Generate one and write it to the file:

```bash
uv run scripts/get_token.py --email user@example.com --password secret > ~/.config/openwebui_api_key
chmod 600 ~/.config/openwebui_api_key
```

Note: JWT tokens expire. If your token has a short lifetime, use `get_token.py` inline in the cron job instead or configure an API_KEY.

### Add the cron job

```bash
crontab -e
```

Run every hour:

```cron
0 * * * * cd /home/andresgavriljuk/RAG && $HOME/.local/bin/uv run scripts/update_knowledge.py data/versioned/et_wiki_10 --api-key "$(cat ~/.config/openwebui_api_key)" >> /var/log/update_knowledge.log 2>&1
```
