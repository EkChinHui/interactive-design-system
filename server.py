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

# Helper function to check if HTML is complete
def is_html_complete(html: str) -> bool:
    """Check if HTML document is complete with proper closing tags"""
    html_lower = html.lower().strip()

    # Check for essential closing tags
    has_closing_html = '</html>' in html_lower
    has_closing_body = '</body>' in html_lower

    # Check if it ends properly (not mid-tag or mid-attribute)
    ends_properly = html_lower.endswith('</html>') or html_lower.endswith('</html>\n')

    return has_closing_html and has_closing_body and ends_properly

# Helper function to get the last N characters for context
def get_continuation_context(html: str, chars: int = 2000) -> str:
    """Get the last N characters of HTML for continuation context"""
    return html[-chars:] if len(html) > chars else html

# Helper function to call LLM
async def call_llm(user_prompt: str, system_prompt: str = "", max_tokens: int = 64000) -> str:
    """Call LLM using litellm"""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    response = litellm.completion(
        model="anthropic/claude-sonnet-4-5-20250929",
        messages=messages,
        temperature=0.7,
        max_tokens=max_tokens,
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

        # Check if HTML is complete, if not, continue generation
        continuation_attempts = 0
        max_continuations = 5  # Prevent infinite loops

        while not is_html_complete(cleaned_html) and continuation_attempts < max_continuations:
            continuation_attempts += 1
            print(f"HTML incomplete, continuing generation (attempt {continuation_attempts}/{max_continuations})...")

            # Get context from the end of the current HTML
            context = get_continuation_context(cleaned_html)

            continuation_prompt = f"""The previous response was cut off. Here is where it ended:

...{context}

Please continue from EXACTLY where this left off and complete the rest of the HTML document. Do NOT repeat any of the content shown above. Start immediately from where it was cut off and continue until the document is complete with proper closing tags (</body> and </html>).

Output ONLY the continuation HTML code, no explanations or markdown code blocks."""

            print(f"Requesting continuation from position: ...{context[-100:]}")

            # Get continuation
            continuation = await call_llm(continuation_prompt, "")
            cleaned_continuation = clean_html(continuation)

            # Append continuation to existing HTML
            cleaned_html += "\n" + cleaned_continuation

            print(f"Added {len(cleaned_continuation)} characters. Total length: {len(cleaned_html)}")

        if is_html_complete(cleaned_html):
            print(f"✓ HTML generation complete after {continuation_attempts} continuation(s)")
        else:
            print(f"⚠ Warning: HTML may still be incomplete after {max_continuations} attempts")

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

        # Check if HTML is complete, if not, continue generation
        continuation_attempts = 0
        max_continuations = 5  # Prevent infinite loops

        while not is_html_complete(cleaned_html) and continuation_attempts < max_continuations:
            continuation_attempts += 1
            print(f"HTML incomplete, continuing generation (attempt {continuation_attempts}/{max_continuations})...")

            # Get context from the end of the current HTML
            context = get_continuation_context(cleaned_html)

            continuation_prompt = f"""The previous response was cut off. Here is where it ended:

...{context}

Please continue from EXACTLY where this left off and complete the rest of the HTML document. Do NOT repeat any of the content shown above. Start immediately from where it was cut off and continue until the document is complete with proper closing tags (</body> and </html>).

Output ONLY the continuation HTML code, no explanations or markdown code blocks."""

            print(f"Requesting continuation from position: ...{context[-100:]}")

            # Get continuation
            continuation = await call_llm(continuation_prompt, "")
            cleaned_continuation = clean_html(continuation)

            # Append continuation to existing HTML
            cleaned_html += "\n" + cleaned_continuation

            print(f"Added {len(cleaned_continuation)} characters. Total length: {len(cleaned_html)}")

        if is_html_complete(cleaned_html):
            print(f"✓ HTML generation complete after {continuation_attempts} continuation(s)")
        else:
            print(f"⚠ Warning: HTML may still be incomplete after {max_continuations} attempts")

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

@app.delete("/api/design-system/{file_name}")
async def delete_design_system(file_name: str):
    """Delete a design system file"""
    try:
        # Validate file name to prevent path traversal
        if '/' in file_name or '\\' in file_name or '..' in file_name:
            raise HTTPException(status_code=400, detail="Invalid file name")

        file_path = Path(__file__).parent / "public" / "systems" / file_name

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Design system file not found")

        # Delete the file
        file_path.unlink()

        print(f"Design system deleted: {file_path}")

        return {"success": True, "fileName": file_name}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting design system: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete design system: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server on http://localhost:3001")
    print("Available endpoints:")
    print("  POST   /api/generate-design-system")
    print("  POST   /api/edit-design-system")
    print("  DELETE /api/design-system/{file_name}")
    print("  GET    /api/design-systems")
    uvicorn.run(app, host="0.0.0.0", port=3001)
