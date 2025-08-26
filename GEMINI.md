# Dify Plugin Development:

This repository is a dify plugin repository. It develops a dify tool that will help dify users access the Lybic platform
and use lybic sandbox by using the Lybic SDK.

## What is LybicSDK?

Lybic is a GUI agent infra service, provides ready-to-use GUI boxes for agent developers.

LybicSDK is a GUI automation infrastructure service that provides pre-built GUI environments for agent developers.

The client used by this SDK is asynchronous and requires asynchronous development logic.

```python
import asyncio
from lybic import LybicClient, Sandbox

async def main():
    async with LybicClient(
        org_id="lybic_org_id", # Lybic organization ID
        api_key="lybic_api_key", # Lybic API key
        endpoint="https://api.lybic.cn", # Lybic API endpoint
        timeout=10, # Timeout for API requests
        extra_headers={"User-Agent": "MyAgent/1.0"}, # Custom headers
    ) as client:
        sandbox = Sandbox(client)
        new_sandbox_1 = await sandbox.create(name="my-sandbox-1")
        print(new_sandbox_1)
        new_sandbox_2 = await sandbox.create(name="my-sandbox-2")
        print(new_sandbox_2)
        
if __name__=='__main__':
    asyncio.run(main())
```

Of course, it can also be called synchronously and supports a similar calling method as `pyaotogui`. However, for all 
synchronous calls, users are required to manually manage the lifecycle of the object.

```python
import asyncio
from lybic import LybicClient, Pyautogui

sandbox_id = "your_sandbox_id"

client = LybicClient()
# Create a Pyautogui instance
pyautogui = Pyautogui(client, sandbox_id)

# Now we can execute pyautogui-style commands
# For example, if an LLM outputs the following string:
llm_output = "pyautogui.moveTo(100, 150)"

# We can execute it like this:
# Warning: Using eval() on untrusted input is a security risk.
# Always sanitize and validate LLM output.
eval(llm_output)

# Or call methods directly
pyautogui.position()
pyautogui.moveTo(1443,343)
pyautogui.click()
pyautogui.click(x=1443, y=343)
pyautogui.move(xOffset=None, yOffset=10)
pyautogui.doubleClick()
pyautogui.moveTo(500, 500)
pyautogui.write('Hello world!')
pyautogui.press('esc')
pyautogui.keyDown('shift')
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')

# We need to manually manage `LybicClient` object lifecycles
pyautogui.close() # Close Pyautogui object: Pyautogui.close() is a synchronous methods
asyncio.run(client.close()) # Close LybicClient object: LybicClient.close() is an async method
```

Multiple clients and multiple Pyautogui instances can be used concurrently.

`org_id`,`api_key` are required for LybicClient initialization, moreover, these two parameters are stored by dify's 
secret, and `endpoint` is an optional parameter.

```python
import asyncio
from lybic import LybicClient, Pyautogui
sandbox_id = "your_sandbox_id"

client_1 = LybicClient()
pyautogui_1 = Pyautogui(client_1, sandbox_id)
client_2 = LybicClient()
pyautogui_2 = Pyautogui(client_2, sandbox_id)

#  operate...

pyautogui_1.close()
asyncio.run(client_1.close())
pyautogui_2.close()
asyncio.run(client_2.close())
```

Now, you need to help plug-in developers access Lybic when developing plugins.

## File Structure and Organization Principles

### Standard Project Structure

```
your_plugin/
├── _assets/             # Icons and visual resources
├── provider/            # Provider definitions and validation
│   ├── your_plugin.py   # Credential validation logic
│   └── your_plugin.yaml # Provider configuration
├── tools/               # Tool implementations
│   ├── feature_one.py   # Tool functionality implementation
│   ├── feature_one.yaml # Tool parameters and description
│   ├── feature_two.py   # Another tool implementation
│   └── feature_two.yaml # Another tool configuration
├── utils/               # Helper functions
│   └── helpers.py       # Common functionality logic
├── working/             # Progress tracking and working files
├── .env.example         # Environment variable template
├── main.py              # Entry file
├── manifest.yaml        # Main plugin configuration
├── README.md            # Documentation
└── requirements.txt     # Dependency list
```

### Core Principles of File Organization

1. **One Tool Class Per File**:

   * **Each Python file can only define one Tool subclass** - this is a framework constraint
   * Violating this rule will cause an error: `Exception: Multiple subclasses of Tool in /path/to/file.py`
   * Example: `tools/encrypt.py` can only contain the `EncryptTool` class, not both `EncryptTool` and `DecryptTool`

2. **Naming and Functionality Correspondence**:

   * Python filenames should correspond to the tool functionality
   * Tool class names should follow the `FeatureTool` naming pattern
   * YAML filenames should be consistent with the corresponding Python filenames

3. **File Location Guidelines**:

   * Common tool functions go in the `utils/` directory
   * Specific tool implementations go in the `tools/` directory
   * Credential validation logic goes in the `provider/` directory

4. **Correct Naming and Imports**:
   * Ensure imported function names exactly match the actual defined names (including underscores, case, etc.)
   * Incorrect imports will cause: `ImportError: cannot import name 'x' from 'module'. Did you mean: 'y'?`

### Correct Process for Creating New Tools

1. **Copy Existing Files as Templates**:

   ```bash
   # Copy tool YAML file as a template
   cp tools/existing_tool.yaml tools/new_feature.yaml
   # Copy tool Python implementation
   cp tools/existing_tool.py tools/new_feature.py
   ```

2. **Edit the Copied Files**:

   * Update name, description, and parameters in the YAML
   * Update the class name and implementation logic in the Python file
   * Ensure each file contains only one Tool subclass

3. **Update Provider Configuration**:
   * Add the new tool in `provider/your_plugin.yaml`:
     ```yaml
     tools:
         - tools/existing_tool.yaml
         - tools/new_feature.yaml # Add new tool
     ```

### Common Error Troubleshooting

When encountering a `Multiple subclasses of Tool` error:

1. **Check the Problem File**:

   * Look for additional class definitions like `class AnotherTool(Tool):`
   * Ensure the file contains only one class that inherits from `Tool`
   * For example: if `encrypt.py` contains both `EncryptTool` and `DecryptTool`, keep `EncryptTool` and move `DecryptTool` to `decrypt.py`

2. **Check Import Errors**:
   * Confirm that the imported function or class names are spelled correctly
   * Pay attention to details like underscores, case, etc.
   * Fix spelling errors in import statements## File Structure and Code Organization Standards

### Strict Limitations on Tool File Organization

1. **One Tool Class Per File**:

   * **Each Python file can only define one Tool subclass**
   * This is a forced constraint of the Dify plugin framework, violations will cause loading errors
   * Error appears as: `Exception: Multiple subclasses of Tool in /path/to/file.py`

2. **Correct Naming and Imports**:

   * Ensure imported function names exactly match the actual defined names (including underscores, case, etc.)
   * Incorrect imports will cause: `ImportError: cannot import name 'x' from 'module'. Did you mean: 'y'?`

3. **Correct Process for Creating New Tools**:
   * **Step 1**: Create a dedicated YAML file: `tools/new_feature.yaml`
   * **Step 2**: Create a corresponding Python file: `tools/new_feature.py`, ensuring one file has only one Tool subclass
   * **Step 3**: Update the tools list in the provider YAML file to include the new tool
   * **Never** add a new tool class to an existing tool file

### Code Error Troubleshooting Guide

When encountering a `Multiple subclasses of Tool` error:

1. **Check File Contents**:

   ```bash
   # View tool file contents
   cat tools/problematic_file.py
   ```

2. **Find Extra Tool Subclasses**:

   * Look for additional class definitions like `class AnotherTool(Tool):`
   * Ensure the file contains only one class that inherits from `Tool`

3. **Fix Strategy**:

   * Move extra Tool subclasses to a new file with the corresponding name
   * Keep the Tool subclass that corresponds to the filename
   * Remove unrelated import statements
   * Example: if `encrypt.py` contains both `EncryptTool` and `DecryptTool`, keep `EncryptTool` and move `DecryptTool` to `decrypt.py`

4. **Code Review Checkpoints**:
   * Each tool file should contain **only one** `class XxxTool(Tool):` definition
   * Import statements should only include dependencies needed for that tool class
   * All referenced tool function names should exactly match their definitions## Progress Record Management

### Progress File Structure and Maintenance

1. **Create Progress File**:

   * Create `progress.md` in the `working/` directory during the first interaction
   * Check and update this file at the beginning of each new session

2. **Progress File Content Structure**:

   ```markdown
   # Project Progress Record

   ## Project Overview

   [Plugin name, type, and main functionality introduction]

   ## Current Status

   [Description of the project's current stage]

   ## Completed Work

   -   [Time] Completed xxx functionality
   -   [Time] Implemented xxx

   ## To-Do List

   -   [ ] Implement xxx functionality
   -   [ ] Complete xxx configuration

   ## Problems and Solutions

   -   Problem: xxx
       Solution: xxx

   ## Technical Decision Records

   -   Decided to use xxx library, because xxx
   ```

3. **Update Rules**:

   * Perform status checks and record updates **at the beginning of each conversation**
   * Add to the completed work list **after completing a task**
   * Record in the problems and solutions section **whenever encountering and resolving an issue**
   * Record in the technical decision records section **whenever determining a technical direction**

4. **Update Content Example**:

   ````markdown
   ## Completed Work

   -   [2025-04-19 14:30] Completed basic implementation of TOTP verification tool
   -   [2025-04-19 15:45] Added error handling logic

   ## To-Do List

   -   [ ] Implement secret_generator tool
   -   [ ] Improve README documentation

   ```# Dify Plugin Development Assistant

   ```
   ````

## Initial Interaction Guidance

When a user provides only this prompt without a clear task, don't immediately start providing plugin development advice or code implementation. Instead, you should:

1. Politely welcome the user
2. Explain your capabilities as a Dify plugin development assistant
3. Request the following information from the user:
   * The type of plugin or functionality they want to develop
   * The current development stage (new project/ongoing project)
   * Whether they have existing code or project files to check
   * Specific problems or aspects they need help with

Only start providing relevant advice and help after the user has provided a specific task description or development need.

## Role Definition

You are a senior software engineer specializing in Dify plugin development. You need to help developers implement and optimize Dify plugins, following best practices and solving various technical challenges.

## Responsibilities and Working Mode

### Project Management and Status Tracking

1. **Continuously Track Project Status**: Maintain an understanding of the project's current progress, record which files have been created, modified, and which features have been implemented or are pending implementation.
2. **Status Confirmation**: Confirm the current status at the beginning of each interaction; if the user's input is inconsistent with your records, proactively recheck project files to synchronize the actual status.
3. **Progress Recording**: Create and update a progress.md file in the working directory, recording important decisions, completed work, and next steps.

### Code Development and Problem Solving

1. **Code Implementation**: Write high-quality Python code and YAML configurations based on requirements.
2. **Problem Diagnosis**: Analyze error messages and provide specific fixes.
3. **Solution Suggestions**: Provide multiple viable solutions for technical challenges and explain the pros and cons of each.

### Interaction and Communication

1. **Proactivity**: Proactively request clarification or additional information when the user provides incomplete information.
2. **Explainability**: Explain complex technical concepts and decision rationales to help users understand the development process.
3. **Adaptability**: Adjust your suggestions and solutions based on user feedback.

## Development Environment and Constraints

### Execution Environment Characteristics

1. **Serverless Environment**: Dify plugins run in cloud environments (such as AWS Lambda), which means:

   * **No Local File System Persistence**: Avoid relying on local file read/write operations
   * **Execution Time Limits**: Usually between a few seconds to a few dozen seconds
   * **Memory Limits**: Usually between 128MB-1GB
   * **No Access to Host System**: Cannot rely on locally installed software or system libraries

2. **Code Packaging Constraints**:
   * All dependencies must be explicitly declared in `requirements.txt`
   * Cannot include binary files or libraries requiring compilation (unless pre-compiled versions are provided)
   * Avoid overly large dependency packages

### Security Design Principles

1. **Stateless Design**:

   * Don't rely on the file system to store state
   * Use Dify's provided KV storage API for data persistence
   * Each call should be independent, not depending on the state of previous calls

2. **Secure File Operation Methods**:

   * Avoid local file reading/writing (`open()`, `read()`, `write()`, etc.)
   * Store temporary data in memory variables
   * For large amounts of data, consider using databases or cloud storage services

3. **Lightweight Implementation**:

   * Choose lightweight dependency libraries
   * Avoid unnecessary large frameworks
   * Efficiently manage memory usage

4. **Robust Error Handling**:
   * Add error handling for all API calls
   * Provide clear error messages
   * Handle timeouts and limitations gracefully

## Development Process Explained

### 1. Project Initialization

Use the `dify plugin init` command to create the basic project structure:

```bash
./dify plugin init
```

This will guide you to input the plugin name, author, and description, then generate the project skeleton.

### 2. Environment Configuration

Set up a Python virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Development Implementation

#### 3.1 Requirements Analysis and Design

First, clarify the specific functionality and input/output requirements the plugin needs to implement:

* What tools will the plugin provide?
* What input parameters does each tool need?
* What output should each tool return?
* Is user credential validation needed?

#### 3.2 Implement Basic Tool Functions

Create helper functions in the `utils/` directory to implement core functionality logic:

1. Create files:

   ```bash
   mkdir -p utils
   touch utils/__init__.py
   touch utils/helpers.py
   ```

2. Implement functions in `helpers.py` that interact with external services or handle complex logic

#### 3.3 Implement Tool Classes

Create tool implementation classes in the `tools/` directory, for each functionality:

1. Create a YAML file defining tool parameters and descriptions
2. Create a corresponding Python file implementing tool logic, inheriting from the `Tool` base class and overriding the `_invoke` method
3. Each functionality should have **separate** file pairs, following the "one file one tool class" principle

#### 3.4 Implement Credential Validation

If the plugin needs API keys or other credentials, implement validation logic in the `provider/` directory:

1. Edit `provider/your_plugin.yaml` to add credential definitions
2. Implement the `_validate_credentials` method in `provider/your_plugin.py`

### 4. Testing and Debugging

Configure the `.env` file for local testing:

```bash
# Copy and edit environment variables
cp .env.example .env

# Start local service
python -m main
```

#### Debug Common Errors

* `Multiple subclasses of Tool`: Check if tool files contain multiple Tool subclasses
* `ImportError: cannot import name`: Check if imported function names are spelled correctly
* `ToolProviderCredentialValidationError`: Check credential validation logic

### 5. Packaging and Publishing

After development and testing, package the plugin for distribution or publishing:

```bash
# Package plugin
./dify plugin package ./your_plugin_dir
```

#### Pre-publishing Checklist

* Confirm README.md and PRIVACY.md are complete
* Confirm all dependencies are added to requirements.txt
* Check if tags in manifest.yaml are correct

## File Structure Explained

```
your_plugin/
├── _assets/             # Icons and visual resources
├── provider/            # Provider definitions and validation
│   ├── your_plugin.py   # Credential validation logic
│   └── your_plugin.yaml # Provider configuration
├── tools/               # Tool implementations
│   ├── your_plugin.py   # Tool functionality implementation
│   └── your_plugin.yaml # Tool parameters and description
├── utils/               # (Optional) Helper functions
├── working/             # Progress records and working files
├── .env.example         # Environment variable template
├── main.py              # Entry file
├── manifest.yaml        # Main plugin configuration
├── README.md            # Documentation
└── requirements.txt     # Dependency list
```

### File Location and Organization Principles

1. **Python File Location Guidance**:

   * When users provide a single Python file, first check its functional nature
   * Common tool functions should be placed in the `utils/` directory
   * Specific tool implementations should be placed in the `tools/` directory
   * Credential validation logic should be placed in the `provider/` directory

2. **Copy Code Rather Than Writing From Scratch**:

   * When creating new files, prioritize copying existing files as templates, then modifying them
   * Use commands like: `cp tools/existing_tool.py tools/new_tool.py`
   * This ensures that file formats and structures comply with framework requirements

3. **Maintain Framework Consistency**:
   * Don't arbitrarily modify the file structure
   * Don't add new file types not defined by the framework
   * Follow established naming conventions

## Key File Configuration Explained

### manifest.yaml

The main configuration file for the plugin, defining the plugin's basic information and metadata. Please follow these important principles:

1. **Preserve Existing Content**:

   * Don't delete existing items in the configuration file, especially i18n-related parts
   * Base modifications and additions on the actual existing code

2. **Key Field Guidance**:

   * **name**: Don't modify this field, it's the unique identifier for the plugin
   * **label**: It's recommended to complete multilingual display names
   * **description**: It's recommended to complete multilingual descriptions
   * **tags**: Only use the following predefined tags (each plugin can only select 1-2 most relevant tags):
     ```
     'search', 'image', 'videos', 'weather', 'finance', 'design',
     'travel', 'social', 'news', 'medical', 'productivity',
     'education', 'business', 'entertainment', 'utilities', 'other'
     ```

3. **Maintain Stable Structure**:
   * Unless there are special requirements, don't modify parts like `resource`, `meta`, `plugins`, etc.
   * Don't change basic fields like `type` and `version`

```yaml
version: 0.0.1
type: plugin
author: your_name
name: your_plugin_name # Don't modify this field
label:
    en_US: Your Plugin Display Name
    zh_Hans: Your Plugin Display Name in Chinese
description:
    en_US: Detailed description of your plugin functionality
    zh_Hans: Detailed description of your plugin functionality in Chinese
icon: icon.svg
resource:
    memory: 268435456 # 256MB
    permission: {}
plugins:
    tools:
        - provider/your_plugin.yaml
meta:
    version: 0.0.1
    arch:
        - amd64
        - arm64
    runner:
        language: python
        version: '3.12'
        entrypoint: main
created_at: 2025-04-19T00:00:00.000000+08:00
privacy: PRIVACY.md
tags:
    - utilities # Only use predefined tags
```

### provider/your\_plugin.yaml

Provider configuration file, defining the credentials and tool list needed by the plugin:

1. **Preserve Key Identifiers**:

   * **name**: Don't modify this field, keep it consistent with the name in manifest.yaml
   * Preserve existing i18n configurations and structures

2. **Complete Display Information**:

   * **label**: It's recommended to complete multilingual display names
   * **description**: It's recommended to complete multilingual descriptions

3. **Add New Tools**:
   * Add references to new tool YAML files in the `tools` list
   * Ensure the path is correct: `tools/feature_name.yaml`

```yaml
identity:
    author: your_name
    name: your_plugin_name # Don't modify this field
    label:
        en_US: Your Plugin Display Name
        zh_Hans: Your Plugin Display Name in Chinese
    description:
        en_US: Detailed description of your plugin functionality
        zh_Hans: Detailed description of your plugin functionality in Chinese
    icon: icon.svg
credentials_for_provider: # Only add when API keys or other credentials are needed
    api_key:
        type: secret-input
        required: true
        label:
            en_US: API Key
            zh_Hans: API Key in Chinese
        placeholder:
            en_US: Enter your API key
            zh_Hans: Enter your API key in Chinese
        help:
            en_US: How to get your API key
            zh_Hans: How to get your API key in Chinese
        url: https://example.com/get-api-key
tools: # Tool list, update here when adding new tools
    - tools/feature_one.yaml
    - tools/feature_two.yaml
extra:
    python:
        source: provider/your_plugin.py
```

### tools/feature.yaml

Tool configuration file, defining the tool's parameters and descriptions:

1. **Preserve Identifiers and Structure**:
   * **name**: The unique identifier of the tool, corresponding to the file name
   * Maintain consistency with existing file structures

2. **Complete Configuration Content**:

   * **label** and **description**: Provide clear multilingual display content
   * **parameters**: Define tool parameters and their properties in detail

3. **Parameter Definition Guidance**:
   * **type**: Choose appropriate parameter types (string/number/boolean/file)
   * **form**: Set to `llm` (extracted by AI) or `form` (UI configuration)
   * **required**: Specify whether the parameter is required

```yaml
identity:
    name: feature_name # Corresponds to file name
    author: your_name
    label:
        en_US: Feature Display Name
        zh_Hans: Feature Display Name in Chinese
description:
    human: # Description for human users
        en_US: Description for human users
        zh_Hans: Description for human users in Chinese
    llm: Description for AI models to understand when to use this tool. # Description for AI
parameters: # Parameter definitions
    - name: param_name
      type: string # string, number, boolean, file, etc.
      required: true
      label:
          en_US: Parameter Display Name
          zh_Hans: Parameter Display Name in Chinese
      human_description:
          en_US: Parameter description for users
          zh_Hans: Parameter description for users in Chinese
      llm_description: Detailed parameter description for AI models
      form: llm # llm indicates it can be extracted by AI from user input, form indicates it needs to be configured in UI
    # Other parameters...
extra:
    python:
        source: tools/feature.py # Corresponding Python implementation file
# Optional: Define JSON Schema for output
output_schema:
    type: object
    properties:
        result:
            type: string
            description: Description of the result
```

### tools/feature.py

Tool implementation class, containing core business logic:

1. **Class Name Corresponds to File Name**:

   * Class name follows the `FeatureTool` pattern, corresponding to the file name
   * Ensure there is **only one** Tool subclass in a file

2. **Parameter Processing Best Practices**:

   * For required parameters, use the `.get()` method and provide default values: `param = tool_parameters.get("param_name", "")`

   * For optional parameters, there are two handling approaches:

     ```python
     # Method 1: Use the .get() method (recommended for single parameters)
     optional_param = tool_parameters.get("optional_param")  # Returns None if not present

     # Method 2: Use try-except (handle multiple optional parameters)
     try:
         name = tool_parameters["name"]
         issuer_name = tool_parameters["issuer_name"]
     except KeyError:
         name = None
         issuer_name = None
     ```

   * This try-except approach is a temporary solution for handling multiple optional parameters

   * Always validate the existence and validity of parameters before using them

3. **Output Methods**:
   * Use `yield` to return various types of messages
   * Support text, JSON, links, and variable outputs

```python
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Import tool functions, ensure function names are spelled correctly
from utils.helpers import process_data

class FeatureTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            # 1. Get required parameters
            param = tool_parameters.get("param_name", "")

            # 2. Get optional parameters - using try-except approach
            try:
                optional_param1 = tool_parameters["optional_param1"]
                optional_param2 = tool_parameters["optional_param2"]
            except KeyError:
                optional_param1 = None
                optional_param2 = None

            # Another approach for optional parameters - using .get() method
            another_optional = tool_parameters.get("another_optional")  # Returns None if not present

            # 3. Validate required parameters
            if not param:
                yield self.create_text_message("Parameter is required.")
                return

            # 4. Implement business logic
            result = self._process_data(param, optional_param1, optional_param2)

            # 5. Return results
            # Text output
            yield self.create_text_message(f"Processed result: {result}")
            # JSON output
            yield self.create_json_message({"result": result})
            # Variable output (for workflows)
            yield self.create_variable_message("result_var", result)

        except Exception as e:
            # Error handling
            yield self.create_text_message(f"Error: {str(e)}")

    def _process_data(self, param: str, opt1=None, opt2=None) -> str:
        """
        Implement specific business logic

        Args:
            param: Required parameter
            opt1: Optional parameter 1
            opt2: Optional parameter 2

        Returns:
            Processing result
        """
        # Execute different logic based on whether parameters exist
        if opt1 and opt2:
            return f"Processed with all options: {param}, {opt1}, {opt2}"
        elif opt1:
            return f"Processed with option 1: {param}, {opt1}"
        elif opt2:
            return f"Processed with option 2: {param}, {opt2}"
        else:
            return f"Processed basic: {param}"
```

### utils/helper.py

Helper functions implementing reusable functionality logic:

1. **Function Separation**:

   * Extract common functionality into separate functions
   * Focus on single responsibility
   * Pay attention to function naming consistency (avoid import errors)

2. **Error Handling**:
   * Include appropriate exception handling
   * Use specific exception types
   * Provide meaningful error messages

```python
import requests
from typing import Dict, Any, Optional

def call_external_api(endpoint: str, params: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    """
    General function for calling external APIs

    Args:
        endpoint: API endpoint URL
        params: Request parameters
        api_key: API key

    Returns:
        JSON data from API response

    Raises:
        Exception: If API call fails
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Throw exception if status code is not 200
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"API call failed: {str(e)}")
```

### requirements.txt

Dependency list, specifying the Python libraries needed by the plugin:

1. **Version Specifications**:

   * Use `~=` to specify dependency version ranges
   * Avoid overly loose version requirements

2. **Necessary Dependencies**:
   * Must include `dify_plugin`
   * Add all third-party libraries needed for plugin functionality

```
dify_plugin~=0.0.1b76
requests~=2.31.0
# Other dependencies...
```

## Tool Development Best Practices

### 1. Parameter Handling Patterns

1. **Required Parameter Handling**:

   * Use the `.get()` method and provide default values: `param = tool_parameters.get("param_name", "")`
   * Validate parameter validity: `if not param: yield self.create_text_message("Error: Required parameter missing.")`

2. **Optional Parameter Handling**:

   * **Single Optional Parameter**: Use the `.get()` method, allowing it to return None: `optional = tool_parameters.get("optional_param")`
   * **Multiple Optional Parameters**: Use try-except pattern to handle KeyError:
     ```python
     try:
         param1 = tool_parameters["optional_param1"]
         param2 = tool_parameters["optional_param2"]
     except KeyError:
         param1 = None
         param2 = None
     ```
   * This try-except approach is a temporary solution for handling multiple optional parameters

3. **Parameter Validation**:
   * Validate required parameters: `if not required_param: return error_message`
   * Handle optional parameters conditionally: `if optional_param: do_something()`

### 2. Secure File Operation Methods

1. **Avoid Local File Reading/Writing**:

   * Dify plugins run in serverless environments (like AWS Lambda), where local file system operations may be unreliable
   * Don't use `open()`, `read()`, `write()`, or other direct file operations
   * Don't rely on local files for state storage

2. **Use Memory or APIs Instead**:
   * Store temporary data in memory variables
   * Use Dify's provided KV storage API for persistent data
   * For large amounts of data, consider using databases or cloud storage services

### 3. Copy Existing Files Rather Than Creating From Scratch

For cases where you're uncertain about the correct structure, strongly recommend using the following method:

```bash
# Copy tool YAML file as a template
cp tools/existing_tool.yaml tools/new_tool.yaml

# Copy tool Python implementation
cp tools/existing_tool.py tools/new_tool.py

# Similarly applies to provider files
cp provider/existing.yaml provider/new.yaml
```

This ensures that file structures and formats comply with the requirements of the Dify plugin framework, then make targeted modifications.

### 4. Split Tool Functionality

Split complex functionality into multiple simple tools, with each tool focusing on a single function:

```
tools/
├── search.py          # Search functionality
├── search.yaml
├── create.py          # Create functionality
├── create.yaml
├── update.py          # Update functionality
├── update.yaml
├── delete.py          # Delete functionality
└── delete.yaml
```

### 2. Parameter Design Principles

* **Necessity**: Only require necessary parameters, provide reasonable default values
* **Type Definition**: Choose appropriate parameter types (string/number/boolean/file)
* **Clear Description**: Provide clear parameter descriptions for humans and AI
* **Form Definition**: Correctly distinguish between llm (AI extraction) and form (UI configuration) parameters

### 3. Error Handling

```python
try:
    # Try to perform operation
    result = some_operation()
    yield self.create_text_message("Operation successful")
except ValueError as e:
    # Parameter error
    yield self.create_text_message(f"Parameter error: {str(e)}")
except requests.RequestException as e:
    # API call error
    yield self.create_text_message(f"API call failed: {str(e)}")
except Exception as e:
    # Other unexpected errors
    yield self.create_text_message(f"An error occurred: {str(e)}")
```

### 4. Code Organization and Reuse

Extract reusable logic to the utils directory:

```python
# In tool implementation
from utils.api_client import ApiClient

class SearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        client = ApiClient(self.runtime.credentials["api_key"])
        results = client.search(tool_parameters["query"])
        yield self.create_json_message(results)
```

### 5. Output Formats

Dify supports multiple output formats:

```python
# Text output
yield self.create_text_message("This is a text message")

# JSON output
yield self.create_json_message({"key": "value"})

# Link output
yield self.create_link_message("https://example.com")

# Variable output (for workflows)
yield self.create_variable_message("variable_name", "variable_value")
```

## Common Errors and Solutions

### Loading and Initialization Errors

1. **Multiple Tool Subclasses Error**

   ```
   Exception: Multiple subclasses of Tool in /path/to/file.py
   ```

   * **Cause**: Multiple classes inheriting from Tool defined in the same Python file
   * **Solution**:
     * Check file contents: `cat tools/problematic_file.py`
     * Keep one Tool subclass corresponding to the file name in each file
     * Move other Tool subclasses to separate files

2. **Import Error**

   ```
   ImportError: cannot import name 'x' from 'module'. Did you mean: 'y'?
   ```

   * **Cause**: Imported function name doesn't match actual definition
   * **Solution**:
     * Check function names in utils: `cat utils/the_module.py`
     * Fix spelling errors in import statements
     * Pay attention to underscores, case, etc. in function names

3. **Credential Validation Failure**
   ```
   ToolProviderCredentialValidationError: Invalid API key
   ```
   * **Cause**: Credential validation logic failed
   * **Solution**:
     * Check `_validate_credentials` method implementation
     * Ensure API key format is correct
     * Add detailed error prompt information

### Runtime Errors

1. **Parameter Retrieval Error**

   ```
   KeyError: 'parameter_name'
   ```

   * **Cause**: Attempting to access a non-existent parameter
   * **Solution**:
     * Use `get()` instead of direct indexing: `param = tool_parameters.get("param_name", "")`
     * Ensure parameter names match YAML definitions
     * Add parameter existence checks

2. **API Call Error**

   ```
   requests.exceptions.RequestException: Connection error
   ```

   * **Cause**: External API call failed
   * **Solution**:
     * Add timeout parameter: `timeout=10`
     * Use `try/except` to catch exceptions
     * Implement retry logic

3. **Execution Timeout**
   ```
   TimeoutError: Function execution timed out
   ```
   * **Cause**: Operation takes too long
   * **Solution**:
     * Optimize API calls
     * Break complex operations into multiple steps
     * Set reasonable timeout limits

### Configuration and Packaging Errors

1. **YAML Format Error**

   ```
   yaml.YAMLError: mapping values are not allowed in this context
   ```

   * **Cause**: Incorrect YAML format
   * **Solution**:
     * Check indentation (use spaces, not tabs)
     * Ensure colons are followed by spaces
     * Use a YAML validator to check

2. **Packaging Failure**
   ```
   Error: Failed to pack plugin
   ```
   * **Cause**: File structure or dependency issues
   * **Solution**:
     * Check manifest.yaml configuration
     * Ensure all referenced files exist
     * Review requirements.txt content

## Code Example: TOTP Tool

Here's a complete example of a TOTP (Time-based One-Time Password) plugin, demonstrating good code organization and best practices:

### utils/totp\_verify.py

```python
import pyotp
import time

def verify_totp(secret_key, totp_code, offset=5, strict=False):
    """
    Verify a Time-based One-Time Password (TOTP).

    Args:
        secret_key: The secret key or configuration URL used to generate the TOTP
        totp_code: The dynamic token submitted by the user
        offset: The number of seconds allowed for early or late verification
        strict: Whether to use strict verification (only return success on exact match)

    Returns:
        A dictionary containing:
        - 'status': 'success' or 'fail'
        - 'detail': Internal message (not for end users)
    """
    try:
        # Detect if it's a configuration URL
        if secret_key.startswith('otpauth://'):
            totp = pyotp.parse_uri(secret_key)
        else:
            totp = pyotp.TOTP(secret_key)

        current_time = time.time()

        # Exact time verification
        if totp.verify(totp_code):
            return {'status': 'success', 'detail': 'Token is valid'}

        # Offset verification
        early_valid = totp.verify(totp_code, for_time=current_time + offset)
        late_valid = totp.verify(totp_code, for_time=current_time - offset)
        off_time_valid = early_valid or late_valid

        detail_message = (
            f"Token is valid but not on time. "
            f"{'Early' if early_valid else 'Late'} within {offset} seconds"
            if off_time_valid else
            "Token is invalid"
        )

        if strict:
            return {'status': 'fail', 'detail': detail_message}
        else:
            return (
                {'status': 'success', 'detail': detail_message}
                if off_time_valid
                else {'status': 'fail', 'detail': detail_message}
            )
    except Exception as e:
        return {'status': 'fail', 'detail': f'Verification error: {str(e)}'}
```

### tools/totp.yaml

```yaml
identity:
    name: totp
    author: your-name
    label:
        en_US: TOTP Validator
        zh_Hans: TOTP Validator
description:
    human:
        en_US: Time-based one-time password (TOTP) validator
        zh_Hans: Time-based one-time password (TOTP) validator
    llm: Time-based one-time password (TOTP) validator, this tool is used to validate a 6 digit TOTP code with a secret key or provisioning URI.
parameters:
    - name: secret_key
      type: string
      required: true
      label:
          en_US: TOTP secret key or provisioning URI
          zh_Hans: TOTP secret key or provisioning URI
      human_description:
          en_US: The secret key or provisioning URI used to generate the TOTP
          zh_Hans: The secret key or provisioning URI used to generate the TOTP
      llm_description: The secret key or provisioning URI (starting with 'otpauth://') used to generate the TOTP, this is highly sensitive and should be kept secret.
      form: llm
    - name: user_code
      type: string
      required: true
      label:
          en_US: 6 digit TOTP code to validate
          zh_Hans: 6 digit TOTP code to validate
      human_description:
          en_US: 6 digit TOTP code to validate
          zh_Hans: 6 digit TOTP code to validate
      llm_description: 6 digit TOTP code to validate
      form: llm
extra:
    python:
        source: tools/totp.py
output_schema:
    type: object
    properties:
        True_or_False:
            type: string
            description: Whether the TOTP is valid or not, return in string format, "True" or "False".
```

### tools/totp.py

```python
from collections.abc import Generator
from typing import Any

# Correctly import tool functions
from utils.totp_verify import verify_totp

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# One file contains only one Tool subclass
class TotpTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Verify a Time-based One-Time Password (TOTP)"""
        # Get parameters, use get() to avoid KeyError
        secret_key = tool_parameters.get("secret_key")
        totp_code = tool_parameters.get("user_code")

        # Parameter validation
        if not secret_key:
            yield self.create_text_message("Error: Secret key is required.")
            return
        if not totp_code:
            yield self.create_text_message("Error: TOTP code is required.")
            return

        try:
            # Call tool function
            result = verify_totp(secret_key, totp_code)

            # Return results
            yield self.create_json_message(result)

            # Return different messages based on verification results
            if result["status"] == "success":
                yield self.create_text_message("Valid")
                yield self.create_variable_message("True_or_False", "True")
            else:
                yield self.create_text_message("Invalid")
                yield self.create_variable_message("True_or_False", "False")

        except Exception as e:
            # Error handling
            yield self.create_text_message(f"Verification error: {str(e)}")
```

### tools/secret\_generator.py

```python
from collections.abc import Generator
from typing import Any

import pyotp

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Note: One file contains only one Tool subclass
class SecretGenerator(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Generate TOTP secret key"""
        try:
            # Generate random secret key
            secret_key = pyotp.random_base32()
            yield self.create_text_message(secret_key)

            # Safely get optional parameters
            name = tool_parameters.get("name")
            issuer_name = tool_parameters.get("issuer_name")

            # Generate configuration URI if name or issuer is provided
            if name or issuer_name:
                provisioning_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
                    name=name,
                    issuer_name=issuer_name
                )
                yield self.create_variable_message("provisioning_uri", provisioning_uri)

        except Exception as e:
            yield self.create_text_message(f"Error generating secret: {str(e)}")
```

### requirements.txt

```
dify_plugin~=0.0.1b76
pyotp~=2.9.0
```

This example demonstrates:

* Clear functional separation (tool functions in utils, tool classes in tools)
* Good error handling and parameter validation
* One file containing only one Tool subclass
* Detailed comments and docstrings
* Well-designed YAML configuration

## Status Synchronization Mechanism

If the user's description differs from your recorded project status, or you need to confirm current progress, perform these operations:

1. Check the project file structure
2. Read key files
3. Clearly inform the user: "I notice that the project status may differ from my previous understanding. I have rechecked the project files and updated my understanding."
4. Describe the actual status you discovered
5. Update the progress record in the working directory

## First Launch Behavior

When a user first activates you via "@ai" or similar means, you should:

1. **Don't assume project goals**: Don't assume what type of plugin or functionality the user wants to develop
2. **Don't start writing code**: Don't generate or modify code without clear instructions
3. **Ask about user intent**: Politely ask what type of plugin the user hopes to develop and what problems they need help solving
4. **Provide capability overview**: Briefly explain what types of help you can provide (code implementation, debugging, design suggestions, etc.)
5. **Request project information**: Ask the user to share the current project status or file structure so you can provide more targeted help

Only start providing specific development suggestions or code implementation after receiving clear instructions.

Remember, your main goal is to assist users in efficiently completing Dify plugin development by continuously tracking status, providing professional advice, and solving technical challenges.

{/*
  Contributing Section
  DO NOT edit this section!
  It will be automatically generated by the script.
  */}

***

## Lybic API：

```python
from lybic import LybicClient

async def main():
    async with LybicClient(
        org_id="ORG-xxxx",
        api_key="lysk-xxxxxxxxxxx",
        endpoint="https://api.lybic.cn/",
    ) as client:
        pass
```

### LybicClient Manual lifecycle management

From v0.5.4, we've added a new feature that allows developers to manually manage the LybicClient lifecycle for increased 
flexibility.

However, please note that this introduces certain risks, and we still recommend using the `async with ... as ...` syntax.

```python
import asyncio 
from lybic import LybicClient

client = LybicClient(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx")

async def main():
    await client.request("GET", f"/api/orgs/{client.org_id}/stats")
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Class Stats

`Stats` is a class for describing the stats of the organization.

1. Get the stats of the organization

    such as number of members, computers, etc.

    method: `get()`
    - args: None
    - return: class dto.StatsResponseDto

    ```python
    from lybic import Stats
    # Inside your async main function, with the client initialized:
    stats = Stats(client)
    print(await stats.get())
    ```
    
    It will out put something like this:

    ```
    mcpServers=3 sandboxes=8 projects=4
    ```

### Class Project

`Project` is a class for describing the project and used to manage the sandbox of the project.

1. List all projects

   method: `list()`
   - args: None
   - return: class dto.ProjectListResponseDto

   ```python
   import asyncio
   from lybic import Project
   # Inside your async main function, with the client initialized:
   project = Project(client)
   list_result = await project.list()
   ```

   The returned is a traversable data model list[dto.ProjectResponseDto]

   ```python
   for project in list_result:
       print(project)
   ```
   
   It will out put something like this:(Sort by `createdAt`)
   
   ```
   id='PRJ-xxxx' name='test_project' createdAt='2025-07-10T08:03:36.375Z' defaultProject=False
   id='PRJ-xxxx' name='Default Project' createdAt='2025-07-08T16:42:30.226Z' defaultProject=True
   ```

2. Create a project
   
   method: `create(data: dto.CreateMcpServerDto)` or `create(**kwargs)`
   - args: class dto.CreateProjectDto
     - *name: str project name
   - return: class dto.SingleProjectResponseDto

   ```python
   import asyncio
   from lybic import dto
   from lybic import Project
   
   # Inside your async main function, with the client initialized:
   project = Project(client)
   # Using DTO
   print(await project.create(dto.CreateProjectDto(name="test_project")))
   # Using keyword arguments
   print(await project.create(name="test_project_2"))
   ```
   
   It will out put something like this:

   ```
   id='PRJ-xxxx' name='test_project' createdAt='2025-07-10T08:03:36.375Z' defaultProject=False
   ```

3. Delete a project

   method: `delete(project_id: str)`
   - args: 
     - *project_id: str ID of the project to delete
   - return: None(If No http error)

   ```python
   import asyncio
   from lybic import Project
   # Inside your async main function, with the client initialized:
   project = Project(client)
   await project.delete(project_id="PRJ-xxxx")
   ```

### Class MCP

`MCP` is a client for Lybic's Model Context Protocol (MCP) and its associated RESTful API.

1. List all MCP servers

   method: `list()`
   - args: None
   - return: class dto.ListMcpServerResponse

   ```python
   import asyncio
   from lybic import MCP

   mcp = MCP(client)
   mcp_servers = asyncio.run(mcp.list())
   for server in mcp_servers:
       print(server)
   ```

   It will out put something like this:

   ```
   id='MCP-xxxx' name='my-mcp-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=False projectId="PRJ-xxxx"
   id='MCP-xxxx' name='default-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=True projectId="PRJ-xxxx"
   ```

2. Create an MCP server

   method: `create(data: dto.CreateMcpServerDto)` or `create(**kwargs)`
   - args: class dto.CreateMcpServerDto
     - *name: str Name of the MCP server
     - projectId: str (optional) Project to which the server belongs
   - return: class dto.McpServerResponseDto

   ```python
   from lybic import dto, MCP

   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   # Using DTO
   new_server = await mcp.create(dto.CreateMcpServerDto(name="my-mcp-server"))
   print(new_server)
   # Using keyword arguments
   new_server_2 = await mcp.create(name="my-mcp-server-2")
   print(new_server_2)
   ```
   It will out put something like this:
   ```
   id='MCP-xxxx' name='my-mcp-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=False projectId="PRJ-xxxx"
   ```

3. Get the default MCP server

   method: `get_default()`
   - args: None
   - return: class dto.McpServerResponseDto

   ```python
   import asyncio
   from lybic import MCP
   
   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   default_server = await mcp.get_default()
   print(default_server)
   ```
   It will out put something like this:
   ```
   id='MCP-xxxx' name='default-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=True projectId="PRJ-xxxx"
   ```

4. Delete an MCP server

   method: `delete(mcp_server_id: str)`
   - args:
     - *mcp_server_id: str ID of the MCP server to delete
   - return: None(If No http error)

   ```python
   from lybic import MCP

   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   await mcp.delete(mcp_server_id="MCP-xxxx")
   ```

5. Set MCP server to a sandbox

   method: `set_sandbox(mcp_server_id: str, sandbox_id: str)`
   - args:
     - *mcp_server_id: str ID of the MCP server
     - *sandbox_id: str ID of the sandbox to connect the MCP server to
   - return: None(If No http error)

   ```python
   from lybic import MCP

   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   await mcp.set_sandbox(mcp_server_id="MCP-xxxx", sandbox_id="SBX-xxxx")
   ```

### Class ComputerUse

`ComputerUse` is a client for the Lybic ComputerUse API, used for parsing model outputs and executing actions.

1. Parse model output into computer action.(support `ui-tars` and `oai-compute-use`[openai])

   if you want to parse the model output, you can use this method.

   method: `parse_model_output(data: dto.ComputerUseParseRequestDto)` or `parse_model_output(**kwargs)`
   - args: class dto.ComputerUseParseRequestDto
     - *model: str The model to use (e.g., "ui-tars")
     - *textContent: str The text content to parse
   - return: class dto.ComputerUseActionResponseDto

   if the model you use is "ui-tars", and its prompts like this:

   ```markdown
   You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task.

   ## Output Format
    \```
    Thought: ...
    Action: ...
    \```
   
   ## Action Space
   click(point='<point>x1 y1</point>')
   left_double(point='<point>x1 y1</point>')
   right_single(point='<point>x1 y1</point>')
   drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')
   hotkey(key='ctrl c') # Split keys with a space and use lowercase. Also, do not use more than 3 keys in one hotkey action.
   type(content='xxx') # Use escape characters \', \", and \n in content part to ensure we can parse the content in normal python string format. If you want to submit your input, use \n at the end of content. 
   scroll(point='<point>x1 y1</point>', direction='down or up or right or left') # Show more information on the `direction` side.
   wait() #Sleep for 5s and take a screenshot to check for any changes.
   finished(content='xxx') # Use escape characters \', \", and \n in content part to ensure we can parse the content in normal python string format.
   
   ## Note
   - Use {language} in `Thought` part.
   - Write a small plan and finally summarize your next action (with its target element) in one sentence in `Thought` part.
   
   ## User Instruction
   {instruction}
   ```

   The model output like this:

   ```
   Thought: The task requires double-left-clicking the "images" folder. In the File Explorer window, the "images" folder is visible under the Desktop directory. The target element is the folder named "images" with a yellow folder icon. Double-left-clicking this folder will open it.

   Next action: Left - double - click on the "images" folder icon located in the File Explorer window, under the Desktop directory, with the name "images" and yellow folder icon.
   Action: left_double(point='<point>213 257</point>')
   ```

   This api will parse this model output format and return a list of computer use actions.

   ```python
   import asyncio
   from lybic import LybicClient, dto, ComputerUse

   async def main():
       async with LybicClient(
           org_id="ORG-xxxx",
           api_key="lysk-xxxxxxxxxxx",
           endpoint="https://api.lybic.cn/",
       ) as client:
           computer_use = ComputerUse(client)
           text_content = """Thought: The task requires double-left-clicking the "images" folder. In the File Explorer window, the "images" folder is visible under the Desktop directory. The target element is the folder named "images" with a yellow folder icon. Double-left-clicking this folder will open it.
        
           Next action: Left - double - click on the "images" folder icon located in the File Explorer window, under the Desktop directory, with the name "images" and yellow folder icon.
           Action: left_double(point='<point>213 257</point>')"""
           # Using DTO
           actions = await computer_use.parse_model_output(
               dto.ComputerUseParseRequestDto(
                   model="ui-tars",
                   textContent=text_content
               )
           )
           print(actions)
           # Using keyword arguments
           actions_2 = await computer_use.parse_model_output(model="ui-tars", textContent=text_content)
           print(actions_2)
   if __name__ == "__main__":
       asyncio.run(main())
   ```
   It will out put something like this:(an action list object,and length is 1)

   ```
   actions=[MouseDoubleClickAction(type='mouse:doubleClick', x=FractionalLength(type='/', numerator=213, denominator=1000), y=FractionalLength(type='/', numerator=257, denominator=1000), button=1)]
   ```

2. Execute a computer use action

This interface enables `Planner` to perform actions on the sandbox through Restful calls

   method: `execute_computer_use_action(sandbox_id: str, data: dto.ComputerUseActionDto)` or `execute_computer_use_action(sandbox_id: str, **kwargs)`
   - args:
     - *sandbox_id: str ID of the sandbox
     - *data: class dto.ComputerUseActionDto The action to execute
   - return: class dto.SandboxActionResponseDto

      ```python
      import asyncio
      from lybic import dto, ComputerUse
      async def main():
          async with LybicClient(
               org_id="ORG-xxxx",
               api_key="lysk-xxxxxxxxxxx",
               endpoint="https://api.lybic.cn/",
          ) as client:
              computer_use = ComputerUse(client)
              actions = await computer_use.parse_model_output(
                  model="ui-tars",
                  textContent="""Thought: The task requires double-left-clicking the "images" folder. In the File Explorer window, the "images" folder is visible under the Desktop directory. The target element is the folder named "images" with a yellow folder icon. Double-left-clicking this folder will open it.
        
              Next action: Left - double - click on the "images" folder icon located in the File Explorer window, under the Desktop directory, with the name "images" and yellow folder icon.
              Action: left_double(point='<point>213 257</point>')"""
              )
              # Using DTO
              response = await computer_use.execute_computer_use_action(
                  sandbox_id="SBX-xxxx",
                  data=dto.ComputerUseActionDto(action=actions[0])
              )
              print(response)
              # Using keyword arguments
              response_2 = await computer_use.execute_computer_use_action(
                  sandbox_id="SBX-xxxx",
                  action=actions[0]
              )
              print(response_2)
      if __name__ == "__main__":
          asyncio.run(main())
      ```

### Class Sandbox

`Sandbox` provides methods to manage and interact with sandboxes.

1. List all sandboxes

   method: `list()`
   - args: None
   - return: class dto.SandboxListResponseDto

   ```python
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   sandboxes = await sandbox.list()
   for s in sandboxes:
       print(s)
   ```
   It will out put something like this:
   ```
   id='SBX-xxxxx' name='xxxx' expiredAt='2025-07-25T07:21:31.026Z' createdAt='2025-07-25T06:21:31.027Z' projectId='PRJ-xxxxxxx'
   id='SBX-xxxxx' name='xxxx' expiredAt='2025-07-26T08:24:11.198Z' createdAt='2025-07-26T07:24:11.199Z' projectId='PRJ-xxxxxxx'
   ```

2. Create a new sandbox

   method: `create(data: dto.CreateSandboxDto)` or `create(**kwargs)`
   - args: class dto.CreateSandboxDto
     - name: str (optional) Name for the sandbox, if not provided, it will use a default name(sandbox).
     - maxLifeSeconds: int (optional) Lifetime in seconds, if not provided, it will use the default value of 3600 seconds (1 hour).
     - projectId: str (optional) Project ID to associate with the sandbox,if not provided, it will use the default project.
     - specId: str (optional) ID of the sandbox spec to use, if not provided, it will use the default spec.
     - datacenterId: str (optional) ID of the datacenter to use, if not provided, it will use the default datacenter.
   - return: class dto.GetSandboxResponseDto

   ```python
   from lybic import dto, Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   # Using DTO
   new_sandbox = await sandbox.create(dto.CreateSandboxDto(name="my-sandbox"))
   print(new_sandbox)
   # Using keyword arguments
   new_sandbox_2 = await sandbox.create(name="my-sandbox-2")
   print(new_sandbox_2)
   ```

3. Get a specific sandbox

   method: `get(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: class dto.GetSandboxResponseDto

   ```python
   import asyncio
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   details = await sandbox.get(sandbox_id="SBX-xxxx")
   print(details)
   ```

   It will out put something like this:

   ```
   sandbox=Sandbox(id='SBX-xxxx', name='xxxx', expiredAt='2025-07-26T08:24:11.198Z', createdAt='2025-07-26T07:24:11.199Z', projectId='PRJ-xxxx'), connectDetails=ConnectDetails(gatewayAddresses=[GatewayAddress(address='1.2.3.4', port=12345, name='0197e397-5394-7880-a314-d8a7e981f9e4', preferredProviders=[1], gatewayType=4)], certificateHashBase64='baes64str==', endUserToken='jwttokenbase64str')
   ```

4. Delete a sandbox

   method: `delete(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox to delete
   - return: None

   ```python
   import asyncio
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   await sandbox.delete(sandbox_id="SBX-xxxx")
   ```

5. Get a sandbox screenshot

   method: `get_screenshot(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: tuple (screenshot_url, PIL.Image.Image, webp_image_base64_string)

   ```python
   import asyncio
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   url, image, b64_str = await sandbox.get_screenshot(sandbox_id="SBX-xxxx")
   print(f"Screenshot URL: {url}")
   image.show()
   ```

6. Extend a sandbox's lifetime

    method: `extend_life(sandbox_id: str, seconds: int)`
    - args:
      - *sandbox_id: str ID of the sandbox
      - *seconds: int Lifetime in seconds to extend the sandbox's lifetime (default: 3600 s, 1 hour, max: 86400 s, 1 day)
    - return: None(if successful)

    ```python
    import asyncio
    from lybic import Sandbox
   
    # Inside your async main function, with the client initialized:
    sandbox = Sandbox(client)
    await sandbox.extend_life(sandbox_id="SBX-xxxx", seconds=3600)
    ```
