<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

# MovieScore Frontend

## Architecture

This is a Next.js application using the App Router, TypeScript, React, and Tailwind CSS. The frontend is organized by responsibility:

```text
app/          Next.js routes, pages, the root layout, and global styles
components/   reusable visual components
	ui/         generic interface primitives (Button, Logo)
	features/   components grouped by product feature (auth, landing)
actions/      server-side operations exposed as Server Actions
lib/          shared application support code
	routes/     backend endpoint URL builders
	schemas/    Zod runtime validation schemas and inferred form types
	types/      shared TypeScript contracts for API data and pagination
	utils.ts    generic utilities
public/       static assets
```

The current request flow is:

```text
app page -> feature component -> action -> lib/routes + lib/types -> backend API
												 |
												 -> lib/schemas (form validation where needed)
```

`app/` owns URL-addressable UI. For example, `app/cadastro/page.tsx` composes feature components; it should not contain reusable form implementation. `components/features/` owns feature-specific UI and behavior, while `components/ui/` is reserved for primitives that are genuinely reusable across unrelated features.

## Server And Client Boundaries

- Keep pages and components as Server Components by default.
- Add `"use client"` only when a component needs browser interaction, hooks, form state, or a browser-only library. `FormCadastro` is the existing example.
- Keep server-only API mutations and reads in `actions/`. Files containing Server Actions must start with `"use server"`.
- Client Components may import actions intended to be called from the client, but should not import server-only implementation details or backend credentials.
- Do not move Server Actions into visual components merely for convenience.
- Handle action failures explicitly. The existing actions currently log errors and may return `undefined`; preserve or improve the return contract when extending them so callers can render a meaningful state.

## Data And Validation Conventions

- Put backend URL construction in `lib/routes/`; use `lib/routes/api.ts` for the backend base URL and domain modules such as `usuario.ts` for endpoint paths.
- Put shared API request and response contracts in `lib/types/`. Reuse existing types such as `CursorPaging` instead of duplicating them in pages or components.
- Put Zod schemas in `lib/schemas/` when they are shared by a feature or define an external/input contract. Infer form types from schemas with `z.infer` when possible.
- Keep API calls inside actions rather than directly in presentational components.
- Use the `@/*` path alias for imports from the frontend root, for example `@/components/ui/Button` and `@/lib/utils`.

## UI Conventions

- Global design tokens live in `app/globals.css`; use the existing CSS variables and Tailwind theme names (`primary`, `secondary`, `background`, and `foreground`) instead of introducing duplicate colors.
- The application language is Portuguese (`pt-BR`); keep user-facing text consistent with that language.
- The project uses Poppins through `next/font/google` in `app/layout.tsx`.
- Use existing UI primitives before creating another equivalent button, logo, or input component.
- Keep links and navigation in the appropriate page or feature component. Use Next.js navigation components/APIs when navigation behavior requires it.

## Naming conventions

- Component files: PascalCase, matching the exported component name (`FormCadastro.tsx` → `FormCadastro`).
- Non-component files (lib, actions, routes): lowercase (`usuario.ts`).

## Change Guidance For Agents

Before adding a file, identify its owner:

- URL-addressable screen: `app/<route>/page.tsx`.
- Feature-specific visual behavior: `components/features/<feature>/`.
- Cross-feature visual primitive: `components/ui/`.
- Server-side backend operation: `actions/`.
- Shared endpoint, validation, or type contract: the corresponding `lib/` subdirectory.

Prefer small, local changes that follow these boundaries. Do not create a catch-all `lib` module or duplicate a type/schema solely to avoid an import. When a feature grows, keep its closely related UI together under `components/features/`; only introduce a feature-level abstraction when it removes real duplication.

After changes, run the narrowest relevant check first, then use the project scripts as needed:

```bash
npm run lint
npm run build
```
