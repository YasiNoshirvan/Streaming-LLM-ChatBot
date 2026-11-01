# 💬 Streaming LLM Chatbot

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![Groq](https://img.shields.io/badge/LLM-Groq-F55036) ![Transformers](https://img.shields.io/badge/Tokenizer-Transformers-FFD21E) ![Type](https://img.shields.io/badge/Type-Educational%20Project-informational)

A **terminal-based LLM chatbot** that streams responses from Groq as they arrive. Alongside basic conversation, it explores **message history, automatic summarization, token counting, and usage reporting**.

The goal is to understand the practical details of building a conversational application around an LLM API, beyond a single prompt-and-response call.

## ✨ Features

- **Streaming output:** Prints response text incrementally as it arrives from the API.
- **Conversation history:** Includes recent user and assistant messages in subsequent requests.
- **Automatic summarization:** Periodically compresses older messages using the LLM.
- **History trimming:** Limits how many raw messages remain in memory.
- **Prompt length check:** Uses a Hugging Face tokenizer to check input length.
- **Token tracking:** Counts API-reported prompt, completion, and total tokens.
- **Usage report:** Prints token totals and an illustrative cost estimate when the chat ends.

## 🔄 How it works

```text
User input
    |
    v
Prompt token check
    |
    v
Groq streaming completion
    |
    v
Display text as it arrives
    |
    v
Update token counters + conversation history
    |
    v
Summarize / trim older messages when needed
```

## 📂 Project files

```text
├── ChatBot.py      # Streaming, memory, token checks, and usage report
├── Pipfile
└── Pipfile.lock
```

## ⚙️ Run locally

```bash
git clone https://github.com/YasiNoshirvan/Streaming-LLM-ChatBot.git
cd Streaming-LLM-ChatBot
python -m pip install openai transformers python-dotenv
```

Create a local `.env` file:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Then run:

```bash
python ChatBot.py
```

Type `q` to end the session and print the usage report. The local Hugging Face tokenizer may need to be downloaded on the first run.

## ⚙️ Configuration

| Setting | Value in the script | Purpose |
| --- | --- | --- |
| `MODEL_NAME` | `openai/gpt-oss-20b` | Groq-hosted response model |
| `TOKENIZER_NAME` | `meta-llama/Llama-3.1-8B` | Local input token counting |
| `PROMPT_TOKEN_LIMIT` | `10` | Small learning/demo limit per user input |
| `DAILY_TOKEN_LIMIT` | `10,000` | Token budget for the **current run** |

## 📝 Limitations

The Hugging Face tokenizer is **not the exact tokenizer** used by the response model, so local input counts can differ from API usage. The code's "daily" token budget resets when the program restarts, and estimated cost uses example rates from the course rather than verified current pricing. Chat history is not persistent between runs.

---

*An educational LLM API project focused on streaming, conversational context, and token accounting.*
