# Frontend Development Skills - Installed for Claude Code

## Installed Skills (5 Total)

### 1. **Next.js + React + TypeScript**
- **Skill**: `nextjs-react-typescript`
- **Source**: mindrally/skills
- **Location**: `~/.agents/skills/nextjs-react-typescript`
- **Perfect For**:
  - Next.js 16 + React 19 best practices
  - TypeScript patterns and conventions
  - Server components and client components
  - App Router optimization
  - Performance tuning

### 2. **shadcn/ui Components**
- **Skill**: `shadcn-ui`
- **Source**: existential-birds/beagle
- **Location**: `~/.agents/skills/shadcn-ui`
- **Perfect For**:
  - shadcn/ui component implementation
  - Radix UI primitives
  - Accessible component patterns
  - Component composition
  - Used extensively in drafted-recruiter

### 3. **Tailwind CSS**
- **Skill**: `tailwind-css`
- **Source**: bobmatnyc/claude-mpm-skills
- **Location**: `~/.agents/skills/tailwind-css`
- **Perfect For**:
  - Tailwind CSS utilities and patterns
  - Responsive design
  - Custom configurations
  - Design tokens
  - Both drafted-seeker and drafted-recruiter use this

### 4. **Design System Architect**
- **Skill**: `design-system-architect`
- **Source**: daffy0208/ai-dev-standards
- **Location**: `~/.agents/skills/design-system-architect`
- **Perfect For**:
  - Building cohesive design systems
  - Component library architecture
  - Design token management
  - Consistency across applications
  - Scalable component patterns

### 5. **UX Designer** (Bonus!)
- **Skill**: `ux-designer`
- **Source**: daffy0208/ai-dev-standards
- **Location**: `~/.agents/skills/ux-designer`
- **Perfect For**:
  - User experience patterns
  - Interaction design
  - Accessibility best practices
  - User flow optimization
  - Interface usability

---

## How These Skills Help Your Projects

### For drafted-seeker-nextjs:
✅ Next.js 16 + React 19 expertise
✅ Material-UI + Tailwind CSS optimization
✅ Framer Motion animations
✅ Form handling (Formik + Yup)
✅ Performance optimization

### For drafted-recruiter:
✅ Vite + React 18 + TypeScript patterns
✅ shadcn/ui + Radix UI components
✅ Tailwind CSS utilities
✅ React Hook Form + Zod integration
✅ Component architecture

---

## Usage

These skills are now automatically available to Claude Code! When you ask me to:

- **Build components**: I'll use shadcn/ui patterns
- **Style interfaces**: I'll apply Tailwind CSS best practices
- **Structure apps**: I'll follow Next.js conventions
- **Design systems**: I'll create cohesive, scalable patterns
- **Improve UX**: I'll apply accessibility and usability principles

---

## Example Prompts

**Component Creation:**
```
"Create a new shadcn/ui card component for displaying user profiles"
"Build a responsive navigation using Tailwind CSS"
```

**Next.js Optimization:**
```
"Optimize this Next.js page for performance"
"Convert this component to a server component"
```

**Design System:**
```
"Create a design token system for our color palette"
"Build a reusable button component with variants"
```

**UX Improvements:**
```
"Review this form for accessibility issues"
"Suggest UX improvements for this checkout flow"
```

---

## Updating Skills

To update all skills to their latest versions:

```bash
npx skills check    # Check for updates
npx skills update   # Update all skills
```

To remove a skill:

```bash
npx skills remove <skill-name>
```

---

## Additional Skills Available

If you need more specialized skills, search for them:

```bash
npx skills find "animation"     # For animation skills
npx skills find "testing"        # For testing skills
npx skills find "performance"    # For optimization skills
```

Browse all skills at: https://skills.sh/

---

## Notes

- Skills are installed globally (user-level)
- They work across all Claude Code sessions
- Skills have full agent permissions
- Each skill includes specialized prompts and knowledge
- Skills are automatically loaded when Claude Code starts

**Your frontend development capabilities are now enhanced!** 🎨⚡
