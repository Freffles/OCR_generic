#WS Glocal Rules.md
<IDE_Rules>
    <General_Concepts>
        <rule>Follow the DRY (Don't Repeat Yourself) principle.</rule>
        <rule>Use the single responsibility principle to divide code into modules.</rule>
        <rule>Always ensure dependencies exist before attempting to use them. When setting up event listeners or interactions, place the setup code immediately after creating the elements they depend on, not before.</rule>
        <rule>Images provided as part of a prompt are typically used to describe a problem. The image and user provided text will describe the problem and request an action. If the user provides an image but no text, ask for more information.</rule>
        <rule>Make small, step-by-step changes; avoid large refactors.</rule>
        <rule>If the user provides a prompt that does not ask for specific actions, ask for more direction. If unsure, always seek clarification before proceeding.</rule>
        <rule>Follow user instructions above all else. Ask permission to change code outside your task.</rule>
        <rule>Do not overwrite manual changes unless explicitly requested.</rule>
        <rule>Reference project documentation when applicable.</rule>
        <rule>Approach problem-solving step-by-step.</rule>
        <rule>Minimize AI requests; batch changes when possible.</rule>
        <rule>Address bugs incrementally, using terminal output for insight.</rule>
    </General_Concepts>
    <Core_Programming_Principles>
        <rule>Separation of concerns to be applied wherever possible.</rule>
        <rule>Prioritize clean, readable, maintainable code.</rule>
        <rule>Use efficient algorithms and data structures.</rule>
        <rule>Break complex logic into smaller functions.</rule>
        <rule>Reuse existing, validated code when appropriate.</rule>
        <rule>Follow secure coding practices.</rule>
        <rule>Avoid over-engineering; prioritize simple solutions.</rule>
        <rule>Ensure all public-facing code, APIs, and key functionalities are thoroughly documented. Use docstrings for functions, methods, and classes.</rule>
        <rule>Document all dependencies; adapt interconnected components as needed.</rule>
        <rule>Avoid unnecessary changes to working components.</rule>
    </Core_Programming_Principles>
    <Error_Handling>
        <rule>During initial development, use broad exception handling (try/except Exception) with detailed logging to identify all possible failure modes</rule>
        <rule>Replace broad exception handlers with specific exceptions (e.g., OSError, ValueError, IOError)</rule>
        <rule>Group related exceptions when their handling is identical (e.g., except (OSError, IOError) as e:)</rule>
        <rule>Always include error details in the response message to aid debugging</rule>
    </Error_Handling>
    <Code_Style_and_Formatting>
        <rule>Use tabs for indentation.</rule>
        <rule>Use snake_case for variables, PascalCase for classes, and camelCase for functions.</rule>
        <rule>Add concise comments to explain logic; avoid redundancy.</rule>
        <rule>Always format code for readability.</rule>
        <rule>Keep lines under 100 characters.</rule>
        <rule>Format long lists and dictionaries for readability.</rule>
    </Code_Style_and_Formatting>
    <Language_Specific_Instructions>
        <Python>
            <rule>always use the virtual environment at ./.venv</rule>
            <rule>Use type hints for all parameters and return values.</rule>
            <rule>Group imports as: standard, external, and local.</rule>
            <rule>black/pylint/radon</rule>
            <rule>Test using .venv/bin/pytest</rule>
        </Python>
        <JavaScript>
            <rule>Use modern ECMAScript conventions.</rule>
            <rule>Avoid var; prefer const and let.</rule>
            <rule>eslint for consistent style.</rule>
            <rule>JSDoc for documenting functions.</rule>
            <rule>jest for unit testing.</rule>
        </JavaScript>
    </Language_Specific_Instructions>
    <File_Handling>
        <rule>Break large files into smaller, manageable modules.</rule>
        <rule>Prefer importing functions from other files instead of direct modification.</rule>
        <rule>Organize files into logical directories.</rule>
    </File_Handling>
</IDE_Rules>
