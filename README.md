# Causal Conversation Analyzer

A multi-turn, context-aware system for **causal analysis over conversational data**. It explains why customers experience issues based on transcripts, provides evidence-backed explanations, and maintains chat memory for follow-up queries.

## Features

- Evidence-based causal explanations citing transcript IDs
- Multi-turn query support with conversation memory
- Domain-level statistics and structured feature analysis
- Works offline with **Llama3 / Phi3**
- Supports online LLM APIs (e.g., Gemini) if API key is provided
- Streamlit-based chat interface

## Project Structure

```
pravaah2026-iit-bbsr/
├── app.py                    # Streamlit frontend (chat interface)
├── pipeline.py               # Orchestrates retrieval, reasoning, and memory
├── retriever.py              # Transcript search & FAISS embeddings
├── reasoning.py              # Generates explanations using LLM (offline or API)
├── features.py               # Extracts structured features from transcripts
├── analytics.py              # Computes domain-level statistics
├── causal.py                 # Detect causal patterns
├── memory.py                 # Multi-turn chat memory
├── data/                     # JSON transcripts
├── models/                   # Offline LLMs/embeddings
├── output                    # contains outputs of system required for judgement
├── precompute.py             # Optional preprocessing scripts
├── generate_queries_csv.py   # Automates generating Output csv file of different queries
├── hackathon_queries.csv     # output csv file of different domain queries
├── output.csv                # A copy/backup of queries_output.csv
├── README.md
├── requirements.txt
└── pycache_/                 # Auto-generated Python cache
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/balabhadra3141/pravaah2026-iit-bbsr.git
cd pravaah2026-iit-bbsr.git
```

### 2. Create a virtual environment

```bash
python -m venv myenv
```

Windows:

```bash
myenv\Scripts\activate
```

Linux / macOS:

```bash
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Offline LLM Setup (default)

1. Download and install Ollama: `https://ollama.com`
2. Pull the Phi3 model:

```bash
ollama pull phi3
```

Run the system without API keys; offline reasoning will use Phi3 locally. \
**Note:** Offline LLMs like Phi3 require proper hardware — ideally GPU-enabled machine with sufficient VRAM for reasonable performance. On CPU-only machines, response times may be very long.

## Online LLM Setup (optional)

1. Obtain a Gemini API key from `https://ai.google.com/studio`
2. Set your environment variable:

Windows:

```bash
set GEMINI_API_KEY=YOUR_API_KEY
```

Linux / macOS:

```bash
export GEMINI_API_KEY=YOUR_API_KEY
```

The system will automatically use the online API if the key is detected.

## Run the Streamlit App

```bash
streamlit run app.py
```

---
## Repository & Running Ports

- **GitHub Repository:** [https://github.com/balabhadra3141/pravaah2026-iit-bbsr](https://github.com/yourusername/causal-conversation-analyzer)

- **Default Ports:**
  - **Ollama API / Local LLM:** `http://localhost:11434`  
    *(Ensure Ollama is running and Phi3 model is loaded)*
  - **Streamlit App:** `http://localhost:8501`  

> Tip: First start Ollama to serve the model if running offline, then run the Streamlit app. The app will connect to Ollama on port 11434 to generate explanations.

---
## Usage

Type an analytical query in the chat box, for example:

```
Why are customers escalating in healthcare calls?
```

The system will:

- Retrieve relevant transcripts
- Analyze structured features and domain-level statistics
- Return a structured explanation:
  - Key Causes
  - Evidence (quotes + transcript IDs)
  - Explanation

Ask follow-up queries; the system remembers prior chat context and responds accordingly.

## Deliverables

- Task 1: Single-query causal explanation
- Task 2: Multi-turn interactive reasoning
- Query dataset (`.csv`) covering multiple domains and intents
- Structured outputs referencing transcript IDs
- Fully reproducible environment (offline and online LLM support)

