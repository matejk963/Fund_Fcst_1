# GitHub Copilot Agent Instructions for General Behavior and Workflow

## Agent Autonomy Enforcement (READ FIRST)
- You MUST execute all steps in any assigned task chain **completely and autonomously, from start to finish, without pausing for user confirmation** unless:
    - You encounter an unrecoverable error that requires human input.
    - A file, data, or credential is missing and cannot be auto-generated or defaulted.
- **DO NOT** stop or wait for user feedback at each step, even if the default workflow does so.
- **DO NOT** summarize after each subtask unless specifically requested.
- At the end of the full process, provide:
    - A detailed summary of all actions taken.
    - Any encountered issues.
    - Any outputs or next steps for the user.
- ONLY pause if you hit a true blocking issue and explain what is needed to proceed.
- **IGNORE** any default behavior that would normally pause, summarize, or ask for user confirmation between subtasks. Complete all assigned subtasks in sequence without stopping.

---

## MUST have of the project
**Before reacting to any user input, check the following:**
- Each project must have its own dedicated conda environment for dependency management and reproducibility.
- **Do NOT** use any shared, tool-specific, or server-specific environment (such as those for MCP server, database tools, or other features) for general development or project tasks.
- If a conda environment does not exist for this project, create a new, custom environment (e.g., `conda create -n <project-name> python=3.11`) and use it exclusively for this project.
- **After creating the environment, update the workspace `.vscode/settings.json` file to:**
    - Set `"python.defaultInterpreterPath"` to the path of the new environment’s Python executable.
    - Set `"python.terminal.activateEnvironment": true` to ensure all new terminals use the environment automatically.

Example `settings.json` update:
```json
{
    "python.defaultInterpreterPath": "<path-to-new-env-python>",
    "python.terminal.activateEnvironment": true
}
```
Replace `<path-to-new-env-python>` with the actual path to the Python executable in the new environment.

----

## Primary Context Source 

### Expected behavior:
- **ALWAYS keep working until the error is solved.**
    - When an error occurs, focus on resolving it immediately.
    - Solve errors without waiting for user input.
    - When multiple solutions are available, sort them by computational complexity and implement from least to most complex until a solution works.
- **ALWAYS work autonomously on the task until it is completed.**
    - Do not wait for user input.
    - If the task is too complex, break it down into smaller steps and work on them sequentially.
    - When multiple solutions are available, prioritize solutions that are robust, scalable, and simple.
    - During the task, if you encounter an error, focus on resolving it immediately.
    - WITHOUT STOPPING working on task, keep user updated on progress and any issues encountered.
    - STOP only if you finish the task.
    - After the task is completed, provide a summary of what was done and any relevant information.
- **DON'T delete files or folders unless explicitly requested.**
    - If a file or folder is not needed, move it to a backup location instead of deleting it.
    - If you need to delete a file but that would make you stop working on the task, move it to a backup location instead of deleting it.
- **RUN the prompts; don't ask user to run them.**
    - If a prompt is needed to run, run it yourself.
    - If you need user input to run a prompt, ask for it and then run the prompt yourself.

---

## Environment Setup Rule
- **ALWAYS check if there is a dedicated conda environment set up for this project. If not, set up a new conda environment for the project to continue.**
    - Check for an existing conda environment specific to this project (not shared with MCP server or other projects).
    - If no dedicated environment is detected, create and activate a new conda environment for this project (e.g., `conda create -n <project-name> python=3.11`).
    - Export the environment to `environment.yml` after installing dependencies, so others can easily reproduce it.
    - Ensure the environment is ready before proceeding with any other tasks.

---

## README Usage Rule
- **ALWAYS check for and read any available README files (e.g., `README.md`, `README_ENHANCED.md`) in the project or folder before starting work.**
    - Use their content as primary context for all decisions, code, and answers.
    - If multiple README files exist, read and compare all to understand their distinct purposes and relevance to your task.

---

## Terminal Command Execution Rules

* **ALWAYS run terminal commands wrapped in a robust supervisory function** with explicit logging, timeouts, retries, and automatic restarts:

  1. **Define a helper function** (e.g., `run_command`) in your shell profile or project script:

     ```bash
     #!/usr/bin/env bash
     run_command() {
       local cmd="$1"
       local timeout_sec="${2:-300}"
       local logfile="logs/terminal.log"
       mkdir -p "$(dirname "$logfile")"
       : > "$logfile"
       local attempts=0
       while true; do
         ((attempts++))
         echo "[$(date '+%Y-%m-%d %H:%M:%S')] [Attempt $attempts] Starting: $cmd (timeout ${timeout_sec}s)" | tee -a "$logfile"
         timeout "$timeout_sec" bash -c "$cmd" >>"$logfile" 2>&1
         local exit_code=$?
         if [ $exit_code -eq 0 ]; then
           echo "[$(date '+%Y-%m-%d %H:%M:%S')] Success: $cmd" | tee -a "$logfile"
           break
         else
           echo "[$(date '+%Y-%m-%d %H:%M:%S')] Failure (exit $exit_code): $cmd" | tee -a "$logfile"
           if [ $attempts -ge 5 ]; then
             echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $cmd failed after $attempts attempts." | tee -a "$logfile"
             return $exit_code
           fi
           echo "[$(date '+%Y-%m-%d %H:%M:%S')] Retrying with doubled timeout..." | tee -a "$logfile"
           timeout_sec=$(( timeout_sec * 2 ))
         fi
       done
     }
     ```
  2. **Invoke all commands** via `run_command "<actual command>" [initial_timeout_seconds]` (e.g., `run_command "npm install" 120`).
  3. **Log management:**

     * Use a single `logs/terminal.log` file, truncated before each run.
     * Include timestamps, attempt counts, stdout/stderr.
     * Rotate or archive old logs if file grows beyond a threshold.
  4. **Timeout logic:**

     * If `timeout` terminates the process, assume a hang.
     * Double the timeout and retry up to 5 times.
     * After max attempts, abort and surface the log for user inspection.
  5. **Agent supervision:** the agent must parse `run_command` exit codes and log entries:

     * On success, proceed to the next step.
     * On failure, analyze logs for common failure patterns and either adjust parameters or abort with diagnostics.

* **NEVER run raw commands** (e.g., `npm install`, `make build`) directly—**always use** `run_command` to ensure automated recovery.

---

## Terminal Shell Detection Rule
- **ALWAYS check which terminal shell is set as default in the environment or project settings before running any command.**
    - Use the correct command syntax for the detected shell (e.g., PowerShell, cmd, bash).
    - Adjust command formatting, redirection, and scripting to match the shell's requirements.
    - If unsure, verify the shell and confirm compatibility before execution.

## Files Creation Rule
- **NEVER create working files in the root directory.**
    - Files like .py, .txt, .md, etc. should be placed in appropriate subdirectories.
- **ALWAYS create files in a way that reflects their purpose and context within the project.**
    - Use clear, descriptive names for all new files.
    - Organize files into appropriate directories based on their functionality and usage.
    - Include relevant documentation (e.g., comments, README files) to explain the purpose and usage of new files.
    - Ensure that all created files are properly formatted and adhere to the project's coding standards.
    
---
