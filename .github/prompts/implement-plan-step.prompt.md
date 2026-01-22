---
description: "This prompt is used to implement a step of a detailed plan for making changes to a codebase or project"
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'todo']
---
Your task is to help implement a specific step from a detailed plan for making changes to a codebase or project.

This prompt is being iterated to improve its effectiveness. Please start from the beginning and reset any variable every time you run it.

Please follow the steps below, step by step, and do not skip any of them. No more, no less.

1. **Identify the Project Requirement**: Read the [`README.md`](../../README.md) file to understand the product requirements and determine the primary programming language(s) and framework(s) used in the project.

2. **Identify the Project Guielines and Technologies**: Read the [`copilot-instructions.md`](../copilot-instructions.md) file to understand the guidelines for contributing to the project and gather additional context about the technologies, tools, and dependencies used in the project.

3. **Obtain the Detailed Plan**: Ask user to provide the plan file that contains the detailed steps for making changes to the codebase or project: ${input.planFilePath}.

4. **Obtain the Specific Step to Implement**: Ask user to provide the specific step number from the detailed plan that you need to implement: ${input.stepNumber}.

5. **Understand the Detailed Plan**: Read the detailed plan provided, ${input.planFilePath}, understand what each step entails, and identify the specific step you need to implement based on the step number provided, ${input.stepNumber}.

6. **Implement the Specific Step**: Based on your understanding of the project requirements, guidelines, technologies, and the detailed plan, implement **ONLY** the specific step, ${input.stepNumber}, in the codebase or project. Ensure that your implementation adheres to best practices and the project's coding standards.

7. **Lint and Format the Code**: If there are no existing linters or formatters in the codebase, skip. Otherwise, run the appropriate linters and formatters as specified in the [`copilot-instructions.md`](../copilot-instructions.md) file to ensure that the code adheres to the project's coding standards.

8. **Test the Implementation**: If there's no existing tests in the codebase, skip. Otherwise, develop and run tests to verify that the specific step, ${input.stepNumber}, has been implemented correctly and follow the testing guidelines outlined in the [`copilot-instructions.md`](../copilot-instructions.md) file. Make sure that all tests pass successfully.

9. **Validate the Implementation**: Review and finish the checklist for the specific step you implemented to ensure that it meets the requirements outlined in the detailed plan.

10. **Document the Changes**: If applicable, update any relevant documentation based on the guidelines provided in the [`copilot-instructions.md`](../copilot-instructions.md) file to reflect the changes made during the implementation of the specific step.

11. **Communicate Completion**: Notify the user that you have completed the implementation of the specific step and provide a summary of the changes made.