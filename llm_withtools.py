import json
import copy
from llm import create_client, get_response_from_llm
from tools import load_all_tools

DEEPSEEK_MODEL = 'deepseek-r1-0528'

def process_tool_call(tools_dict, tool_name, tool_input):
    """Process a tool call and return the result."""
    try:
        if tool_name in tools_dict:
            return tools_dict[tool_name]['function'](**tool_input)
        else:
            return f"Error: Tool '{tool_name}' not found"
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"

def chat_with_agent(msg, model=DEEPSEEK_MODEL, msg_history=None, logging=print):
    """Chat with agent that has access to mathematical tools."""
    if msg_history is None:
        msg_history = []
    
    # Load mathematical tools
    all_tools = load_all_tools(logging=logging)
    tools_dict = {tool['info']['name']: tool for tool in all_tools}
    
    # System message with tool descriptions
    tool_descriptions = "\n".join([
        f"- {tool['info']['name']}: {tool['info']['description']}"
        for tool in all_tools
    ])
    
    system_message = f"""You are a mathematical research agent with access to these tools:

{tool_descriptions}

To use a tool, respond with:
<tool_use>
{{
    "tool_name": "tool_name_here",
    "tool_input": {{...}}
}}
</tool_use>

Focus on rigorous mathematical research for ECDLP."""

    # Get response from LLM
    response, new_msg_history = get_response_from_llm(
        msg=msg,
        client=create_client(model)[0],
        model=model,
        system_message=system_message,
        msg_history=msg_history
    )
    
    logging(f"Response: {response[:200]}...")
    
    # Check for tool use
    while '<tool_use>' in response:
        # Extract tool call
        start = response.find('<tool_use>') + len('<tool_use>')
        end = response.find('</tool_use>')
        
        if end > start:
            try:
                tool_call = json.loads(response[start:end].strip())
                tool_name = tool_call.get('tool_name')
                tool_input = tool_call.get('tool_input', {})
                
                # Execute tool
                tool_result = process_tool_call(tools_dict, tool_name, tool_input)
                
                # Add tool result to conversation
                tool_msg = f"Tool '{tool_name}' returned:\n{tool_result}"
                
                # Get next response
                response, new_msg_history = get_response_from_llm(
                    msg=tool_msg,
                    client=create_client(model)[0],
                    model=model,
                    system_message=system_message,
                    msg_history=new_msg_history
                )
                
            except Exception as e:
                logging(f"Error processing tool call: {e}")
                break
        else:
            break
    
    return new_msg_history