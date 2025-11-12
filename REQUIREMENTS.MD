Design System Generator — Requirements Document (Markdown)

Goal: Build a single-file generator that outputs a complete, self-contained index.html showcasing and documenting a fully functional, accessible, themeable design system. After generation, an LLM (or a human) can modify the system by following embedded comment directives.

⸻

1) Scope & Objectives

Primary outcome
	•	Produce one deliverable: index.html containing:
	•	Design tokens (CSS custom properties), scales, and themes
	•	Core foundations (type, color, spacing, elevation, motion, grid)
	•	A comprehensive set of UI components (markup, styles, and JS behaviors)
	•	Usage guidelines, accessibility notes, code examples, live playgrounds
	•	Built-in LLM edit hooks via structured HTML comments and data attributes

Non-goals
	•	No external network requests (fonts, icons, CSS/JS). Everything is inlined.
	•	No bundling pipeline required by the consumer: single file only.
	•	No JS frameworks; rely on vanilla JS + Web Components are optional but not required.

Success criteria
	•	Opening index.html in any evergreen browser displays the docs site + component gallery.
	•	Changing tokens or component variants via LLM directives or manual edits updates visuals consistently.
	•	Meets WCAG 2.2 AA for included components (see §7).

⸻

2) Personas & Use Cases
	•	Designers: Browse tokens and components; copy usage guidance; toggle themes/scales.
	•	Engineers: Copy/paste examples; inspect accessible markup; integrate tokens.
	•	Docs writers: Edit guidelines inline; add patterns, do/don’t lists.
	•	LLM agents: Apply structured changes (e.g., change primary color, add a component variant) using embedded directive syntax.

⸻

3) Deliverables & File Layout

Single file: index.html must include:
	•	<head>: metadata, <style> blocks (base + themes + utilities + components), optional <template> blocks, and optional embedded SVG symbol sprite.
	•	<body>:
	•	Header (brand, search, theme switcher, density switcher)
	•	Nav (left sidebar with foundations/components/patterns)
	•	Main content (docs + live previews + code tabs)
	•	Footer (version, license, generation timestamp)
	•	<script>: vanilla JS for interactivity, copy-code, playground controls, theme/density switches, and LLM directive processor (optional live application of directives).

⸻

4) Design Tokens (Foundations)

All tokens must be exposed as CSS custom properties and documented in tables with live swatches.

4.1 Token Namespacing
	•	Prefix all tokens with --ds-.
	•	Group tokens by area: --ds-color-*, --ds-space-*, --ds-font-*, --ds-radius-*, --ds-shadow-*, --ds-motion-*, --ds-z-*, --ds-size-*, --ds-border-*, --ds-opacity-*.

4.2 Color System
	•	Semantic tokens (recommended):
	•	--ds-bg, --ds-bg-muted, --ds-surface, --ds-surface-raised,
	•	--ds-text, --ds-text-muted, --ds-border,
	•	--ds-primary, --ds-primary-contrast,
	•	--ds-success, --ds-warning, --ds-danger, --ds-info, each with -emphasis when needed
	•	State overlays: --ds-hover, --ds-active, --ds-focus-ring
	•	Variant ramps (per color family): --ds-primary-50 … 900.
	•	Contrast: ensure semantic text/background meet AA (≥ 4.5:1 body, ≥ 3:1 large text/icons).

4.3 Typography
	•	Scales: --ds-font-size-50 … 1000 (modular or custom).
	•	Line height: --ds-line-compact, --ds-line-default, --ds-line-loose.
	•	Families: --ds-font-sans, --ds-font-mono.
	•	Weights: --ds-font-weight-regular, --ds-font-weight-medium, --ds-font-weight-bold.
	•	Letter-spacing tokens for headings and UI labels (optional).

4.4 Spacing & Sizing
	•	Spacing scale: --ds-space-0 (0) to --ds-space-16 (e.g., 64px).
	•	Component size scale: --ds-size-sm|md|lg|xl for controls and targets (min target ≥ 44×44 CSS px).

4.5 Radius & Elevation
	•	Radii: --ds-radius-none, --ds-radius-sm, --ds-radius-md, --ds-radius-lg, --ds-radius-full.
	•	Shadows: --ds-shadow-0 … 5 with subtle, non-blurry AA-compliant shadows.
	•	Borders: --ds-border-width-1|2, --ds-border-color, --ds-border-style.

4.6 Motion
	•	Durations: --ds-duration-fast|normal|slow.
	•	Easings: --ds-ease-standard, --ds-ease-emphasized.
	•	Reduced motion: respect prefers-reduced-motion.

4.7 Z-Index
	•	Layer tokens: --ds-z-base, --ds-z-sticky, --ds-z-overlay, --ds-z-popover, --ds-z-modal, --ds-z-toast.

⸻

5) Theming & Modes
	•	Base theme on :root.
	•	Additional themes via [data-theme="light"], [data-theme="dark"], [data-theme="brandX"], etc., overriding semantic tokens only.
	•	Support high-contrast variant [data-contrast="high"].
	•	Density/compact mode via [data-density="compact|comfortable"] toggling --ds-space-* and control heights.

Runtime switching: Provide UI toggles that set data-theme/data-density on <html> and persist via localStorage.

⸻

6) Layout, Grid & Utilities
	•	Grid system: CSS grid utilities with 12-col defaults at sm, md, lg, xl breakpoints (tokens for breakpoints).
	•	Containers: responsive max-width tokens.
	•	Utility classes: margin/padding, flex/grid helpers, text align/weight, display/visibility, width/height, overflow, position, z-index, radius, shadow, cursor.

⸻

7) Accessibility Requirements (WCAG 2.2 AA)
	•	Keyboard support for all interactive components (Tab, Shift+Tab, Arrow keys, Esc).
	•	Focus states: visible, non-color-only indicators (use --ds-focus-ring).
	•	ARIA roles, states, and names per component (documented next to examples).
	•	Color contrast rules in docs; theme switch should never break contrast.
	•	Reduced motion support.
	•	Form controls with labels, descriptions, and error messaging tied via id/aria-*.
	•	RTL support: [dir="rtl"] verified on key components (buttons, forms, menus, tables).
	•	I18n/l10n readiness: text nodes in examples are easily replaceable; date/number formats not hard-coded.

⸻

8) Components (Minimum Set)

Each component section must include:
	1.	Overview and usage guidance
	2.	Accessibility notes (roles, keyboard, ARIA)
	3.	Anatomy (labeled diagram or bullets)
	4.	Variants & States (default/hover/focus/active/disabled/loading)
	5.	Responsive behavior
	6.	Live preview with knobs (size, variant, disabled, icon, etc.)
	7.	Copyable code (HTML+minimal JS, and token references)

Required components:
	•	Core Inputs: Button, Icon Button, Link, Input, Textarea, Select, Combobox (optional), Checkbox, Radio, Switch, Slider, Range, File Upload, Rating (optional)
	•	Feedback: Badge, Chip/Tag, Tooltip, Popover, Toast/Notification, Alert, Progress, Skeleton
	•	Navigation: Tabs, Accordion, Breadcrumbs, Pagination, Navbar/Top App Bar, Sidebar, Dropdown Menu, Command Menu/Quick Search (optional)
	•	Containers: Card, Modal/Dialog, Drawer/Sheet, Table (sortable, selectable, paginated), List, Data Grid (simple)
	•	Media & Misc: Avatar, Carousel (optional), Steps, Calendar/Date Picker (basic)
	•	Layout Blocks: Page header, Empty state, Sign-in panel (mock), Settings form (pattern)
	•	Icons: Inline SVG sprite with a documented icon set and <svg><use href="#..."></use></svg> usage.

⸻

9) Patterns & Templates
	•	Form patterns: validation messages, required indicators, helper text, error summaries.
	•	Content patterns: do/don’t, voice & tone examples.
	•	Page templates:
	•	Dashboard (cards, table, filters)
	•	Detail page (tabs, side panel)
	•	Settings page (forms, accordions)
	•	Auth pages (mock layout only)

⸻

10) Documentation Site Features (within index.html)
	•	Search (client-side fuzzy search over headings and component names).
	•	Sidebar nav with section highlighting.
	•	Playgrounds: per component live controls (attributes toggles, content text).
	•	Code tabs: HTML (required), “Token refs” (shows which tokens affect the example).
	•	Copy buttons for code and tokens.
	•	Theme/Density toggles in header.
	•	Contrast checker tool: foreground vs background in place.
	•	RTL toggle to flip direction and preview.
	•	Audit panel (optional): lists contrast violations or missing ARIA in examples.
	•	Version & build info: generation timestamp, semantic version, commit/seed hash.

⸻

11) JavaScript Conventions
	•	Vanilla JS; no global pollution—namespace under window.DS (e.g., window.DS.applyTheme()).
	•	Module pattern with small helpers: dom(), on(), toggleAttr(), prefersReducedMotion().
	•	Event handling: delegate where possible.
	•	State synchronized to attributes/classes to keep CSS simple.
	•	No external dependencies; icons embedded as SVG symbols; optional small inline base64 images.

⸻

12) Performance & Quality
	•	One file target budgets (unminified guidance; not strict hard caps):
	•	CSS: ≤ 80 KB
	•	JS: ≤ 80 KB
	•	SVG sprite: ≤ 40 KB (depends on icon count)
	•	Avoid layout thrash; prefer CSS transitions; throttle resize/scroll listeners.
	•	Paint containment where useful (contain CSS).
	•	Lazy-init heavy interactive examples (e.g., tables) when visible.

⸻

13) Testing & Validation (Manual within index.html)
	•	Accessibility checklist per component (checkbox list).
	•	Keyboard walk-through script (prints detected focus traps).
	•	Contrast checks for all semantic pairs.
	•	Visual regression hooks: stable data-testid attributes on examples.
	•	LTR/RTL snapshot toggles.

⸻

14) LLM Edit Protocol (Directives)

Enable safe, structured modifications by embedding machine-readable comments and stable hooks:

14.1 Comment Directive Format
	•	HTML comment blocks anywhere inside index.html:

<!-- LLM:DIRECTIVE
{
  "id": "change-primary-color-001",
  "target": "token",
  "action": "update",
  "path": "--ds-primary",
  "value": "#3B82F6",
  "rationale": "Increase vibrancy for links and buttons",
  "scope": ["[data-theme='light']", "[data-theme='dark']"]
}
-->

Supported directive targets:
	•	"token": update CSS custom property values in specified scopes.
	•	"component": add/update a variant, state style, or anatomy part.
	•	"theme": create a new [data-theme="brandX"] block with overrides.
	•	"docs": insert or update documentation text or examples.
	•	"pattern": add a new page template or example section.
	•	"icon": add/replace SVG symbols (base64 or inline path).

14.2 Attribute Hooks
	•	Every token table row includes data-ds-token="--ds-primary" (or actual token name).
	•	Every component example wrapper includes data-ds-component="button" and data-variant="solid|outline|ghost", etc.
	•	The docs section has data-ds-docs-section="foundations/colors" etc.

14.3 Directive Processing
	•	Optional inline JS function DS.applyDirectives() can parse all <!-- LLM:DIRECTIVE ... --> blocks and:
	•	Locate and update <style> token definitions within the right scope.
	•	Inject new theme blocks or component style rules at the end of the main style sheet.
	•	Update docs DOM nodes targeted by data-ds-* hooks.
	•	Provide a “Apply Directives” button that re-parses comments and applies changes at runtime (for human preview).

14.4 Changeset Log
	•	Maintain an append-only Changeset panel (collapsible) showing directive IDs, timestamps, and success/failure status.

⸻

15) Security & Safety
	•	No external scripts; no eval of arbitrary JS from directives (only token/style/docs updates).
	•	Sanitize any innerHTML updates (docs text updates only allow a safe subset or text-only).
	•	Restrict directive "target" operations to known whitelisted areas.

⸻

16) Versioning & Metadata
	•	<meta name="generator" content="Design System Generator vX.Y.Z">
	•	data-build="YYYY-MM-DDTHH:mm:ssZ" on <html>.
	•	Document semver and change log in a “Release notes” section.

⸻

17) Licensing & Attributions
	•	Default to a permissive license snippet (e.g., MIT) embedded in a “License” section.
	•	If shipping sample icons, ensure they’re license-compatible and documented.

⸻

18) Example: Token Definition Style Block (Skeleton)

/* Foundations: base tokens */
:root,
:root[data-theme="light"] {
  --ds-bg: #ffffff;
  --ds-surface: #ffffff;
  --ds-text: #111827;
  --ds-text-muted: #4b5563;
  --ds-border: #e5e7eb;

  --ds-primary: #0ea5e9;
  --ds-primary-contrast: #ffffff;

  --ds-success: #16a34a;
  --ds-warning: #f59e0b;
  --ds-danger:  #ef4444;
  --ds-info:    #3b82f6;

  --ds-focus-ring: 0 0 0 3px rgba(14,165,233,0.4);

  --ds-font-sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji","Segoe UI Emoji";
  --ds-font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;

  --ds-font-size-100: 12px;
  --ds-font-size-200: 14px;
  --ds-font-size-300: 16px;
  --ds-font-size-400: 18px;
  --ds-font-size-500: 20px;

  --ds-space-0: 0;
  --ds-space-1: 4px;
  --ds-space-2: 8px;
  --ds-space-3: 12px;
  --ds-space-4: 16px;
  --ds-space-6: 24px;
  --ds-space-8: 32px;

  --ds-radius-sm: 6px;
  --ds-radius-md: 10px;
  --ds-radius-lg: 14px;

  --ds-shadow-1: 0 1px 2px rgba(0,0,0,0.06), 0 1px 1px rgba(0,0,0,0.04);

  --ds-duration-fast: 120ms;
  --ds-duration-normal: 200ms;
  --ds-duration-slow: 320ms;
  --ds-ease-standard: cubic-bezier(.2,.0,.2,1);
}

:root[data-theme="dark"] {
  --ds-bg: #0b0f14;
  --ds-surface: #0f1620;
  --ds-text: #e5e7eb;
  --ds-text-muted: #9ca3af;
  --ds-border: #1f2937;

  --ds-primary: #38bdf8; /* elevated contrast in dark */
  --ds-primary-contrast: #0b0f14;

  --ds-focus-ring: 0 0 0 3px rgba(56,189,248,0.35);
}

/* Density */
:root[data-density="compact"] {
  --ds-space-2: 6px; /* example tweak */
  --ds-space-3: 10px;
}


⸻

19) Example: Button Component (Skeleton)

Accessibility: <button type="button" aria-label="…">, focus ring, 44px target.

<div class="ds-example" data-ds-component="button" data-variant="solid">
  <button class="ds-btn ds-btn--primary">Primary</button>
  <button class="ds-btn ds-btn--outline">Outline</button>
  <button class="ds-btn ds-btn--ghost" disabled>Ghost disabled</button>
</div>

.ds-btn {
  font: 600 14px/1 var(--ds-font-sans);
  min-height: 40px;
  padding: 0 var(--ds-space-4);
  border-radius: var(--ds-radius-md);
  border: 1px solid transparent;
  transition: background-color var(--ds-duration-normal) var(--ds-ease-standard),
              border-color var(--ds-duration-normal) var(--ds-ease-standard),
              box-shadow var(--ds-duration-fast) var(--ds-ease-standard);
}

.ds-btn:focus-visible {
  outline: none;
  box-shadow: var(--ds-focus-ring);
}

.ds-btn--primary {
  color: var(--ds-primary-contrast);
  background: var(--ds-primary);
}
.ds-btn--primary:hover { filter: brightness(0.96); }
.ds-btn--primary:active { transform: translateY(1px); }

.ds-btn--outline {
  color: var(--ds-text);
  background: transparent;
  border-color: var(--ds-border);
}
.ds-btn--outline:hover { background: rgba(0,0,0,.03); }

LLM directive to update the primary color:

<!-- LLM:DIRECTIVE
{ "id":"btn-primary-color","target":"token","action":"update","path":"--ds-primary","value":"#7c3aed" }
-->


⸻

20) Example: Docs Section Structure

<section id="foundations-colors" data-ds-docs-section="foundations/colors">
  <h2>Colors</h2>
  <p>Use semantic tokens to ensure theme resilience.</p>
  <table class="ds-token-table">
    <thead><tr><th>Token</th><th>Value</th><th>Sample</th></tr></thead>
    <tbody>
      <tr data-ds-token="--ds-primary">
        <td><code>--ds-primary</code></td>
        <td><code>#0ea5e9</code></td>
        <td><span class="swatch" style="background:var(--ds-primary)"></span></td>
      </tr>
    </tbody>
  </table>
</section>


⸻

21) Build/Growth Hooks
	•	Add a new component: Provide a docs template snippet (anatomy/ARIA/variants/preview/code).
	•	Extend themes: Template for [data-theme="brand-new"] overrides + docs card.
	•	Icon pipeline: Instructions for adding an SVG <symbol> and its docs row.

⸻

22) Quality Gates & Acceptance Criteria
	•	index.html opens with no console errors.
	•	All required components render and demonstrate states.
	•	Theme toggle switches tokens and maintains AA contrast.
	•	Keyboard navigation works across interactive components.
	•	“Copy code” works.
	•	“Apply Directives” updates tokens/styles/docs according to valid directives.
	•	LTR/RTL toggle doesn’t break layout of core nav/menu/tabs/table.
	•	prefers-reduced-motion respected (no essential info conveyed by motion only).
	•	At least one template page (Dashboard) demonstrates system composition.

⸻

23) Optional Enhancements
	•	Web Components wrappers (<ds-button>, <ds-tabs>) with progressive enhancement.
	•	Theming sandbox: color pickers write to tokens live with delta preview.
	•	Export: button to download a JSON of current tokens, or a stripped CSS file.
	•	Inline unit tests (very light) asserting available tokens and ARIA attributes.
	•	Design token JSON comment block for external tooling:

<!-- LLM:TOKENS
{
  "color": {"primary":"var(--ds-primary)","text":"var(--ds-text)"},
  "space": {"2":"var(--ds-space-2)"}
}
-->


⸻

24) Generator Inputs (if applicable)
	•	Brand Config (optional): seed colors, logo SVG, font stacks (system defaults if omitted).
	•	Component selection: allow toggling optional components (carousel, command menu).
	•	Accessibility strictness: enable extra lint rules/messages in docs.

⸻

25) Maintenance
	•	Keep tokens semantic-first to survive theme changes.
	•	Use data-ds-* hooks consistently so LLMs can target stable selectors.
	•	Append changes in Changeset rather than overwriting history.

⸻

Endnote

This requirements doc defines the minimum complete design system generator output for a single, richly documented index.html. The embedded LLM directive protocol and data-ds-* hooks allow safe, structured modifications post-generation.