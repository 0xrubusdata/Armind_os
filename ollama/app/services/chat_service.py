import json
import asyncio
from typing import List, Dict, Any, AsyncGenerator
import logging

from app.models.request import ChatRequest
from app.core.logging import logger
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)

class ChatService(BaseService):
    """Service for handling chat-related operations."""

    async def process_chat(self, request: ChatRequest) -> Dict[str, Any]:
        """
        Process a chat request with the Ollama model.

        Args:
            request: The chat request containing messages, model, and optional tools

        Returns:
            The processed chat response

        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        try:
            await self.log_request(
                "chat",
                model=request.model,
                messages=request.messages,
                tools=request.tools
            )
            
            # Prepare the request data
            data = {
                "model": request.model,
                "messages": [msg.dict() for msg in request.messages],
                "stream": False
            }
            
            # Add optional parameters if provided
            if request.options:
                data["options"] = request.options
            if request.format:
                data["format"] = request.format
                
            # Call the Ollama API
            response = await self.call_ollama_api("chat", data)
            return await self.handle_ollama_response(response)

        except Exception as e:
            logger.error(f"Error in chat service: {str(e)}")
            raise
            
    async def process_chat_stream(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """
        Process a streaming chat request with the Ollama model.

        Args:
            request: The chat request containing messages, model, and optional tools

        Yields:
            The streaming chat response

        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        try:
            await self.log_request(
                "chat_stream",
                model=request.model,
                messages=request.messages,
                tools=request.tools
            )
            
            # Prepare the request data
            data = {
                "model": request.model,
                "messages": [msg.dict() for msg in request.messages],
                "stream": True
            }
            
            # Add optional parameters if provided
            if request.options:
                data["options"] = request.options
            if request.format:
                data["format"] = request.format
                
            # Stream from the Ollama API
            async for chunk in self.stream_ollama_api("chat", data):
                # Check for tool calls in the response
                if "message" in chunk and chunk["message"].get("role") == "assistant":
                    content = chunk["message"].get("content", "")
                    if content and "```json" in content and "tool" in content:
                        # Extract the tool call
                        try:
                            tool_start = content.find("```json") + 7
                            tool_end = content.find("```", tool_start)
                            if tool_start > 7 and tool_end > tool_start:
                                tool_json = content[tool_start:tool_end].strip()
                                tool_data = json.loads(tool_json)
                                
                                if "tool" in tool_data and "endpoint" in tool_data and "params" in tool_data:
                                    # Execute the tool
                                    tool_result = await self.execute_tool(
                                        tool_data["tool"],
                                        tool_data["endpoint"],
                                        tool_data["params"]
                                    )
                                    
                                    # Add the tool result to the messages
                                    data["messages"].append({
                                        "role": "tool",
                                        "content": json.dumps(tool_result),
                                        "name": tool_data["tool"]
                                    })
                                    
                                    # Continue the conversation with the tool result
                                    async for new_chunk in self.stream_ollama_api("chat", data):
                                        yield json.dumps(new_chunk) + "\n"
                                    return
                        except Exception as e:
                            logger.error(f"Error processing tool call: {str(e)}")
                
                # Yield the chunk
                yield json.dumps(chunk) + "\n"

        except Exception as e:
            logger.error(f"Error in chat stream service: {str(e)}")
            yield json.dumps({"error": str(e)}) + "\n"