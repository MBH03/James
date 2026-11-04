# QA checklist (run before every push)

1. **Build**: run the build script. It must finish without error and a second run must produce no diff.
2. **Facts**: every price, policy, time, license, fee and credential on the site matches the owner's confirmed answers. Search the whole repo for superseded wording (old prices, "lunch provided", removed destinations, old counts like "seven lakes").
3. **Removed items**: search the repo for names of anything removed (pages, destinations). Zero hits.
4. **Links**: every local `href` and `src` resolves to a file. No `localhost` or staging domains. No references to the old domain after a cutover.
5. **Structured data**: every JSON-LD block parses as JSON; FAQ text matches the visible FAQ.
6. **Visual check** (Playwright with local Chromium, `executablePath: '/opt/pw-browsers/chromium'`):
   - 390px wide phone and 1280px desktop screenshots of home, one destination page, rates page.
   - Set `html{scroll-behavior:auto}` and force `.reveal` visible before capturing.
   - Look for overflow, clipped tables, unreadable contrast, missing images, cramped nav.
   - Offline screenshots use fallback fonts; do not judge typography from them.
7. **Images**: dimensions declared, file sizes reasonable, nothing upscaled beyond about 2x, weak sources flagged to the owner.
8. **Git**: clean status, clear commit message, risky changes on a branch. Pull before pushing; if the remote has new commits, reset or rebase onto it and do not overwrite someone else's work.
9. **Report**: say what was verified and what was not (live site, Search Console, rankings, real-device rendering).
