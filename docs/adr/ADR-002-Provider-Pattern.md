# ADR 002: Provider Pattern for LLMs

## Status
Accepted

## Problem
The intelligence pipeline relies heavily on Large Language Models (LLMs) to analyze articles, score business impact, and extract events. Relying on a single vendor (e.g., OpenAI) creates vendor lock-in, increases operational risk if the vendor experiences downtime, and limits our ability to use cost-effective local models for development.

## Decision
We will use the **Provider Pattern** for all LLM interactions. We define an abstract `BaseProvider` interface with an `analyze()` method. Implementations like `OpenAIProvider`, `AnthropicProvider`, or `MockProvider` will implement this interface.

## Alternatives Considered
- **Direct OpenAI SDK usage**: Tightly couples the codebase to OpenAI's specific JSON response formats and SDK objects, making it painful to switch later.
- **LangChain / LlamaIndex**: Powerful, but adds excessive bloat and abstraction layers that obscure the underlying prompts, which are the core IP of this intelligence engine.

## Consequences
- **Positive**: We can seamlessly switch to Anthropic Claude or local open-source models without changing a single line of business logic.
- **Positive**: Offline development is fully supported via the `MockProvider`.
- **Negative**: We must normalize outputs from different LLMs into a standardized `AnalysisResult` class, handling variations in how different models emit JSON.
