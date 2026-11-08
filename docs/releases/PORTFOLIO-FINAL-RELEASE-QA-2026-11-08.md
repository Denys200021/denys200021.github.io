> **Historical release record.** This report documents an earlier incremental build and is retained for traceability. Its test results and file inventory are not the status of the current release. See [`FULL-SYSTEM-AUDIT-2026-11-09.md`](../../FULL-SYSTEM-AUDIT-2026-11-09.md) for the current audit.

---

# Portfolio Final Release QA — Header, Motion & Disclosures

Date: 2026-11-08

## User-facing fixes

- The complete masthead now hides on a downward scroll and reappears on an upward scroll. It remains visible near the top, while the mobile menu is open, while keyboard focus is inside the header, and when motion is paused.
- The play/pause button is enabled even when the OS requests reduced motion. The default follows the OS preference; a deliberate site-level click can opt into motion or pause it. The setting is stored under `legion-portfolio-motion-v4`; old v1-v3 values are ignored.
- Hero, profile, projects, skills, experience, education-related content, and contact sections use bidirectional enter/exit reveals with re-entry when scrolling back.
- Skill groups, work-history entries, extracurricular items, education history, achievement details, and project notes use consistent native disclosures.
- Disclosure panels animate between `minmax(0, 0fr)` and `minmax(0, 1fr)` plus opacity. The zero minimum prevents grid auto-minimum sizing from leaving a closed panel partly visible.
- The achievement detail selector was narrowed to `.achievement-detail`; it no longer styles every descendant `div` and overrides the disclosure panel layout.
- The `KA` header mark remains one line across the tested mobile, tablet, and desktop widths. Typography uses balanced headings, readable body measure, and system-font fallbacks.

## Checks passed

- `npm run check` — static source, content, asset, path, and configuration preflight passed.
- `npm run test:adaptive` — passed for desktop, touch, data saver, reduced motion, zoomed viewport, DPR cap, invalid-input fallback, and resize coalescing.
- `npm run test:motion` / `python tests/portfolio-motion-qa.py` — passed in Chromium. Verifies section enter/exit/re-entry, dynamic project insertion, skill/education/achievement disclosure open and keyboard-close, OS reduced-motion default, site-level motion opt-in, header down/up movement, menu/top/motion guards, and `KA` layout at seven viewport widths.
- `python tests/interactions-browser-qa.py` — 29/29 interaction assertions passed.
- Standalone TypeScript checking passed for `adaptive.ts`, `reveal.ts`, `masthead.ts`, `sound.ts`, `config.ts`, and `data.ts`.
- TypeScript/TSX syntax transpilation passed for 10 application/configuration source files.
- CSS parser passed: 936 top-level rules and zero parse errors.
- `index.html` parsed with Python's HTML parser; both public SVG resources parsed as XML.
- ZIP integrity, current public document paths, original resume PDF signature, and absence of private CVs in `public/` verified.

## Not verified

- `npm run typecheck` and the Vite production build are not verified because this working environment does not have React, React DOM, their type packages, Vite, or the React Vite plugin installed. The attempted typecheck reports missing modules; this is an environment/dependency blocker, not a passing build.
- The source has not been pushed to GitHub and GitHub Pages has not been deployed.

## Ports and privacy

- Development: `5174` (strict port).
- Preview: `4174` (strict port).
- `public/King-Art-Pacumberto-Resume.pdf` is the exact original uploaded resume and includes the phone number printed on it. Anyone who can access the deployed site can download it. The redesigned public-safe CV PDF and DOCX omit the phone number.
