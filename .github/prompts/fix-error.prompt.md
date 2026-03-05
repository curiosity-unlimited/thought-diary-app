---
description: This prompt is used to fix an error in the codebase or project.
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent', 'todo']
---
Your task is to help fix a specific error in the codebase or project with a workflow that ensures best practices are followed.

This prompt is being iterated to improve its effectiveness. Please start from the beginning and reset any variable every time you run it.

Please follow the steps below, step by step, and do not skip any of them. No more, no less.

1. **Identify the Project Requirement**: Read the [`README.md`](../../README.md) file to understand the product requirements and determine the primary programming language(s) and framework(s) used in the project.

2. **Identify the Project Guielines and Technologies**: Read the [`copilot-instructions.md`](../copilot-instructions.md) file to understand the guidelines for contributing to the project and gather additional context about the technologies, tools, and dependencies used in the project.

3. **Identify the Commands to Use**: Read the development documentation under [`docs/`](../../docs/) to identify any specific commands, scripts, or tools that are commonly used in the project for development, debugging, linting, formatting, and testing.

4. **Identify the Error to Fix**: Read the error message or description and any relevant context of the issue provided by the user to understand what needs to be fixed.

5. **Locate the Source of the Error**: Analyze the codebase to locate the source of the error based on the information provided. This may involve searching through files, examining logs, or reproducing the error.

6. **Confirm Environment Setup**: Ensure that your development environment is properly set up with all necessary dependencies, tools, and configurations as specified in the development documentation under [`docs/`](../../docs/), for example:
  - Ensure that backend servers or services are running if the error is related to backend functionality.
  - Ensure that frontend development servers are running if the error is related to frontend functionality.
  - If the error is related both frontend and backend, ensure both servers or services are running in different terminal sessions.

7. **Fix the Error**: Based on your understanding of the project requirements, guidelines, technologies, and the source of the error, implement a fix in the codebase or project. Ensure that your fix adheres to best practices and the project's coding standards. Start a new terminal session if needed to run commands without stopping any running servers or services from step 6.

8. **Confirm the Fix**: Ask the user if the error has been resolved after your fix. If the user indicates that the error persists, revisit step 5 to further investigate and address the issue.

9. **Create a Test for the Error**: If there's no existing tests in the codebase, skip. Otherwise, 
add new tests to specifically cover the fixes made for the error. Follow the testing guidelines outlined in the [`copilot-instructions.md`](../copilot-instructions.md) file. Run those tests to ensure they pass successfully.

10. **Clean Up the Code**: Review the code changes made during the error fix to ensure that they are clean, well-organized, and free of any unnecessary code, temporary debugging scripts,
or comments.

11. **Lint and Format the Code**: If there are no existing linters or formatters in the codebase, skip. Otherwise, run the appropriate linters and formatters as specified in the [`copilot-instructions.md`](../copilot-instructions.md) file to ensure that the code adheres to the project's coding standards.

12. **Run Final Tests**: If there are no existing tests in the codebase, skip. Otherwise, run all tests in the codebase to ensure all tests pass successfully and meet code coverage requirements as specified in the [`copilot-instructions.md`](../copilot-instructions.md) file.

13. **Document the Changes**: Follow the testing guidelines outlined in the [`copilot-instructions.md`](../copilot-instructions.md) file and update all relevant documentation to reflect the changes made during the error fix. Follow these substeps:

  a. **Update Code Comments**: Review and update TSDoc/docstring comments in the modified code files to ensure they accurately reflect the new behavior.
  
  b. **Update README.md**: Check if [`README.md`](../../README.md) mentions the affected features or functionality. Update it if the changes affect its content.
    
  c. **Search for Related Documentation**: Use grep or semantic search to find documentation files under [`docs/`](../../docs/) that reference the code, APIs, functions, or components you modified. Look for:
     - File names, function names, or class names you changed
     - API endpoints or response structures you modified
     - Configuration or setup instructions affected by your changes
  
  d. **Update Technical Documentation**: Review and update all relevant files under [`docs/`](../../docs/) that reference the modified code.
  
  e. **Update CHANGELOG.md**: Document the changes in [`CHANGELOG.md`](../../CHANGELOG.md).

14. **Communicate Completion**: Notify the user that you have completed the error fix and provide a summary of all changes made.