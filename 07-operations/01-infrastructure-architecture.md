# Moore Awareness — Infrastructure & Architecture

> Operational decisions that affect how the brand is built, hosted, and scaled.

---

## BRAND ARCHITECTURE

**Umbrella:** Moore Awareness LLC  
**Primary domain:** mooreawareness.com

### Subdomain Map

| Layer | Address | Purpose |
|-------|---------|---------|
| Marketing / mission | mooreawareness.com | Brand home, story, content funnel |
| So Brrr Streak App | app.mooreawareness.com | Consumer app access |
| Admin / org dashboard | admin.mooreawareness.com | Org management, reports, Tier 4 features |
| API backend | api.mooreawareness.com | Data layer, integrations, auth |
| So Brrr Water store | sobrrrwater.mooreawareness.com | Physical product shop |

### Principles

- Single domain authority — all SEO and brand equity centralizes at mooreawareness.com
- Modular on subdomains — later we can spin off MSAP or So Brrr Water into standalone domains without rebuilding
- Investor clarity — one ecosystem, not scattered projects
- Privacy separation — app/api/admin on distinct layers for security posture

---

## HOSTING / DEPLOYMENT (To Be Decided)

Options:
- Vercel / Netlify (frontends)
- Fly / Render / DigitalOcean (API + backend)
- Supabase / Firebase (BaaS — auth, DB, storage)
- WordPress (marketing site, if preferred for content flexibility)

**Decision gate:** align with MVP tech path before spending.

---

## DATA & PRIVACY

- User consent model: opt-in for any org data sharing
- Aggregate by default for organizational dashboards
- Individual-level data only with explicit authorization
- HIPAA-aware for treatment center pilots
- FERPA-conscious for education pilots
- Regular privacy audits as org tier scales

---

## INTEGRATION PRINCIPLES

- Physical products should have digital companion hooks
- App should feed content to website (blogs from journals, etc.)
- Podcast and storytelling assets should feed the content ecosystem
- No siloed tools without an integration path

---

*Infrastructure evolves with the product. Update as decisions harden.*
