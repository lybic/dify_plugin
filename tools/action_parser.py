from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.model.message import SystemPromptMessage, UserPromptMessage
from dify_plugin.entities.tool import ToolInvokeMessage


class ActionParserTool(Tool):
    """
    This tool invokes an LLM to parse a natural language instruction into a pyautogui-style command.
    """

    # The prompt is a class variable.
    # We will define the prompt that will be sent to the LLM here.
    _prompt = """You are an expert in GUI automation. Your task is to convert a natural language instruction into a single, precise `pyautogui`-style command.

**Instructions:**
1.  Analyze the user's instruction carefully.
2.  Your output MUST be a single line of Python code representing the action.
3.  Do NOT add any explanations, comments, or any text other than the command itself.
4.  If the instruction is ambiguous, choose the most common and logical interpretation.
5.  Use the exact function names and syntax provided in the examples.

**Available Functions and Syntax:**
-   `pyautogui.moveTo(x, y)`
-   `pyautogui.click(x=None, y=None, button='left')`
-   `pyautogui.doubleClick(x=None, y=None)`
-   `pyautogui.rightClick(x=None, y=None)`
-   `pyautogui.dragTo(x, y, duration=0.0)`
-   `pyautogui.write('text')`
-   `pyautogui.press('key')`
-   `pyautogui.hotkey('ctrl', 'c')`

**Examples:**
-   User: "move the mouse to 100, 150" -> `pyautogui.moveTo(100, 150)`
-   User: "click the center of the screen" -> `pyautogui.click()`
-   User: "double click the icon" -> `pyautogui.doubleClick()`
-   User: "type hello world into the text field" -> `pyautogui.write('hello world')`
-   User: "press the enter key" -> `pyautogui.press('enter')`
-   User: "copy the selected text" -> `pyautogui.hotkey('ctrl', 'c')`
-   User: "right click at 250, 300" -> `pyautogui.rightClick(x=250, y=300)`
"""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        Invokes the LLM to parse the user's instruction.
        """
        instruction = tool_parameters.get('instruction', '')
        if not instruction:
            raise Exception("Error: Instruction is required.")
        response = self.session.model.llm.invoke(
            model_config=tool_parameters.get('model'),
            prompt_messages=[
                SystemPromptMessage(
                    content=self._prompt
                ),
                UserPromptMessage(
                    content=tool_parameters.get('instruction')
                )
            ],
            stream=False
        )

        for chunk in response:
            if chunk.delta.message:
                full_response = chunk.delta.message.content
                assert isinstance(full_response, str)

                command = full_response.strip().replace('```python', '').replace('```', '').strip()
                yield self.create_text_message(text=command)
