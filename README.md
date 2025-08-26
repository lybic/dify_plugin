# 📦 lybic sandbox - A cloud-based sandbox operating environment for Ai Agent

- **Plugin ID** : lybic/sandbox_tools
- **Author** : lybic
- **Version** : 0.0.1
- **Type:** : tool
- **Repository** : https://github.com/lybic/dify_plugin
- **Marketplace** : https://marketplace.dify.ai/plugins/lybic/sandbox_tools

## Description

🌃 ** Infrastructure Tools **

Lybic is the infrastructure layer for your GUI agents.

**Lybic** (/ˈlaɪbɪk/) provides a robust, on-demand infrastructure platform designed specifically for the AI agent development lifecycle. This tool for dify is your command center for programmatically controlling the entire Lybic ecosystem, empowering you to build, test, and scale your agents with unprecedented speed and simplicity.

🚀 **Introduction and Mission**

Lybic provides a cutting-edge infrastructure solution for AI agents. Through our cloud-based sandbox environments (including virtual computers, mobile devices, and containers), we offer **out-of-the-box GUI operation capabilities**. This infrastructure, accessible via standard MCP, SDKs, and RESTful APIs, resolves critical challenges in GUI interaction, resource hosting, and high-concurrency execution.

Our self-developed **Grounding Inference Framework** empowers agents not just to "operate" interface elements, but to truly "understand" screen content, enabling autonomous decision-making in complex digital environments. Our mission is to provide the foundational tools that allow developers to focus on building intelligent agents, not on the underlying infrastructure.

##  🛠️ Bundled Tools

### ActionExecutor

This is a tool that allows LLM/User to perform [computer-use](https://platform.openai.com/docs/guides/tools-computer-use),
mobile-use and container-use-like capabilities on the sandbox.

#### pyautogui style action

Input: a sandbox_id and an action(pyautogui-like action) to execute.

```json
{
  "sandbox_id": "BOX-01K3JQN3BVRVHXTAM3N60C76AD",
  "action": "pyautogui.click(x=10,y=10,clicks=2)"
}
```

Output:

```json
{
  "text": "",
  "files": [],
  "json": [
    {
      "result": "action has no return value",
      "status": "success"
    }
  ]
}
```

pyautogui style supported functions:

| Function | Supported | Notes |
| :--- | :---: | :--- |
| `position()` | ✅ | |
| `moveTo()` | ✅ | |
| `move()` | ✅ | |
| `click()` | ✅ | |
| `doubleClick()` | ✅ | |
| `write()` | ✅ | |
| `press()` | ✅ | Supports single key and list of keys. |
| `hotkey()` | ✅ | |
| `keyDown()` | ❌ | Not supported by Lybic API. |
| `keyUp()` | ❌ | Not supported by Lybic API. |


### ScreenshotViewer

This is a tool that allows LLM/User to view the screenshot of the sandbox.

input: a sandbox_id

output: a dify image object that can be viewed in dify other tools.

```json
{
  "text": "",
  "files": [
    {
      "dify_model_identity": "__dify__file__",
      "id": null,
      "tenant_id": "61ffc0ed-321a-4c8a-9bb9-93918b241cae",
      "type": "image",
      "transfer_method": "tool_file",
      "remote_url": "https://192.0.2.3/b488aea8e87445739b25f451c893e5c9.webp",
      "related_id": "8bec8591-d2f8-450f-869f-7844ba10ce11",
      "filename": "b488aea8e87445739b25f451c893e5c9.webp",
      "extension": ".webp",
      "mime_type": "image/webp",
      "size": 32144,
      "url": "http://192.0.2.58/files/tools/8bec8591-d2f8-450f-869f-7844ba10ce11.webp?timestamp=1756199657&nonce=13cd3132de500433807fae5dcc054f04&sign=9tzNzyWwQWD4f2NDLAvZs96RKDEpY0O0-Q2IscM57-s="
    }
  ],
  "json": [
    {
      "data": []
    }
  ]
}
```
