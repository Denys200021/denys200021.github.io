# Recruiter / Full Portfolio View-Transition QA

**Release date:** 2026-11-09  
**Scope:** Recruiter View, full portfolio, project case-study routing, browser history, DOM-bound observers, scroll behavior, and PWA cache lifecycle.

## Defect reproduced from source inspection

The top-level `App` component remains mounted while its conditional return swaps the entire rendered tree between `RecruiterView` and the full `.site-shell`. Several effects had dependencies that did not include the view state, or used an empty dependency array. They therefore initialized against the initial DOM tree and did not rebind when that tree was removed and re-created.

This left stale references in:

- The direction-aware masthead scroll controller.
- The section `IntersectionObserver` used by the main navigation.
- The scroll-reveal `useLayoutEffect` and its `#main-content` target.
- The off-screen motion-zone observer.

The user-facing symptom was a partially initialized or apparently incomplete full portfolio after switching out of Recruiter View. A refresh recreated all observers, which explains why refreshing appeared to repair it.

## Changes

1. **Masthead lifecycle:** detach while Recruiter View is active; bind against the current header when the full portfolio returns.
2. **Section tracking:** disconnect on recruiter entry, reset the active section, and register the full set of section nodes again on return. A safe fallback marks `home` active when `IntersectionObserver` is unavailable.
3. **Scroll reveal:** do not create a body-wide observer for Recruiter View. Install before paint against the current `#main-content` element each time the full portfolio tree mounts.
4. **Motion zones:** detach while recruiter mode is active and observe the newly mounted full-view motion zones after exit.
5. **Layout scroll position:** explicit view transitions and recruiter-to-project transitions reset scroll immediately. Browser back/forward resets scroll only when the active layout changes; same-layout project history can retain its scroll position.
6. **PWA cache:** advance the shell cache from `v3` to `v4` to ensure deployed clients do not retain the previous app shell.
7. **Regression test:** extend `tests/recruiter-view-browser-qa.py` to assert that main sections, reveal readiness, header/progress, Quick Navigator, downward/upward masthead behavior, back/forward navigation, and repeated round trips work without reloading.

## Checks completed in this environment

| Check | Result |
|---|---:|
| Project source preflight | Passed |
| Feature and security assertions | 58/58 passed |
| Production-source assertions | 55/55 passed |
| Adaptive runtime smoke suite | Passed |
| TypeScript / TSX syntax transpilation | 15 files, 0 syntax errors |
| Python QA script compilation | Passed |
| Node syntax checks (`scripts/portfolio.mjs`, `public/sw.js`) | Passed |
| CSS parser | Passed |
| Deployment and Dependabot YAML parsing | Passed |
| ZIP integrity | Passed |

## Checks not certified locally

- The Vite production preview could not start because dependencies are not installed (`vite` executable missing; preview process exited with status 127).
- `npm install` could not complete because the environment could not resolve `registry.npmjs.org` (DNS resolution failure / `EAI_AGAIN`).
- The full `npm run typecheck`, compiled-app Chromium browser suite, production build, and measured Lighthouse audits therefore remain unverified in this environment. The browser regression test has been updated and is included in the GitHub Actions verification workflow.

The TypeScript syntax-transpilation check is not a substitute for full semantic typechecking. No browser-test pass or Lighthouse score is claimed in this report.
