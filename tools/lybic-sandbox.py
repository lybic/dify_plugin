import asyncio
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from lybic import LybicClient, ComputerUse, Sandbox

def _run_async(coro, timeout: int = 60):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=1) as ex:
            return ex.submit(lambda: asyncio.run(asyncio.wait_for(coro, timeout))).result()
    return asyncio.run(asyncio.wait_for(coro, timeout))

async def execute_action(org_id: str, api_key: str, endpoint:str, sandbox_id: str, action: str, provider:str):
    async with LybicClient(org_id=org_id, api_key=api_key, endpoint=endpoint) as client:
        computer_use = ComputerUse(client)
        sandbox = Sandbox(client)

        computer_use_action =  await computer_use.parse_model_output(
            model=provider,
            textContent=action
        )
        for action in computer_use_action.actions:
            await sandbox.execute_computer_use_action(sandbox_id=sandbox_id, action=action)
        return computer_use_action.model_dump()


class LybicSandboxTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the tool to execute a pyautogui-style action in a Lybic sandbox.
        """
        provider = tool_parameters.get("grounding_provider")
        sandbox_id = tool_parameters.get("sandbox_id")
        action = tool_parameters.get("action")

        if not provider or not sandbox_id or not action:
            raise ValueError("Error: grounding_provider, sandbox_id and action are required.")

        # WARNING: Using eval on untrusted input is a security risk.
        # The 'action' parameter should be carefully validated or sanitized
        # in a real-world application.
        if not action.startswith("pyautogui."):
            raise Exception("Error: action must be a pyautogui call.")

        org_id = self.runtime.credentials.get("lybic_organization_id")
        api_key = self.runtime.credentials.get("lybic_api_key")
        endpoint = self.runtime.credentials.get("lybic_api_endpoint", "https://api.lybic.cn")

        if not org_id or not api_key:
            raise ToolProviderCredentialValidationError("Error: Lybic credentials are not configured.")

        try:
            result = _run_async(execute_action(org_id=org_id,
                                                     api_key=api_key,
                                                     endpoint=endpoint,
                                                     sandbox_id=sandbox_id,
                                                     action=action,
                                                     provider=provider))
            yield self.create_json_message({
                "status": "success",
                "result": result
            })
        except Exception as e:
            raise Exception(f"Error executing action: {e}")
