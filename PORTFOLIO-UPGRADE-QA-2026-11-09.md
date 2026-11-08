# Portfolio Full-Experience Upgrade — QA & Release Report

**Release date:** 9 November 2026  
**Baseline:** `Legioniz_Portfolio_Senior_Dev_Motion_Disclosure_Fix_2026-11-08.zip`  
**Status:** Source implementation and available QA passed; production build and deployment remain unverified.

## What changed

The previous React/Vite portfolio was extended in-place. Existing theme, motion, sound, scroll-aware masthead, section reveals, project cards, project details, portrait assets, resume links, and accessible disclosures were retained.

### Interactive identity and navigation

- Added a short, skippable opening sequence. It follows the visitor's saved motion preference and the operating-system reduced-motion preference.
- Project case studies can be opened with `?project=<project-id>`, copied as shareable URLs, and navigated with browser back/forward history.
- Added a project comparison view, a searchable command palette, section quick navigator, and reading-progress indicator.
- Extended the career/activities record without manufacturing dates or credentials that were not supplied.

### Project and technical showcases

- **Project Laboratory:** local exposure/EV100 calculator and an editable appliance-energy estimator. The energy model is illustrative and not a live utility tariff or bill calculation.
- **Capability map:** connects documented skills to actual portfolio projects without fabricated proficiency scores.
- **Photography workspace:** responsive, browser-local image gallery with aspect filtering, a treatment slider, and keyboard-accessible viewer. Files are not uploaded. Limits are 12 MB per image, 24 images, 48 MB total, and 45 megapixels per decoded image. The archive starts empty because no public portfolio photo set was supplied.
- **Network Lab:** educational simulation using RFC 5737 documentation-only addresses and fictional hosts/services. It makes no network connection, discovery scan, or request to real systems.
- **OSINT journal:** fictional case study, source-verification checklist, and privacy/authorization boundaries.
- **Hardware Lab:** simplified LM35-to-PWM fan-control model, explicitly identified as a teaching model rather than a claim of exact firmware behavior.
- **Developer Notebook** and **Currently Building** board.

### Inquiry, privacy, and owner console

- Added inquiry and moderated-comment flows, a Supabase Auth-backed owner console, analytics summary, JSON export, status/edit/archive/delete operations, and administrative activity records.
- Added a Supabase SQL migration with row-level security enabled for every application table, least-privilege grants, approved-comment reads, administrator-only inquiry management, and a service-role-only quota function.
- Added a server-side Edge Function for origin checking, bounded JSON request bodies, validation, honeypot, rate quotas, HMAC-derived network bucket identifiers, and optional server-side Cloudflare Turnstile verification.
- The frontend uses only the Supabase URL and public anon key. Service-role, CAPTCHA, and rate-limit secrets remain server-side.
- Analytics are opt-in and limited to random session UUID, path, and timestamp. The consent control is not shown when analytics are not configured.
- When no backend is configured, the inquiry experience falls back to a prefilled email rather than implying that a message was stored. Comments and owner-console data functions remain unavailable until setup is complete.

### Performance, accessibility, and delivery

- Retained adaptive animation behavior and reduced-motion fallbacks; intro, image viewer, and owner console support keyboard dismissal/focus handling.
- Added a versioned production service worker for static assets only. Database, auth, function, and storage API paths are explicitly excluded from caching.
- Added a public copy of `BACKEND-SETUP.md` so the owner-console setup link resolves after static deployment.
- Integrated feature/security checks into `npm run verify` and `npm run release`.
- No additional animation framework or image-heavy runtime dependency was introduced.

## Verification results

| Check | Result |
|---|---|
| `node scripts/portfolio.mjs check` | **PASS** — source/content/config preflight, required assets and deployment files |
| `python tests/feature-security-qa.py` | **PASS** — 52/52 feature and security source assertions |
| `node --experimental-strip-types tests/adaptive-smoke.ts` | **PASS** — desktop, touch, data-saver, reduced motion, zoom, DPR cap, invalid input, resize coalescing |
| `python tests/interactions-browser-qa.py` | **PASS** — 29/29 Chromium interaction checks; no fixture browser errors |
| `python tests/portfolio-motion-qa.py` | **PASS** — reveals, disclosure transitions, reduced motion, masthead behavior, seven viewport widths; no browser errors |
| TypeScript transpile diagnostics | **PASS** — 16 TypeScript/TSX files; zero syntax errors |
| Supplemental strict TypeScript source check | **PASS** — with local minimal React declarations because the actual React type packages were not installable in this environment |
| Supabase Edge Function strict TypeScript check | **PASS** — with a minimal declaration for the Deno runtime API |
| CSS parse | **PASS** — 1,284 top-level rules; zero top-level syntax errors |
| `BACKEND-SETUP.md` public copy | **PASS** — byte-identical to the source guide |
| ZIP integrity / manifest | See release package manifest |

## Not verified / release prerequisites

1. **Production build:** `npm install --no-audit --no-fund --fetch-retries=0 --fetch-timeout=30000` could not complete because the environment could not resolve `registry.npmjs.org` (`EAI_AGAIN`). Consequently, the official project `tsc -b`, Vite production build, and browser test against the compiled React application were not run. The browser tests above exercise the production motion/sound modules and test fixture, not a built React bundle.
2. **Supabase runtime:** No Supabase project or credentials were provided. The SQL migration has not been applied to a live project, and the Edge Function has not been deployed or exercised against a live database. Configure it by following `BACKEND-SETUP.md`; never place service-role or other server secrets in Vite/client variables.
3. **Photography content:** The photo workspace is functional but starts empty. Add only images that are cleared for public portfolio use if you want a populated public archive.
4. **GitHub Pages deployment:** No repository push or deployment was performed. Confirm the target repository and GitHub Pages settings before publishing.
5. **Original resume privacy:** `public/King-Art-Pacumberto-Resume.pdf` is the supplied original PDF and contains a phone number. Remove or replace it before public deployment if that number should not be public. The redesigned public CV PDF is the phone-free alternative. The DOCX was removed from the site and release assets in the November 9 PDF-only update.

## Release commands

```bash
npm install
npm run check
npm run test:adaptive
npm run test:features
npm run test:interactions
npm run test:motion
npm run verify
npm run preview
```

Use `npm run release` for a checksum-verified local backup followed by preflight, adaptive tests, feature/security checks, official TypeScript project check, and Vite build. Review the generated `dist/` output before deployment.


## Follow-up UI patch — collapsible section navigator

The right-side section navigator is now a compact edge tab. It expands when hovered or keyboard-focused, collapses when the pointer leaves, and can be pinned open with its visible toggle. Touch screens use the toggle rather than hover. Hidden section links are removed from keyboard tab order while collapsed; the active section index remains visible in the collapsed rail. The scroll threshold and active-section tracking are unchanged.
