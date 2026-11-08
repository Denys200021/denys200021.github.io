# Recruiter View + Production Quality Upgrade — QA Report

**Release date:** 2026-11-09  
**Project:** Legioniz Personal Portfolio  
**Scope:** Integrate the recruiter-focused profile and production-quality controls into the existing portfolio system.

## Implemented

### Recruiter experience

- Added a dedicated, shareable recruiter profile at `/?view=recruiter`.
- Connected entry points from the full portfolio navigation, hero, footer, and command palette.
- Kept the recruiter profile as a dynamically imported view within the same React application.
- Reused project, skill, education, achievement, and experience data from the existing portfolio data/configuration instead of maintaining a separate copy.
- Prioritized three technical projects and the most relevant IT support and teaching experience, while retaining additional employment history in a disclosure.
- Added a responsive, optimized portrait; project hand-offs into the full case-study dialog; browser-history support; responsive layout; keyboard skip link; print styling; and accessible section navigation.
- Exposed only the public-safe CV PDF in Recruiter View. No DOC/DOCX/ODT files are shipped in public assets.
- Qualified OSINT/cybersecurity details as foundational, self-directed practice in owned or explicitly authorized lab environments.

### Production quality and release controls

- Added canonical metadata, Open Graph and Twitter social metadata, a 1200×630 PNG sharing preview, Person JSON-LD, robots.txt, sitemap.xml, and a web app manifest.
- Updated document and social-preview title/description when moving between recruiter and full-portfolio modes.
- Added Lighthouse CI collection for both the full portfolio and recruiter view, with three runs and accessibility, SEO, best-practices, LCP, CLS, and total-blocking-time assertions.
- Configured Lighthouse reports to stay in the CI workspace and attach to the workflow as a private, 14-day run artifact instead of public temporary storage.
- Added production asset budgets and checks for bundle sizes, image payloads, source maps, private document leakage, and privileged credentials.
- Added automated production dependency auditing, strict TypeScript project checks, Vite production build, adaptive tests, feature/security tests, desktop/touch browser tests, and Lighthouse gates before GitHub Pages deployment.
- Kept deployment limited to successful non-pull-request workflow runs; pull requests run verification only.
- Maintained Supabase boundaries: public browser configuration only, RLS-backed private tables, and server-side submission validation. The Supabase project remains unconfigured and persistent admin/inquiry features are not represented as live.
- Corrected the shared accent foreground token so primary buttons maintain the tested WCAG AA text-contrast ratio in dark and light themes.

## Verification performed in this environment

| Check | Result |
|---|---:|
| Feature and backend source/security checks | **58/58 passed** |
| Recruiter, SEO, accessibility, responsive, privacy, and production-source checks | **50/50 passed** |
| Portfolio static source preflight | **Passed** |
| Adaptive profile smoke tests (desktop, touch, data-saver, reduced-motion, zoom, DPR cap, fallback, resize coalescing) | **Passed** |
| Python test-script compilation | **Passed** |
| TypeScript/TSX syntax transpilation | **15 files, 0 diagnostics** |
| CSS parsing | **Passed** (1505 root nodes parsed) |
| package.json and Lighthouse config JSON | **Valid** |
| GitHub Actions and Dependabot YAML syntax | **Valid** |
| Open Graph PNG integrity | **Passed** (1200×630 PNG) |
| Public editable-document scan | **No DOC/DOCX/ODT files found** |
| Archive integrity | **Verified at packaging** |

## Environment limitation — not certified locally

The environment could not resolve `registry.npmjs.org`. A direct dependency installation attempt failed with:

```text
npm error code EAI_AGAIN
getaddrinfo EAI_AGAIN registry.npmjs.org
```

The npm cache was empty. Consequently, dependencies could not be installed and the following were **not run or measured locally**:

- Full `tsc -b` semantic project typecheck.
- Vite production build and emitted bundle/asset-budget audit.
- Real Chromium tests against the compiled React application.
- Lighthouse scores or measured lab performance values.

These are wired into `.github/workflows/deploy.yml` and `.lighthouserc.json` for execution in the repository's connected CI environment. No Lighthouse score, Core Web Vitals result, successful deployment, or live Supabase integration is claimed by this report.

## Release notes

- The recruiter CV action links to `public/King-Art-Pacumberto-CV.pdf`, the public-safe PDF.
- The full portfolio still includes `public/King-Art-Pacumberto-Resume.pdf`, the original owner-supplied PDF, which contains the phone number from that original file. Review its publication decision before deploying.
- The package has no `.env` secret file, service-role key, private CV variant, Word document, `node_modules`, `dist`, or local backup folder.
- The workflow can deploy through GitHub Pages only after it runs successfully in the target repository and GitHub Pages is configured for Actions.
