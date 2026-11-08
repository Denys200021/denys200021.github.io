# GitHub Pages deployment

This project is configured as the GitHub user site for **Legioniz**. The intended public URLs are:

- Full portfolio: https://legioniz.github.io/
- Recruiter View: https://legioniz.github.io/?view=recruiter

## 1. Create the destination repository

In GitHub, create a **public** repository named exactly `Legioniz.github.io`. Leave **Add a README**, `.gitignore`, and license unchecked so the repository starts empty. The connected GitHub account did not expose an existing portfolio or `Legioniz.github.io` repository when this release was prepared.

## 2. Push the files

1. Extract this ZIP to a normal folder on your Windows PC.
2. Install Git for Windows and Node.js 22.12+ (or 20.19+).
3. Sign in to GitHub through Git Credential Manager when prompted.
4. Double-click `PUSH-TO-GITHUB.cmd`.

The script attempts to generate `package-lock.json` when npm registry access is available, creates a local `main` branch, and pushes to `https://github.com/Legioniz/Legioniz.github.io.git` using a separate `portfolio-live` remote. It never force-pushes. If lockfile generation is unavailable, the script warns and continues; the workflow still installs the exact-pinned direct dependencies.

If you prefer manual commands, open CMD inside the extracted folder and run:

```cmd
npm install --package-lock-only --ignore-scripts --no-audit --no-fund
git init
git branch -M main
git remote add origin https://github.com/Legioniz/Legioniz.github.io.git
git add -A
git commit -m "Deploy portfolio to GitHub Pages"
git push -u origin main
```

## 3. Enable GitHub Pages

Open the repository's **Settings → Pages → Build and deployment** and choose **GitHub Actions** as the source. The included workflow also runs `actions/configure-pages@v5`, verifies the project, builds `dist/`, uploads the Pages artifact, and deploys it after all checks pass.

Follow **Actions → Verify and deploy portfolio to GitHub Pages**. A green completed run means GitHub accepted the deployment. The site will then be available at the URLs above. First publication and DNS/edge propagation can take several minutes.

## 4. Public live preview on the same Wi-Fi

Double-click `START-PORTFOLIO-LAN.cmd`. It prints a local URL and, where available, your LAN IPv4 URL. Anyone on the same network can open the LAN URL while your PC and the dev server remain on. Windows Firewall may ask permission; allow private networks only. This is **not** a public Internet tunnel.

For a persistent public link, use GitHub Pages. Do not expose the Vite development server directly to the public Internet.

## Deployment boundaries

- The Pages workflow deploys the static frontend only. Supabase still requires your own project, database migration, Edge Function deployment, and public build variables before persistent backend features are active.
- Do not commit `.env.local`, service-role keys, Turnstile secrets, or other private credentials. `.gitignore` excludes `.env*` while retaining `.env.example`.
- The original Resume PDF contains a phone number and remains in the Full Portfolio public assets. Recruiter View exposes the public-safe CV PDF only. Review `CONTENT-CHECKLIST.md` before the first public deployment.
- The repo is configured for a root user site; do not move it into a differently named project repository without adjusting `vite.config.ts` base paths, canonical URLs, sitemap, and service-worker scope.
