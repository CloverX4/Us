"""
agents/base.py
──────────────
BaseAgent — now provider-agnostic via LiteLLM.

LiteLLM translates every provider's API into one common format (OpenAI-style).
So the agent loop below works identically whether you're using Gemini, Groq,
Anthropic, OpenAI, or a local Ollama model.

The only thing that changes between providers is:
  - LLM_PROVIDER and LLM_MODEL in your .env
  - The matching API key

The agent loop itself never changes.
"""

import json
import os
import litellm
from typing import Any, Callable
from dataclasses import dataclass
from rich.console import Console
from config.settings import settings

console = Console()

# Set API keys for whichever provider is active
# LiteLLM reads these from environment variables automatically
os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key
os.environ["GEMINI_API_KEY"] = settings.gemini_api_key
os.environ["GROQ_API_KEY"] = settings.groq_api_key
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Suppress LiteLLM's verbose logging
litellm.set_verbose = False


@dataclass
class Tool:
    """
    A Python function exposed as an LLM tool.

    name:         What the LLM calls it
    description:  What the LLM reads to decide when/how to use it
    input_schema: JSON Schema for the arguments
    function:     The actual Python function to run
    """
    name: str
    description: str
    input_schema: dict
    function: Callable

    def to_litellm_format(self) -> dict:
        """LiteLLM uses OpenAI's tool format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema,
            }
        }


class BaseAgent:
    """
    Provider-agnostic base agent using LiteLLM.

    The agent loop:
      1. Send goal + tools to LLM
      2. If LLM calls a tool → execute it → add result → loop
      3. If LLM gives a final answer → return it

    Subclass this and define:
      - system_prompt property
      - register_tool() calls in __init__
    """

    def __init__(self):
        self._tools: list[Tool] = []
        self._max_iterations = 20

    @property
    def system_prompt(self) -> str:
        raise NotImplementedError

    def register_tool(self, tool: Tool):
        self._tools.append(tool)

    def run(self, goal: str, extra_context: dict | None = None) -> str:
        user_message = goal
        if extra_context:
            user_message += f"\n\n## Additional Context\n{json.dumps(extra_context, indent=2)}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        tools = [t.to_litellm_format() for t in self._tools]

        console.print(f"\n[bold cyan]{self.__class__.__name__}[/bold cyan] "
                       f"[dim]({settings.llm_model})[/dim]")

        for iteration in range(self._max_iterations):
            # ── Call LLM via LiteLLM ──────────────────────────────────────
            kwargs = dict(
                model=settings.llm_model,
                messages=messages,
                max_tokens=8096,
            )
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"

            response = litellm.completion(**kwargs)
            msg = response.choices[0].message

            # Add assistant turn to history
            messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})

            # ── Done? ─────────────────────────────────────────────────────
            if not msg.tool_calls:
                console.print(f"[bold green]Done[/bold green] ({iteration + 1} steps)")
                return msg.content or ""

            # ── Execute tool calls ────────────────────────────────────────
            for tc in msg.tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments or "{}")

                console.print(f"  [yellow]→[/yellow] {fn_name}({list(fn_args.keys())})")
                result = self._execute_tool(fn_name, fn_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result)
                })

        raise RuntimeError(f"Agent exceeded {self._max_iterations} iterations")

    def _execute_tool(self, name: str, args: dict) -> Any:
        for tool in self._tools:
            if tool.name == name:
                try:
                    return tool.function(**args)
                except Exception as e:
                    err = f"Tool '{name}' error: {e}"
                    console.print(f"  [red]{err}[/red]")
                    return err
        return f"Unknown tool: {name}"
