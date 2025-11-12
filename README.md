# Design System Showcase

A React + TypeScript + Vite application with AI-powered design system generation and editing capabilities.

## 🎨 Featured Design Systems

1. **Modern Design System** - Clean, accessible, and themeable with comprehensive components
2. **FRESH** - Bold, vibrant with neon gradients and glowing effects
3. **Studio** - Refined, minimal, and sophisticated with exceptional typography
4. **Doodle DS** - Hand-drawn, sketchy design inspired by Excalidraw
5. **Aquarelle** - Watercolor-inspired with soft edges and gentle transparency

## 🚀 Getting Started

### Prerequisites
- Node.js 20.19+ or 22.12+
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for Python package management
- An LLM API key (e.g., OpenAI)

### Installation

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies (done automatically by uv)
# No manual pip installation needed!
```

### Setup API Key

```bash
# Set your LLM API key (example for OpenAI)
export OPENAI_API_KEY=your-api-key-here
```

### Running the Application

You need to run both the frontend and backend servers:

```bash
# Terminal 1: Run frontend development server
npm run dev
# Frontend will be available at http://localhost:5173/

# Terminal 2: Run backend API server
npm run server
# Backend will be available at http://localhost:3001/
```

### Build for Production

```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
showcase/
├── public/
│   └── systems/              # HTML design system files
│       ├── index.html        # Modern Design System
│       ├── fresh.html        # FRESH
│       ├── refined.html      # Studio
│       ├── doodle.html       # Doodle DS
│       └── watercolor.html   # Aquarelle
├── src/
│   ├── components/
│   │   ├── CreateSystemModal.tsx  # Modal for creating new systems
│   │   ├── EditSystemModal.tsx    # Modal for editing systems
│   │   └── Modal.css              # Modal styles
│   ├── App.tsx               # Main application component
│   ├── App.css               # Application styles
│   └── main.tsx              # Entry point
├── server.py                 # FastAPI backend server
├── pyproject.toml            # Python dependencies (uv)
└── package.json              # Node.js dependencies
```

## ✨ Features

### Core Features
- **Interactive Navigation** - Browse through all design systems
- **Live Preview** - Each design system loads in an iframe
- **Responsive Design** - Works on desktop and mobile
- **Dark Theme** - Clean dark UI for the showcase
- **Quick Access** - Open any design system in a new tab

### AI-Powered Features
- **🤖 Generate New Design Systems** - Click "+ New System" to create custom design systems using AI
  - Describe your desired aesthetic in natural language
  - AI generates a complete HTML design system with all components
  - Automatically added to your showcase

- **✏️ Edit Existing Systems** - Click the edit button (✎) on any system
  - Request changes in plain English (e.g., "make buttons rounder", "change colors to purple")
  - AI surgically modifies the design system while preserving structure
  - Changes reflected immediately in the preview

## 🛠️ Technologies

### Frontend
- React 18
- TypeScript
- Vite
- CSS3

### Backend
- FastAPI
- LiteLLM (multi-provider LLM support)
- Python 3.12+
- uv (modern Python package manager)

## 📝 Usage

### Viewing Design Systems
1. Click on any design system in the sidebar to view it
2. Hover over the preview to see system information
3. Click "Open in new tab" to view the design system in full screen
4. Use the menu button to toggle the sidebar on/off

### Creating New Design Systems
1. Click the **"+ New System"** button in the header
2. Enter a name for your design system
3. Describe the aesthetic you want in the prompt field
   - Example: *"A cyberpunk-inspired design system with neon colors, dark backgrounds, and futuristic fonts"*
4. Click **"Generate Design System"** and wait for the AI to create it
5. The new system will automatically appear in your sidebar

### Editing Existing Design Systems
1. Select any design system from the sidebar
2. Click the **edit button (✎)** that appears on the active system
3. Describe the changes you want to make
   - Example: *"Make all buttons more rounded"*, *"Change the primary color to purple"*
4. Click **"Update Design System"** and the changes will be applied
5. The iframe will automatically reload with your changes

## 🎯 Design System Details

Each design system is a complete, self-contained HTML file with:
- Full component library
- Design tokens
- Live interactive examples
- Accessibility features
- Documentation

## 🔌 API Endpoints

The FastAPI backend provides these endpoints:

### `POST /api/generate-design-system`
Generate a new design system using AI.

**Request Body:**
```json
{
  "name": "Cyberpunk",
  "prompt": "A futuristic design system with neon colors..."
}
```

**Response:**
```json
{
  "success": true,
  "fileName": "cyberpunk.html",
  "path": "/systems/cyberpunk.html",
  "content": "<!DOCTYPE html>..."
}
```

### `POST /api/edit-design-system`
Edit an existing design system using AI.

**Request Body:**
```json
{
  "fileName": "cyberpunk.html",
  "comment": "Make all buttons more rounded"
}
```

**Response:**
```json
{
  "success": true,
  "fileName": "cyberpunk.html",
  "content": "<!DOCTYPE html>..."
}
```

### `GET /api/design-systems`
List all available design systems.

**Response:**
```json
{
  "systems": [
    {
      "fileName": "index.html",
      "path": "/systems/index.html",
      "name": "index"
    }
  ]
}
```

## 🎨 Supported LLM Providers

LiteLLM supports 100+ LLM providers. Configure by setting the appropriate environment variable:

- **OpenAI**: `OPENAI_API_KEY`
- **Anthropic**: `ANTHROPIC_API_KEY`
- **Azure**: `AZURE_API_KEY`
- **Cohere**: `COHERE_API_KEY`
- And many more...

To change the model, edit `server.py` and update the `model` parameter in the `litellm.completion()` call.

Enjoy exploring and creating unique design systems!
