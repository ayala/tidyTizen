# Public release review

Prepared for tidyTizen 0.1.38 on 24 October 2026.

## Source boundary

The public source contains the web app, public-font assets, browser checks, documentation, source/icon licences, and screenshots. It does not contain a TMDB API key, Samsung certificates, signing passwords, DUIDs, serial numbers, TV/network addresses, bridge tokens, root/recovery archives, compiled native payloads, proprietary fonts, or signed widgets.

`app/assets/local-secrets.js` is ignored. The public widget generator always substitutes `app/assets/local-secrets.example.js`, even when a real private file exists on the build machine.

The public repository was created with a new Git history from the reviewed working tree so machine-specific files and unrelated private development history were not published. CleanFrame attribution and its MIT copyright are retained.

## Validation

Before publication the source/resource checks, public-font Chromium suite, public-source audit, and unsigned public export were run. The browser suite mocks only the public Tizen boundary and does not prove physical-TV behavior. The resulting public widget is unsigned and requires each owner to create an identity and signing profile.

Third-party logos, fonts, photographs, and TMDB imagery retain the terms in [third-party notices](../THIRD_PARTY_NOTICES.md). Automated scanning is bounded and does not replace review of the staged files, Git history, GitHub Actions logs, and release assets.
