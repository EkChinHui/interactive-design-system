from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import litellm
import os
from pathlib import Path
import re

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class GenerateSystemRequest(BaseModel):
    name: str
    prompt: str

class EditSystemRequest(BaseModel):
    fileName: str
    comment: str

class GenerateSystemResponse(BaseModel):
    success: bool
    fileName: str
    path: str
    content: str

class EditSystemResponse(BaseModel):
    success: bool
    fileName: str
    content: str

class DesignSystemInfo(BaseModel):
    fileName: str
    path: str
    name: str

class DesignSystemsListResponse(BaseModel):
    systems: list[DesignSystemInfo]

# Helper function to clean HTML from markdown code blocks
def clean_html(content: str) -> str:
    """Remove markdown code blocks from LLM response"""
    cleaned = content
    if '```html' in content:
        cleaned = re.sub(r'```html\n?', '', content)
        cleaned = re.sub(r'```\n?', '', cleaned)
    elif '```' in content:
        cleaned = re.sub(r'```\n?', '', content)
    return cleaned.strip()

# Helper function to call LLM
async def call_llm(user_prompt: str, system_prompt: str = "") -> str:
    """Call LLM using litellm"""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    response = litellm.completion(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=16000
    )

    return response.choices[0].message.content

@app.post("/api/generate-design-system", response_model=GenerateSystemResponse)
async def generate_design_system(request: GenerateSystemRequest):
    """Generate a new design system using LLM"""
    try:
        # Read requirements file for context
        requirements_path = Path(__file__).parent.parent / "REQUIREMENTS.MD"
        requirements = ""

        if requirements_path.exists():
            requirements = requirements_path.read_text()

        system_prompt = f"""You are an expert web designer and developer. Create a complete, self-contained HTML design system file.

{f"Follow these requirements:\n{requirements}\n" if requirements else ""}

IMPORTANT INSTRUCTIONS:
- Create a COMPLETE single-file HTML document with embedded CSS and JavaScript
- Include comprehensive design tokens using CSS custom properties
- Include a full component library (buttons, inputs, cards, alerts, badges, tables, forms, etc.)
- Make it fully accessible (WCAG 2.2 AA compliant)
- Include interactive examples and documentation
- The design should be unique, creative, and follow the user's aesthetic requirements
- Include light/dark theme support
- Output ONLY the HTML code, no explanations or markdown code blocks"""

        user_prompt = f"""Create a design system with the following characteristics: {request.prompt}

The design system should be named "{request.name}" and should include all standard components while following the aesthetic described above."""

        print(f"Generating design system: {request.name}")
        html_content = await call_llm(user_prompt, system_prompt)

        # Clean up the response
        cleaned_html = clean_html(html_content)

        # Save the file
        file_name = f"{request.name.lower().replace(' ', '-')}.html"
        file_path = Path(__file__).parent / "public" / "systems" / file_name

        file_path.write_text(cleaned_html)

        print(f"Design system saved to {file_path}")

        return GenerateSystemResponse(
            success=True,
            fileName=file_name,
            path=f"/systems/{file_name}",
            content=cleaned_html
        )

    except Exception as e:
        print(f"Error generating design system: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate design system: {str(e)}")

@app.post("/api/edit-design-system", response_model=EditSystemResponse)
async def edit_design_system(request: EditSystemRequest):
    """Edit an existing design system using LLM"""
    try:
        # Read the existing file
        file_path = Path(__file__).parent / "public" / "systems" / request.fileName

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Design system file not found")

        existing_content = file_path.read_text()

        system_prompt = """You are an expert web designer and developer. You are editing an existing HTML design system file based on user feedback.

IMPORTANT INSTRUCTIONS:
- Modify the existing HTML design system according to the user's comment
- Maintain the overall structure and existing components unless specifically asked to change them
- Keep all CSS custom properties and design tokens consistent
- Ensure accessibility is maintained (WCAG 2.2 AA compliant)
- Output ONLY the complete modified HTML code, no explanations or markdown code blocks
- Make surgical, precise changes based on the feedback"""

        user_prompt = f"""Here is the existing design system HTML:

{existing_content}

User feedback/change request: {request.comment}

Please modify the design system according to this feedback and return the complete updated HTML."""

        print(f"Editing design system: {request.fileName}")
        updated_html = await call_llm(user_prompt, system_prompt)

        # Clean up the response
        cleaned_html = clean_html(updated_html)

        # Save the updated file
        file_path.write_text(cleaned_html)

        print(f"Design system updated at {file_path}")

        return EditSystemResponse(
            success=True,
            fileName=request.fileName,
            content=cleaned_html
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error editing design system: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to edit design system: {str(e)}")

@app.get("/api/design-systems", response_model=DesignSystemsListResponse)
async def list_design_systems():
    """List all design systems"""
    try:
        systems_dir = Path(__file__).parent / "public" / "systems"

        files = [
            DesignSystemInfo(
                fileName=f.name,
                path=f"/systems/{f.name}",
                name=f.stem.replace('-', ' ')
            )
            for f in systems_dir.glob("*.html")
        ]

        return DesignSystemsListResponse(systems=files)

    except Exception as e:
        print(f"Error listing design systems: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list design systems: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server on http://localhost:3001")
    print("Available endpoints:")
    print("  POST /api/generate-design-system")
    print("  POST /api/edit-design-system")
    print("  GET  /api/design-systems")
    uvicorn.run(app, host="0.0.0.0", port=3001)
