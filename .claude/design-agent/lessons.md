# Lessons from the Henrie Outfitters build

- **Patch files can be cumulative.** A second patch contained the first. Apply it on the original base in a temporary worktree, diff against current, and apply only the delta; keep intentional changes made since.
- **Pasted copy conflicted with the owner's earlier answers** (price per person vs per boat, lunch provided vs bring your own, a different list of lakes). Ask a short multiple-choice question and apply the answer everywhere.
- **Do not invent specifics.** Prices, a "4.9 on Google" bar, license badges and drive times appeared in outside suggestions and were all left out until confirmed.
- **Mock-ups from other tools are inspiration, not content.** A React mock-up looked more generic than the real site. Take functional ideas (phone in header, rates block, park-to-lake table) and keep the real brand.
- **"Soft modern" was a styling layer, not a redesign.** Rounded corners, warm lines, soft shadows, pill tags, photo-topped cards and more spacing changed the feel without touching content.
- **Real photos mattered most.** Low-resolution lake photos (under 700px wide) stayed soft even after enlarging; use them small.
- **Removing a destination touches everything**: page, nav, cards, forms, sitemap, llms.txt, structured data, counts ("seven" to "six"), cross-links and FAQ text. Rebuild and grep.
- **Generated-page sites:** change the script, not the HTML. A site-wide wording change (trip length, lunch) needed one pass over the script and one over the hand-written home page.
- **Domain cutover on a branch** avoided a broken site while DNS and HTTPS were pending.
- **Search Console noise**: `?lake=` booking links appear as "Alternate page with proper canonical tag". Harmless.
- **Rankings for "town + service" are won by businesses with the town in their name and address, a Business Profile and reviews.** Page edits help, but a new domain needs time and links.
- **Another tool added** a Search Console verification file and an analytics tag directly to the repo. Pull before pushing, and make sure the build script keeps such tags.
- **Usage**: long sessions with many screenshots and big outputs burn usage fast. Start fresh sessions for new jobs and batch requests.
