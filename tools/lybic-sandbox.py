import asyncio
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from lybic import LybicClient, Pyautogui


class LybicSandboxTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the tool to execute a pyautogui-style action in a Lybic sandbox.
        """
        sandbox_id = tool_parameters.get("sandbox_id")
        action = tool_parameters.get("action")

        if not sandbox_id or not action:
            raise Exception("Error: sandbox_id and action are required.")

        # WARNING: Using eval on untrusted input is a security risk.
        # The 'action' parameter should be carefully validated or sanitized
        # in a real-world application.
        if not action.startswith("pyautogui."):
            raise Exception("Error: action must be a pyautogui call.")

        org_id = self.runtime.credentials.get("lybic_organization_id")
        api_key = self.runtime.credentials.get("lybic_api_key")

        if not org_id or not api_key:
            raise ToolProviderCredentialValidationError("Error: Lybic credentials are not configured.")

        client = LybicClient(
            org_id=org_id,
            api_key=api_key,
            endpoint=self.runtime.credentials.get("lybic_api_endpoint","https://api.lybic.cn")
        )
        pyautogui = Pyautogui(client, sandbox_id)

        try:
            # Execute the action string in a context where 'pyautogui' is defined.
            result = eval(action, {"pyautogui": pyautogui})
            yield self.create_json_message({
                "status": "success",
                "result": str(result) if result is not None else "action has no return value"
            })
        except Exception as e:
            raise Exception(f"Error executing action: {e}")
        finally:
            # It's important to clean up the resources.
            pyautogui.close()
            # LybicClient.close() is an async method.
            asyncio.run(client.close())
