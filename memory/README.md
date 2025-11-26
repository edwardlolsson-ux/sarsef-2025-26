# Codex Memory

This folder is a placeholder for any persistent memory snippets you want Codex to reuse between chats.

## Starting fresh for a new chat

1. Close the current Codex CLI session.
2. Delete or move the contents of this `memory/` folder (for example `rm -rf memory/*` or rename the folder).
3. Start a new Codex chat; it will recreate `memory/` and repopulate it as needed.

Keeping this folder empty before opening a new chat guarantees Codex starts without any previous context.
