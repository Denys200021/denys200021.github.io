# GitHub Pages Jekyll workflow setup QA — 2026-11-09

## Result

The portfolio deployment workflow now uses the official `actions/jekyll-build-pages@v1` action while preserving the existing React/Vite application build and verification pipeline.

## Build and deployment sequence

1. GitHub Actions checks out the repository and configures GitHub Pages with `actions/configure-pages@v5`.
2. Node.js 22 and Python 3.11 are configured; Node and browser test dependencies are installed.
3. `npm run verify` runs the full source, type, browser, production build, and bundle-budget gates. Vite writes the compiled website to `dist/`.
4. `.github/jekyll/_config.yml` is copied into `dist/_config.yml` so Jekyll reads the root-site URL and metadata while processing the compiled static output.
5. `actions/jekyll-build-pages@v1` runs with `source: ./dist` and `destination: ./_site`.
6. The workflow asserts that `_site/index.html`, `_site/assets`, and both public PDF downloads exist, then adds `.nojekyll` to the deploy artifact.
7. `actions/upload-pages-artifact@v4` uploads `./_site`; `actions/deploy-pages@v4` deploys it only after the verification/package job succeeds.

Jekyll is deliberately a packaging step here. It does not compile React or TypeScript; Vite performs that work first. The workflow uses the official Jekyll build action and GitHub Pages artifact/deploy actions documented by GitHub.

## Configuration

- Repository target: `Legioniz/Legioniz.github.io`
- Canonical URL: `https://legioniz.github.io/`
- Jekyll `url`: `https://legioniz.github.io`
- Jekyll `baseurl`: empty string (user-site root)
- Jekyll source: `./dist`
- Jekyll destination: `./_site`
- GitHub Pages publishing source: GitHub Actions
- Single workflow: `.github/workflows/deploy.yml`

Do not create a second deployment workflow from the template picker. The committed workflow already invokes the official Jekyll build action and handles verification, artifact upload, and deployment.

## Automated checks

- Source preflight: passed.
- Feature/security: 59/59 passed.
- Cross-file integrity: 30/30 passed.
- Production-source/SEO/accessibility/security: 68/68 passed.
- Adaptive runtime smoke test: passed for desktop, touch, data-saver, reduced-motion, zoomed viewport, invalid-input fallback, and resize coalescing.
- Chromium design and hero checks: 22/22 passed.
- Desktop/touch interaction checks: 29/29 passed.
- Scroll, disclosure, motion, and masthead browser regression: a previous run completed successfully, but the latest repeat timed out while entering the `education-disclosure` step. This latest repeat is not counted as a pass; it is not a Jekyll workflow failure and should be rerun on the GitHub Actions runner or a local browser environment.
- Ruby YAML parsing: passed for the GitHub Actions workflow, Dependabot config, and Jekyll config.
- Workflow ordering and artifact checks: passed in the cross-file integrity suite.

## Remaining external verification

The Jekyll action itself runs on a GitHub-hosted runner and was not executed locally in this workspace. The React/Vite production build was also not run locally because the release workspace does not have the Node dependencies installed and npm registry access was previously unavailable. The GitHub Actions workflow is configured to perform those checks before deployment. A `package-lock.json` is not included; CI currently uses `npm install` with exact direct dependency versions rather than `npm ci`.

No repository push or GitHub Pages deployment has been performed by this setup change.
