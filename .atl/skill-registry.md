# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

See `_shared/skill-resolver.md` for the full resolution protocol.

---

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| When creating a pull request, opening a PR, or preparing changes for review | branch-pr | `c:\Users\HP 15\.copilot\skills\branch-pr\SKILL.md` |
| When writing Go tests, using teatest, or adding test coverage | go-testing | `c:\Users\HP 15\.copilot\skills\go-testing\SKILL.md` |
| When creating a GitHub issue, reporting a bug, or requesting a feature | issue-creation | `c:\Users\HP 15\.copilot\skills\issue-creation\SKILL.md` |
| When user says "judgment day", "judgment-day", "review adversarial", "dual review", "doble review", "juzgar", "que lo juzguen" | judgment-day | `c:\Users\HP 15\.copilot\skills\judgment-day\SKILL.md` |
| When user asks to create a new skill, add agent instructions, or document patterns for AI | skill-creator | `c:\Users\HP 15\.copilot\skills\skill-creator\SKILL.md` |

---

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### branch-pr
- Every PR MUST link an approved issue via `Closes #N`, `Fixes #N`, or `Resolves #N` — no exceptions
- Every PR MUST have exactly ONE `type:*` label
- Branch naming: `type/description` — regex `^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)\/[a-z0-9._-]+$`
- Run `shellcheck` on any modified shell scripts before opening PR
- PR body MUST use `.github/PULL_REQUEST_TEMPLATE.md` structure
- Automated checks must pass before merge is possible; blank PRs without issue linkage are blocked

### go-testing
- Use table-driven tests for all cases: `tests := []struct{ name, input, expected string; wantErr bool }{...}` with `t.Run(tt.name, ...)`
- Test Bubbletea TUI with `teatest.NewTestModel(t, model, teatest.WithInitialTermSize(w, h))`
- Simulate keys with `tea.KeyMsg{Type: tea.KeyEnter}`; assert model state directly
- Name test files `*_test.go`; target ≥70% coverage
- Use golden files for stable snapshot testing (avoid brittle string assertions on rendered output)
- External dependencies in tests must be mocked; never hit real network/filesystem in unit tests

### issue-creation
- MUST use a template (bug report or feature request) — blank issues are disabled
- Every issue gets `status:needs-review` automatically on creation
- Maintainer MUST add `status:approved` before any PR can be opened
- Search for duplicates first; questions go to Discussions, not Issues
- Bug reports require: description, steps to reproduce, expected vs actual behavior, OS/agent/shell fields

### judgment-day
- Launch TWO independent sub-agents in parallel (async delegate) — never sequential, never self-review
- Both judges receive identical target + context but work in isolation — no cross-contamination
- Categorize after both return: Confirmed (both found) → fix immediately; Suspect (one only) → triage; Contradiction → escalate to user
- Max 2 iterations before final report; re-judge only if fixes were applied
- Inject project compact rules (from `.atl/skill-registry.md`) into BOTH judge prompts AND fix agent prompt

### skill-creator
- Create `skills/{skill-name}/SKILL.md` with YAML frontmatter including `name`, `description`, `license`, `metadata`
- Frontmatter `description` MUST include `Trigger:` phrase — this is how skills are auto-detected and loaded
- Include `## Critical Patterns` (actionable patterns with minimal examples) and `## Rules` sections
- Compact rules: 5-15 lines of actionable constraints only — no motivation, no full examples, no fluff
- NEVER create a skill for a one-off task; skills are for repeated patterns

---

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| homepower-stack.instructions.md | `.github/instructions/homepower-stack.instructions.md` | Stack constraints, non-negotiable rules, and B2B wholesale context for all HTML/CSS/JS/PHP work |

### homepower-stack compact rules
- Stack is fixed: HTML5 + CSS3 + Vanilla JS + PHP 8+ — do NOT recommend React, Vue, Angular, Next.js, jQuery, Bootstrap, Tailwind, or heavy libraries
- Mobile-first is mandatory — all changes must prioritize small-screen readability and thumb-friendly spacing; desktop improvements must never harm mobile
- WhatsApp is the primary CTA — optimize for WhatsApp button visibility, prefilled messages, and low-friction contact paths
- All user-facing copy must be in Spanish unless explicitly requested otherwise
- B2B wholesale buyer context: prioritize credibility, catalog confidence, and low-friction inquiry flow — avoid DTC/checkout-style patterns
- Prefer semantic HTML + modular CSS + minimal JS; no unnecessary third-party dependencies
- WCAG 2.1 AA compliance is required on all changes
- Do not change core file structure, naming conventions, deployment flow, or PHP endpoints without explicit approval
- Images must be WebP; prefer lazy-loading for non-critical assets

---

*Generated: 2026-04-15 | Project: Homepowerpty.com*
