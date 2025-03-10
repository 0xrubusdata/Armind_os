import json
import asyncio
from typing import Dict, Any, AsyncGenerator
import logging

from app.models.request import GenerateRequest
from app.core.logging import logger
from app.services.base_service import BaseService

logger = logging.getLogger(__name__)

class GenerateService(BaseService):
    """Service for handling text generation operations."""

    async def process_generate(self, request: GenerateRequest) -> Dict[str, Any]:
        """
        Process a generate request with the Ollama model.

        Args:
            request: The generate request containing prompt, model, and optional tools

        Returns:
            The processed generation response

        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        try:
            await self.log_request(
                "generate",
                model=request.model,
                prompt=request.prompt,
                tools=request.tools
            )
            
            # Prepare the request data
            data = {
                "model": request.model,
                "prompt": request.prompt,
                "stream": False
            }
            
            # Add optional parameters if provided
            if request.system:
                data["system"] = request.system
            if request.template:
                data["template"] = request.template
            if request.context:
                data["context"] = request.context
            if request.options:
                data["options"] = request.options
            if request.format:
                data["format"] = request.format
                
            # Call the Ollama API
            response = await self.call_ollama_api("generate", data)
            return await self.handle_ollama_response(response)

        except Exception as e:
            logger.error(f"Error in generate service: {str(e)}")
            raise
            
    async def process_generate_stream(self, request: GenerateRequest) -> AsyncGenerator[str, None]:
        """
        Process a streaming generate request with the Ollama model.

        Args:
            request: The generate request containing prompt, model, and optional tools

        Yields:
            The streaming generation response

        Raises:
            OllamaError: If there's an error with the Ollama service
            ModelNotFoundError: If the specified model is not found
        """
        try:
            await self.log_request(
                "generate_stream",
                model=request.model,
                prompt=request.prompt,
                tools=request.tools
            )
            
            # Prepare the request data
            data = {
                "model": request.model,
                "prompt": request.prompt,
                "stream": True
            }
            
            # Add optional parameters if provided
            if request.system:
                data["system"] = request.system
            if request.template:
                data["template"] = request.template
            if request.context:
                data["context"] = request.context
            if request.options:
                data["options"] = request.options
            if request.format:
                data["format"] = request.format
                
            # Stream from the Ollama API
            async for chunk in self.stream_ollama_api("generate", data):
                # Check for tool calls in the response
                if "response" in chunk:
                    content = chunk["response"]
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
                                    
                                    # Continue the conversation with the tool result
                                    tool_prompt = f"{request.prompt}\n\nTool result: {json.dumps(tool_result)}"
                                    data["prompt"] = tool_prompt
                                    
                                    # Stream the continuation
                                    async for new_chunk in self.stream_ollama_api("generate", data):
                                        yield json.dumps(new_chunk) + "\n"
                                    return
                        except Exception as e:
                            logger.error(f"Error processing tool call: {str(e)}")
                
                # Yield the chunk
                yield json.dumps(chunk) + "\n"

        except Exception as e:
            logger.error(f"Error in generate stream service: {str(e)}")
            yield json.dumps({"error": str(e)}) + "\n"