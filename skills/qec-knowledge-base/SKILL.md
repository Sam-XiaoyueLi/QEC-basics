---
name: qec-knowledge-base
description: Create and update Markdown topic pages for this QEC knowledge base after study and discussion, maintain README indexes, and connect related pages and notebooks. Also use for related-topic checks when notebooks are added or updated or substantive QEC discussions occur in this project.
---

# QEC knowledge base

## Scope and location

The user studies a topic independently, discusses it with Codex, and asks Codex to consolidate it into a topic page. Preserve the user's reasoning and learning questions while correcting errors with explanation.

Work in the QEC basics Git repository: when the workspace contains `Notebooks/qec_knowledge_base`, the repository root is `Notebooks`; when already inside that repository, use its root. Topic pages belong in `qec_knowledge_base/`. Basic tutorial PDFs belong in `qec_basic_notes/`. The repository copy of this skill is `skills/qec-knowledge-base/SKILL.md`.

Create or substantially rewrite a topic page when requested. Discussion alone should prompt connection checks, not automatic creation of a full article. Do not commit, push, publish, or schedule background work unless requested.

## Before writing or linking

Read the repository README, `qec_knowledge_base/README.md`, relevant existing topic pages, and the current discussion. Inventory existing Markdown pages and notebooks; read the relevant notebook Markdown cells and code when needed to establish a real connection. Use the user's named relationships as additional evidence. Do not infer relationships solely from filenames.

Reuse an existing topic page when appropriate; otherwise use a descriptive lowercase hyphenated `.md` filename. Start with a flat topic collection; introduce subfolders only when the material warrants them. Use normal Markdown links and GitHub-compatible LaTeX math: `$...$` inline and `$$...$$` for display equations. Define notation before use and link prerequisites.

## Consistent topic-page format

Use this order for every topic page. The contents should be adapted to the topic, rather than padded to fill a template.

```markdown
# Topic title

Status: Draft | Working notes | Reviewed
Last updated: YYYY-MM-DD

## Overview

## Basic intuitions

## Formal descriptions

## Worked examples

## Limitations

## Open questions

## Related topics

## References
```

Choose one status, not the literal list. Use `Draft` for an initial incomplete page and `Working notes` for a developed but evolving explanation. Use `Reviewed` only after an explicit technical review, identifying its scope. Date actual edits using the user's local date.

- **Overview:** Explain what the topic is, why it matters, scope, and prerequisites; link existing prerequisite explanations.
- **Basic intuitions:** Build the conceptual picture before equations. Explain the limits of analogies.
- **Formal descriptions:** Give definitions, notation, assumptions, and mathematical statements. For code topics, include construction, stabilizers, logical operators, and parameters when supported. For decoder topics, include inputs, outputs, noise assumptions, and objective when relevant. Do not force these details onto unrelated topics.
- **Worked examples:** Give at least one concrete, checkable example when feasible, with intermediate reasoning. Link a relevant existing notebook for executable detail. Clearly label illustrative or unexecuted code; do not invent simulation results. If a meaningful example is not yet available, keep the section and state the specific gap.
- **Limitations:** Describe applicability, computational or implementation constraints, and assumptions. Attach noise model, decoder, finite-size conditions, and sources to performance claims when relevant.
- **Open questions:** Distinguish the user's unanswered learning questions from established research questions. Cite sources for claims that a question is open in the field. Keep uncertainty explicit.
- **Related topics:** Link relevant existing pages, notebooks, and basic tutorials, with one sentence explaining each connection. Use relative links to actual files. For useful future topics, use plain text explicitly marked `Planned; no page yet`, without fabricated links.
- **References:** Cite primary papers or official technical documentation near the claims they support and collect readable source links here. Distinguish published results, deductions, the user's interpretation, and unverified statements. Verify niche, uncertain, or recent claims against sources rather than relying on memory.

## Maintain the knowledge network and indexes

Whenever a topic page is created or edited:

1. Scan the current folder and notebooks for relevant material; update the page's Related topics section with supported connections.
2. Where the connection helps readers of an existing topic page, add or update its reciprocal Related topics entry. Avoid duplicate links and do not force every connection to be reciprocal.
3. Add or update the entry in `qec_knowledge_base/README.md`, including title, relative link, brief description, and status. Replace the initial empty-state text when the first page exists.
4. For each newly added Markdown topic page, add its title, relative link, and brief description under Knowledge base in the repository `README.md`. Update entries when pages are renamed or their scope changes. Index content pages, not skill files or other maintenance documents.

When a notebook is added or updated, inspect its actual subject matter and relevant topic pages. Update existing Related topics sections where there is a meaningful connection, and tell the user briefly which connections were added. Apply the same check during substantive QEC discussions; if a discussed topic has no saved page or notebook, mention the potential connection or label it as planned rather than claiming there is a linkable artifact. There is no background watcher: perform these checks during active work in this project.

Respect user-provided relationships, explain any technically misleading connection, and use judgment to avoid a web of weak links. When updating a page's links, update its last-updated date. Keep each index entry unique and the two README files consistent.

## Finish

Check that local links resolve, linked sections exist, math and examples are internally consistent, and the requested headings are present. Perform technical checks appropriate to actual examples; report what was and was not executed. Report the saved topic page, index updates, meaningful related-topic changes, and any unresolved gaps. Keep the summary concise.
