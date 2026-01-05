---
description: "This prompt is used to create a .gitignore file for a new project based on the project's programming language and framework."
agent: "agent"
tools: ['read/readFile', 'edit/createFile', 'edit/editFiles', 'search', 'web']
---
You're an expert in full-stack web development and version control using Git. Your task is to help create a comprehensive `.gitignore` file for a new project.

Please follow the steps below, step by step, and do not skip any of them. No more, no less.

1. **Identify the Project Type**: Read the [`README.md`](../../README.md) file in the project root to determine the primary programming language(s) and framework(s) used in the project.

2. **Identify the Project Technologies**: Read the [`copilot-instructions.md`](../copilot-instructions.md) file in the project root to gather additional context about the technologies, tools, and dependencies used in the project.

3. **Research Standard .gitignore Templates**: Search for standard `.gitignore` templates for the identified programming language(s) and framework(s). Use resources from [GitHub gitignore repository](https://github.com/github/gitignore) and [gitignore.io](https://www.toptal.com/developers/gitignore) to find relevant templates.

4. **Confirm existing .gitignore**: Check if a `.gitignore` file already exists in the project root. If it does, review its contents to see if it meets the project's needs. If it is sufficient, you can stop here. If it is insufficient, proceed to the next steps to enhance it.

5. **Create or Update .gitignore**: Based on the project's specific requirements, your research and your expertise, create a new `.gitignore` file or update the existing one. Ensure that it includes all necessary rules to ignore files and directories that should not be tracked by Git, such as build artifacts, dependency directories, environment files and OS-specific files.

6. Make sure to keep all of the following files are tracked by Git and not included in the `.gitignore`:
  - `.vscode/*`
  - `.devcontainer/*`
  - `.github/*`
  - `uv.lock`

7. **Validate the .gitignore**: Review the `.gitignore` file to ensure it is comprehensive and correctly formatted without duplicates. It must follow best practices for `.gitignore` files.