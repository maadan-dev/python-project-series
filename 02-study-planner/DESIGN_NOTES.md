# Design Notes

This document describes the assumptions, promises, and current boundaries of the Study Planner AI Agent.

## Assumptions

### API

* A valid Groq API key exists in the environment.
* The API key is stored in a `.env` file and loaded using `python-dotenv`.
* The configured Groq model is available to the account.
* The Groq API is reachable when a message is sent.
* The API returns a response containing at least one choice.

### Conversation history

* `history.json` contains valid JSON when it exists.
* The stored history follows the message structure expected by the Groq chat API.
* The history file is accessible and writable.
* Conversation history can be stored locally as plain JSON.
* The entire conversation can be sent to the model for each request.

### Agent

* The `Agent` object is responsible for maintaining the current conversation.
* The system instruction is intended to remain at the beginning of the conversation.
* The model can use previous messages to maintain conversational context.

### CLI

* The user interacts with the application through a terminal.
* User input is provided as text.
* Commands such as `/reset`, `/help`, and `/topics` are entered exactly as expected.

## Promises

### Conversation

The `Agent` promises that:

* User messages are added to the conversation history.
* Successful assistant responses are added to the conversation history.
* The updated conversation is saved after a successful response.
* Existing conversation history is loaded when the agent starts.
* `/reset` replaces the existing conversation with a new system instruction.

### API errors

The `chat()` method catches exceptions raised during the API request and displays an error message instead of allowing the application to immediately crash.

### Topic extraction

`get_topic()` creates a temporary version of the conversation history and asks the model to identify topics discussed by the user.

The temporary topic request does not modify the stored conversation history.

### Storage

`save_history()` serializes the provided conversation history into `history.json`.

`load_history()` returns:

* The stored history if the file exists.
* An empty list if the file does not exist.

## Will Not Handle

### API failures

The current version does not provide specialized handling for:

* Invalid API keys.
* Expired API keys.
* Rate limits.
* Network failures.
* API timeouts.
* Model availability errors.
* Different API error types.

All exceptions from `chat()` are currently handled by the same general error message.

### Conversation history

The application does not currently handle:

* Corrupted `history.json`.
* Invalid JSON.
* Invalid message structures.
* Very large conversation histories.
* Automatic history summarization.
* Token limits.
* Database-backed memory.
* Multiple users or separate conversations.

Because the complete conversation history is sent to the model, a sufficiently long conversation could eventually exceed the model's context limits.

### AI responses

The application does not guarantee:

* That the AI gives correct information.
* That generated study plans are appropriate.
* That the model actually searches the internet.
* That topics returned by `/topics` are complete or accurate.

The system instruction tells the agent it can search the internet when necessary, but no explicit search tool is currently implemented.

### Commands

The CLI does not currently handle:

* Command arguments.
* Command aliases.
* Case-insensitive slash commands.
* Unknown slash commands separately from normal messages.
* A structured command parser.

For example, `/RESET` will not trigger the same behavior as `/reset`.

### Security

The current version does not provide:

* User authentication.
* Authorization.
* Encryption of conversation history.
* Secure multi-user storage.
* API key management beyond using an environment variable.

The `.env` file must remain private and should not be committed to the repository.

### Storage failures

The application does not currently handle:

* Permission errors when writing `history.json`.
* Disk failures.
* Concurrent writes.
* Corrupted history files.

## Design Decisions

### JSON for conversation memory

JSON was chosen because the project is small and the chat API already represents messages as dictionaries containing `role` and `content`.

This makes the API conversation structure easy to persist directly.

### Local persistent history

The application stores the conversation locally instead of using a database.

This keeps the project simple while demonstrating persistent state.

### Agent class

The `Agent` class groups together:

* The Groq client
* Model configuration
* Conversation history
* Chat behavior
* Reset behavior
* Topic extraction

This keeps the AI-related state and behavior together rather than putting everything inside `main.py`.

### Temporary history for `/topics`

The topic request uses:

```python
temp_history = self.history + [...]
```

instead of directly modifying `self.history`.

This means the instruction asking the model to list topics is not permanently added to the conversation.

## Current Boundary

The project is an early experiment with AI-powered applications.

It demonstrates the basic loop:

```text
User
 ↓
CLI
 ↓
Agent
 ↓
Groq API
 ↓
AI response
 ↓
Conversation history
 ↓
JSON storage
```

It is not yet a production AI agent.

The next projects in the series can progressively introduce stronger APIs, databases, structured data, authentication, asynchronous processing, retrieval, and more advanced AI system design.
