"""LLM client with tool calling support."""

import json
import sys
from typing import Any

import httpx
from config import settings


class LLMClient:
    """Client for LLM API with tool calling."""

    def __init__(self):
        self.base_url = settings.llm_api_base_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_api_model
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=60.0,
        )

    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """
        Send a chat request to the LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions
            
        Returns:
            LLM response dict with 'content' and/or 'tool_calls'
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        try:
            response = self._client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]
        except httpx.ConnectError as e:
            return {"content": f"LLM service unavailable: connection refused"}
        except httpx.HTTPStatusError as e:
            return {"content": f"LLM error: HTTP {e.response.status_code} {e.response.reason_phrase}"}
        except Exception as e:
            return {"content": f"LLM error: {str(e)}"}

    def chat_with_tools(
        self,
        system_prompt: str,
        user_message: str,
        tools: list[dict],
        max_iterations: int = 5,
    ) -> str:
        """
        Chat with the LLM using tool calling loop.
        
        Args:
            system_prompt: System instructions
            user_message: User's input message
            tools: List of tool definitions
            max_iterations: Maximum tool calling iterations
            
        Returns:
            Final response text
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        
        for iteration in range(max_iterations):
            # Call LLM
            response = self.chat(messages, tools)
            
            # Check if LLM wants to call tools
            tool_calls = response.get("tool_calls", [])
            
            if not tool_calls:
                # LLM is done, return its response
                return response.get("content", "I'm not sure how to help with that.")
            
            # Execute tool calls and collect results
            tool_results = []
            for tool_call in tool_calls:
                function = tool_call.get("function", {})
                tool_name = function.get("name", "")
                tool_args_str = function.get("arguments", "{}")
                
                try:
                    tool_args = json.loads(tool_args_str) if tool_args_str else {}
                except json.JSONDecodeError:
                    tool_args = {}
                
                # Execute the tool
                result = self._execute_tool(tool_name, tool_args)
                
                # Debug output to stderr
                print(f"[tool] LLM called: {tool_name}({tool_args})", file=sys.stderr)
                print(f"[tool] Result: {result}", file=sys.stderr)
                
                tool_results.append({
                    "tool_call_id": tool_call.get("id", ""),
                    "role": "tool",
                    "name": tool_name,
                    "content": json.dumps(result) if not isinstance(result, str) else result,
                })
            
            # Add assistant's response and tool results to messages
            messages.append(response)
            messages.extend(tool_results)
            
            print(f"[summary] Feeding {len(tool_results)} tool result(s) back to LLM", file=sys.stderr)
        
        # Max iterations reached, ask LLM to summarize
        messages.append({
            "role": "system",
            "content": "Please provide a final answer based on the tool results above."
        })
        
        final_response = self.chat(messages)
        return final_response.get("content", "I encountered an error processing your request.")

    def _execute_tool(self, name: str, arguments: dict) -> Any:
        """Execute a tool by name with given arguments."""
        # Import here to avoid circular imports
        from services.lms_client import lms_client
        
        tool_map = {
            "get_items": lambda: lms_client.get_labs(),
            "get_learners": lambda: lms_client.get_learners(),
            "get_scores": lambda: lms_client.get_scores(arguments.get("lab", "")),
            "get_pass_rates": lambda: lms_client.get_pass_rates(arguments.get("lab", "")),
            "get_timeline": lambda: lms_client.get_timeline(arguments.get("lab", "")),
            "get_groups": lambda: lms_client.get_groups(arguments.get("lab", "")),
            "get_top_learners": lambda: lms_client.get_top_learners(
                arguments.get("lab", ""), 
                arguments.get("limit", 5)
            ),
            "get_completion_rate": lambda: lms_client.get_completion_rate(arguments.get("lab", "")),
            "trigger_sync": lambda: lms_client.trigger_sync(),
        }
        
        if name not in tool_map:
            return {"error": f"Unknown tool: {name}"}
        
        try:
            return tool_map[name]()
        except Exception as e:
            return {"error": str(e)}


# Global client instance
llm_client = LLMClient()
