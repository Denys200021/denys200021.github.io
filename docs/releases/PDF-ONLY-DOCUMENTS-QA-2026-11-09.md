> **Historical release record.** This report documents an earlier incremental build and is retained for traceability. Its test results and file inventory are not the status of the current release. See [`FULL-SYSTEM-AUDIT-2026-11-09.md`](../../FULL-SYSTEM-AUDIT-2026-11-09.md) for the current audit.

---

# PDF-only Personal Documents QA — 2026-11-09

## Requested change

The portfolio should present personal CV/resume downloads as PDF files only. Editable Word/DOCX downloads and public DOCX assets must not be available.

## Implemented

- Retained `public/King-Art-Pacumberto-Resume.pdf`, the exact owner-supplied original resume.
- Retained `public/King-Art-Pacumberto-CV.pdf`, the redesigned public-safe CV.
- Removed `public/King-Art-Pacumberto-CV.docx` from the release.
- Removed the DOCX path from `src/config.ts`.
- Removed Word/DOCX download controls from the header, hero, and contact section.
- Removed Word/DOCX links from the boot/no-JavaScript and React error fallbacks.
- Updated the release preflight to assert that no Word/ODT file is present in `public/` and no DOCX path is configured or rendered.
- Updated README and current document guidance to state the PDF-only policy.

## Verification

- `npm run check`: passed.
- Adaptive profile smoke tests: passed.
- Feature/security QA: 58/58 passed.
- Public personal-document inventory: exactly two PDF files; no DOCX/DOC/ODT assets.
- Resume PDF SHA-256: `99950a214cfa96e400802d3d2266250322ea7ded6c9cfe3ead046259913fc383`.
- Public CV PDF SHA-256: `dccd1565dbbc570c58533e06030474b319af3825b53bfd4b96c535f7f3c305e6`.
- Original resume PDF signature and size: passed.
- Public-safe CV PDF signature and size: passed.
- ZIP integrity: passed.

## Privacy note

The original owner-supplied resume PDF contains the phone number printed in that document. The public-safe CV PDF omits it. Both are still downloadable, as requested; replace the original resume PDF with a redacted copy before public deployment if the phone number should not be exposed.

## Scope

This change removes Word format exposure; it does not combine the two distinct PDF documents. They remain separately labeled as Resume PDF and Public CV PDF.
