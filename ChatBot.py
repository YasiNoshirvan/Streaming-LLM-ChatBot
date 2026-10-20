import os
import time
import dotenv

from openai import OpenAI
from transformers import AutoTokenizer

dotenv.load_dotenv(dotenv.find_dotenv()) # Load environment variables from the .env file


MODEL_NAME = "openai/gpt-oss-20b" # Main model used through the Groq OpenAI-compatible API

TOKENIZER_NAME = "meta-llama/Llama-3.1-8B"  # Tokenizer used only for counting user prompt tokens

PROMPT_TOKEN_LIMIT = 10 # Maximum number of tokens allowed in a single user prompt

DAILY_TOKEN_LIMIT = 10_000  # Maximum API token usage allowed during the session


class ChatBot:

    def __init__(self):# Read the Groq API key from .env
                       # The second option supports the typo used in the instructor's code
        api_key = (os.getenv("GROQ_API_KEY") )

        # Stop immediately with a clear error if the API key is missing
        if not api_key:
            raise RuntimeError("Groq API key was not found. Add GROQ_API_KEY=your_key to the .env file.")

        self.llm = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")  #Create the OpenAI-compatible Groq client

        # Initial system prompt
        self.messages = [ {"role": "system",
                        "content": ("You are a helpful assistant.Your name is Yasaman. In the first response, introduce yourself.Give short and concise answers.")
            }]

        # Token usage counters
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0

        self.iteration = 0  # Counts successful conversation turns

        # Load tokenizer once instead of loading it on every chat loop
        print("Loading tokenizer...")

        self.encoding = AutoTokenizer.from_pretrained(
            TOKENIZER_NAME
        )

        print("Tokenizer loaded successfully.")


    def add_usage(self, usage): # Add API usage statistics to the session counters
        if usage is None:
            return

        self.total_tokens += usage.total_tokens
        self.input_tokens += usage.prompt_tokens
        self.output_tokens += usage.completion_tokens


    def trim_messages(self, max_number=10):  # Keep system messages and only the latest conversation messages

        system_messages = [message for message in self.messages if message["role"] == "system" ]

        other_messages = [message for message in self.messages if message["role"] != "system" ]

        if len(other_messages) <= max_number:   # No trimming is needed when the history is still short
            return

        # Keep only the most recent non-system messages
        trimmed_messages = other_messages[-max_number:]

        self.messages = [*system_messages,*trimmed_messages]

        print("[Conversation history trimmed]")


    def summarize_messages(self): # Summarize conversation history every 5 successful turns

        if self.iteration % 5 != 0:
            return

        system_messages = [message for message in self.messages if message["role"] == "system"]

        other_messages = [message for message in self.messages if message["role"] != "system"]

        # Avoid summarization when there are not enough messages
        if len(other_messages) < 5:
            return

        # Split old and recent conversation history
        early_messages = other_messages[:5]
        last_messages = other_messages[5:]

        # Ask the LLM to summarize older conversation messages
        response = self.llm.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.5,
            messages=[{"role": "system", "content": ("Summarize these messages concisely, keeping key facts and important information." )},
                *early_messages
            ]
        )

        # Count tokens consumed by the summarization request too
        self.add_usage(response.usage)

        summarized_message = {"role": "system", "content": ("Summary of earlier conversation: " f"{response.choices[0].message.content}")}

        # Replace old messages with the generated summary
        self.messages = [*system_messages, summarized_message, *last_messages]

        print("[Conversation history summarized]")


    def bot(self, message):  # Add the current user message to conversation memory
        self.messages.append( {"role": "user", "content": message})

        # Request a streamed response from the LLM
        response = self.llm.chat.completions.create(
            model=MODEL_NAME,
            messages=self.messages,
            temperature=0.7,
            stream=True,
            stream_options={
                "include_usage": True
            }
        )

        response_text = ""

        # Read and display the response token by token
        for chunk in response:

            if chunk.choices:

                delta = chunk.choices[0].delta.content

                if delta:
                    print(delta, end="", flush=True)

                    response_text += delta

                    time.sleep(0.05) # Small delay creates a visible typing effect

           
            usage = getattr(chunk,"usage",None)   # Usage normally appears in the final streaming chunk

            if usage:
                self.add_usage(usage)

        print()

        # Store the assistant response in conversation memory
        self.messages.append({"role": "assistant","content": response_text })

        # Periodically compress old conversation history
        self.summarize_messages()

        # Prevent raw conversation history from growing indefinitely
        self.trim_messages(max_number=10)

        return response_text


    def chat(self): # Main interactive conversation loop

        while True:

            user_input = input('Ask something (type "q" to terminate): ' ).strip()

            # Stop the chatbot when the user enters q
            if user_input.lower() == "q":
                print("Good Luck! Bye!")
                break

            token_count = len(self.encoding.encode(user_input, add_special_tokens=False) ) # Count tokens in the current user prompt

            print(f"Prompt tokens: {token_count}")

            
            if token_count > PROMPT_TOKEN_LIMIT:        # Reject prompts that exceed the per-prompt limit
                print("Your prompt exceeded the limit.Try a shorter one please."  )
                continue

            
            if self.total_tokens >= DAILY_TOKEN_LIMIT:     #Stop when the total token budget has been consumed
                print("Unfortunately, you have exceeded the total token limit for today.")
                break

            self.iteration += 1  #Count only accepted conversation turns

            self.bot(user_input)   # Generate and stream the assistant response

      
            if self.total_tokens >= DAILY_TOKEN_LIMIT:      # Stop immediately if this response crossed the budget
                print("\nDaily token budget reached.")
                break


    def report(self): # Print the final conversation memory and usage statistics

        print("\n Conversation Memory ")

        for message in self.messages:
            print(message)

        print("\n Usage Report")

        print(f"Total tokens used: {self.total_tokens}")

        print(f"Input tokens: {self.input_tokens}")

        print(f"Output tokens: {self.output_tokens}")

        # Estimate cost using the prices given in the course example
        estimated_cost = ( self.input_tokens * 0.05 + self.output_tokens * 0.08) / 1_000_000

        print(f"Estimated cost: ${estimated_cost:.8f}")


def main():   # Create the chatbot and start the interactive session
    bot = ChatBot()
    bot.chat()
    bot.report()


if __name__ == "__main__":
    main()