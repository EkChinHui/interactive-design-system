# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered design system showcase built with React + TypeScript + Vite (frontend) and FastAPI + LiteLLM (backend). Users can browse, generate, and edit complete HTML design systems using natural language prompts.

## Development Commands

### Running the Application
```bash
# Terminal 1: Start frontend (runs on http://localhost:5173)
npm run dev

# Terminal 2: Start backend API (runs on http://localhost:3001)
npm run server
```

Both servers must run simultaneously for full functionality.

### Building and Testing
```bash
# Type check and build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Python Dependencies
Python dependencies are managed by `uv`. The `npm run server` command automatically handles installation via `uv run server.py`.

## Architecture

### Frontend (React + TypeScript)
- **Entry Point**: `src/main.tsx` → `src/App.tsx`
- **State Management**: React useState hooks in App.tsx for:
  - Design system list (`allSystems`)
  - Currently selected system (`selectedSystem`)
  - UI state (sidebar open/closed, modals)
  - Iframe reload trigger (`iframeKey`)

- **Component Structure**:
  - `App.tsx`: Main container with sidebar navigation and iframe preview
  - `CreateSystemModal.tsx`: Modal for generating new design systems via AI
  - `EditSystemModal.tsx`: Modal for editing existing systems via AI

- **Design System Data Flow**:
  1. On mount, fetches all systems from backend via `GET /api/design-systems` (App.tsx:67)
  2. Hardcoded `designSystems` array provides fallback descriptions for known systems (App.tsx:14)
  3. User creates/edits/deletes systems via UI → API calls to backend
  4. New systems added to `allSystems` state dynamically
  5. Deleted systems removed from state with auto-selection of next system
  6. Iframe reloads via `iframeKey` increment on creates and edits (App.tsx:118, 122)

### Backend (FastAPI + Python)
- **Entry Point**: `server.py` (runs on port 3001)
- **LLM Integration**: Uses LiteLLM with Claude Sonnet 4.5 (server.py:68)
- **File Storage**: Generated HTML files saved to `public/systems/`

### API Endpoints

**POST /api/generate-design-system**
- Accepts: `{ name: string, prompt: string }`
- Generates complete self-contained HTML design system
- Saves to `public/systems/{name}.html`
- Returns: `{ success, fileName, path, content }`

**POST /api/edit-design-system**
- Accepts: `{ fileName: string, comment: string }`
- Reads existing HTML, sends to LLM with edit instructions
- Overwrites original file with modified version
- Returns: `{ success, fileName, content }`

**DELETE /api/design-system/{file_name}**
- Deletes a design system file from `public/systems/`
- Includes path traversal validation for security
- Returns: `{ success, fileName }`

**GET /api/design-systems**
- Lists all HTML files in `public/systems/`
- Returns: `{ systems: [{ fileName, path, name }] }`

### Key Implementation Details

**LLM Prompt Architecture** (server.py):
- System prompts emphasize single-file HTML with embedded CSS/JS
- Stresses accessibility (WCAG 2.2 AA), design tokens, theme support
- `clean_html()` function strips markdown code blocks from LLM responses
- Edit prompts include full existing HTML for context
- `max_tokens` configurable in `call_llm()` function (server.py:79)
- **Automatic Continuation**: If HTML is incomplete (missing `</html>` or `</body>`), automatically continues generation up to 5 times (server.py:59-76, 130-163, 220-253)

**Frontend-Backend Communication**:
- Hardcoded API URL: `http://localhost:3001`
- Modal components handle fetch calls directly
- Success callbacks update App.tsx state and trigger iframe reload

**Design System Files**:
- Complete standalone HTML documents in `public/systems/`
- Include full component libraries, design tokens, examples
- Served directly by Vite dev server (frontend) or preview server

## Environment Requirements

- **Node.js**: 20.19+ or 22.12+
- **Python**: 3.12+
- **uv**: Modern Python package manager
- **LLM API Key**: Set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or other LiteLLM-supported provider

## Important Patterns

1. **Dual Server Architecture**: Frontend and backend run separately. Always start both.

2. **System Loading on Mount**: App fetches all design systems from backend on mount (App.tsx:67). This ensures any systems created outside the UI or on page refresh appear in the sidebar.

3. **Iframe Reload Pattern**: Both create and edit operations increment `iframeKey` to force iframe remount and ensure fresh content loads (App.tsx:118, 122).

4. **Delete with Confirmation**: Delete operations use native `window.confirm()` for user confirmation before API call (App.tsx:89).

5. **Auto-Selection on Delete**: When deleting the currently selected system, the app automatically selects the first remaining system (App.tsx:113).

6. **File Path Assumptions**: Backend expects `public/systems/` directory exists relative to `server.py`.

7. **LLM Model Configuration**: Model is hardcoded in `server.py:68`. Change requires editing source, not config file.

8. **CORS Configuration**: Backend only allows `http://localhost:5173` (server.py:14). Must update if frontend port changes.

9. **HTML Cleaning**: LLM responses may include markdown code blocks—always use `clean_html()` utility (server.py:49).

10. **Path Traversal Protection**: DELETE endpoint validates file names to prevent directory traversal attacks (server.py:208).

11. **Automatic Generation Continuation**: If LLM output is truncated (missing closing tags), the system automatically detects incomplete HTML using `is_html_complete()` and prompts the LLM to continue from where it left off, up to 5 continuation attempts. This ensures complete design systems even when they exceed single-response token limits (server.py:130-163).

## Common Modifications

**Change LLM Model**: Edit `server.py:86` model parameter in `litellm.completion()` call.

**Adjust Token Limit**: Modify `max_tokens` parameter in `call_llm()` function (server.py:79). Set to `None` for unlimited (respects model's max). The automatic continuation feature will handle incomplete responses.

**Adjust Continuation Behavior**: Modify `max_continuations` variable in generation endpoints (server.py:132, 222). Default is 5 attempts. Increase for very large design systems; decrease to fail faster.

**Add New Design System Manually**:
1. Place HTML file in `public/systems/`
2. Refresh the frontend - it will automatically appear in the sidebar

**Modify System Prompt**: Edit system_prompt strings in `generate_design_system()` or `edit_design_system()` functions (server.py:105, 197).

**Change API Port**: Update port in both uvicorn.run and modal component fetch URLs (CreateSystemModal.tsx:22, EditSystemModal.tsx:29).
