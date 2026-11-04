# SEO playbook for small local-service sites

## Page types (generate from data)
- Home: the main promise, then everything else.
- Hub: all services or destinations, with a comparison table and FAQ.
- One page per destination or service: hero, experience, why choose it, "good to know", facts and tags, FAQ, other destinations, booking.
- One page per audience or nearby place (a town, a nearby attraction): who it is for, which options suit them, FAQ.
- Rates and policies page and a full FAQ page.
- Photos page.

## On every page
- `<title>`: service + place + brand, about 60 characters or fewer.
- Meta description: one sentence with the offer and phone number.
- One H1 matching the search wording ("Panguitch Lake Fishing Guide" style).
- Canonical URL on the final domain, `og:` tags with a real image.
- Breadcrumbs; internal links with descriptive text ("Panguitch Lake fishing guide", not "details").
- Images: descriptive alt text, width and height set, lazy loading, sized for display (a 1600px hero, 800px cards).

## Structured data (valid JSON, no unverified numbers)
- LocalBusiness: name, url, telephone, email, address (city and state), areaServed, logo, sameAs.
- Service per destination or service, with provider.
- FAQPage on pages with real Q&A, written to match the visible text.
- BreadcrumbList.

## Site files
- `sitemap.xml` listing every page with lastmod; `robots.txt` pointing to it and allowing normal and AI crawlers; `llms.txt` summarising the business and pages.
- Generate all three from the build script so they never drift.

## Launch and domain
- Put a domain change on a branch, set DNS first (four GitHub Pages A records and a `www` CNAME, DNS only), set the custom domain and HTTPS in repo Settings, confirm the domain loads, then merge.
- Register Search Console, verify, submit the sitemap, and inspect key pages. A new domain takes days to weeks to index; a young site will not outrank established local competitors immediately.
- Booking links that carry a query string (`/?lake=...`) show up in Search Console as "Alternate page with proper canonical tag". That is expected and harmless.

## Local SEO guidance that is safe
- Create and fill out a Google Business Profile with the real business name, correct categories, service areas, photos, hours and real services.
- Ask happy customers for reviews. Do not script what they should say, do not buy reviews.
- Do not put keywords in the business name.
- Get links from local tourism, chamber and directory sites that are real.

## Treat outside audits as claims
- Check each fact (elevation, regulations, designations) against an authoritative source before putting it on the site.
- Do not add "we pick up from town X" if the business does not.
- Do not promise ranking timelines.
- Compare the business's prices to local competitors and say so, without copying their terms.
