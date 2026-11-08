> **Historical release record.** This report documents an earlier incremental build and is retained for traceability. Its test results and file inventory are not the status of the current release. See [`FULL-SYSTEM-AUDIT-2026-11-09.md`](../../FULL-SYSTEM-AUDIT-2026-11-09.md) for the current audit.

---

# Original Resume Integration QA — 2026-11-08

## What changed

- Added the exact PDF uploaded by the owner (`King_Art_Pacumberto_Resume_Updated (1)(3).pdf`) to `public/King-Art-Pacumberto-Resume.pdf`.
- Verified the destination file is byte-for-byte identical to the uploaded file using SHA-256.
- Added a dedicated `resumeOriginalPath` in `src/config.ts`; the legacy `resumePath` points to the same original resume for consistency.
- Added an explicit “RESUME” download in the header.
- Added “Original Resume · PDF” in the hero and contact sections.
- Added the original resume to the initial boot fallback, no-JavaScript fallback, and React error boundary.
- Kept the redesigned public-safe CV PDF and editable DOCX as separate downloads.
- Updated the source preflight to require and validate the original PDF and its entry points.

## Document choices shown on the website

1. Original Resume (PDF): exact uploaded one-page resume. It includes the phone number printed in the source document.
2. Public-safe CV (PDF): redesigned two-page CV without the phone number.
3. Editable CV (Word): redesigned two-page DOCX without the phone number.

## Privacy

The original resume is in the public assets directory because the owner specifically requested it be implemented in the portfolio. Deploying GitHub Pages makes the phone number in that exact PDF publicly downloadable. The public-safe CV alternatives remain available for visitors who should not receive that phone number.

## Verification

- Source/content preflight: passed.
- Adaptive-profile smoke tests: passed.
- Original resume PDF signature and size: passed.
- SHA-256 source/destination match: passed.
- PDF info: one A4 page, unencrypted, 358,350 bytes.
- Rendered the original resume at 120 DPI and visually checked the page.
- Confirmed public PDF and DOCX resources remain present.
- Confirmed no private CV variants are in the package.
- The full React/Vite production build remains unverified while dependencies are not installed.

## SHA-256

`99950a214cfa96e400802d3d2266250322ea7ded6c9cfe3ead046259913fc383`


## Superseding update — 2026-11-09 (PDF-only personal documents)

The current portfolio keeps only two personal-document downloads: the exact original resume PDF and the redesigned public-safe CV PDF. The editable DOCX file was removed from `public/`, its configuration property and UI links were deleted, and the header, hero, contact, no-JavaScript, and React error fallbacks now expose PDF links only. The release preflight explicitly fails if a Word/ODT document appears in `public/` or if a DOCX route is configured. See `PDF-ONLY-DOCUMENTS-QA-2026-11-09.md` for current verification.
