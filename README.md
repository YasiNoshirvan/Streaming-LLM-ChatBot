# Streaming LLM Chatbot with Memory and Token Management

A command-line chatbot built in Python using the Groq OpenAI-compatible API.

The project demonstrates how to build a conversational LLM application with streaming responses, conversation memory, automatic history summarization, token counting, usage limits, and estimated API cost tracking.

## Features

- Streaming LLM responses token by token
- Conversation history and contextual memory
- Automatic summarization of older messages
- Conversation history trimming
- Prompt token counting using a Llama 3.1 tokenizer
- Maximum token limit for individual prompts
- Session-wide token budget
- Input, output, and total token usage tracking
- Estimated API cost calculation
- Environment-based API key management
- Groq OpenAI-compatible API integration

## How It Works

The chatbot maintains a list of conversation messages containing system, user, and assistant messages.

Each user message is added to the conversation history before being sent to the LLM. The assistant response is streamed incrementally and stored in the conversation memory after generation.

To prevent the context from growing indefinitely, the application periodically summarizes older messages and trims the raw conversation history while preserving the most relevant recent context.

The application also tracks token usage and prevents prompts or sessions from exceeding predefined token limits.

## Architecture

```text
User Input
    |
    v
Token Counting
    |
    v
Prompt Limit Check
    |
    v
Conversation Memory
    |
    v
Groq OpenAI-Compatible API
    |
    v
Streaming Response
    |
    v
Store Assistant Response
    |
    +----> Periodic Summarization
    |
    +----> History Trimming
    |
    v
Token Usage Tracking
