# Streaming LLM Chatbot with Memory & Token Management 🤖💬

A Python-based conversational chatbot built on the **Groq OpenAI-compatible API**, with support for streaming responses, conversation memory, automatic history summarization, token-budget control, and API usage tracking.

The project was developed as an AI Engineering exercise focused on understanding how real-world LLM applications manage context, memory, streaming generation, and token usage.

---

## 🌍 Overview

Large Language Model applications need more than a single API request to behave like real conversational systems.

This project implements a stateful command-line chatbot that preserves previous messages, streams generated responses in real time, periodically summarizes older conversation history, and controls token usage.

The chatbot connects to an LLM through Groq's OpenAI-compatible API and uses a Hugging Face tokenizer to estimate prompt length before requests are sent.

The pipeline includes:

- LLM API integration
- Stateful conversation memory
- Streaming response generation
- Automatic conversation summarization
- History trimming
- Prompt token counting
- Session token-budget enforcement
- API usage monitoring
- Estimated cost calculation
- Secure environment-variable management

---

## 🎯 Objectives

The main objectives of this project are:

- Build a conversational chatbot connected to an external LLM.
- Preserve previous conversation context across multiple turns.
- Prevent conversation history from growing indefinitely.
- Summarize older messages while retaining important information.
- Stream generated responses progressively to the terminal.
- Count prompt tokens before sending requests.
- Enforce per-prompt and session-wide token limits.
- Track input, output, and total API token usage.
- Estimate API cost based on configurable token rates.

---

## 🧠 Conversation Memory

The chatbot stores the conversation using the standard chat-message structure:

```python
{
    "role": "user",
    "content": "Hello"
}
