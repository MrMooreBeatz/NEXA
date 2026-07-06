# Moore Awareness — So Brrr Streak App Brief

> This is the thinking document, not a technical spec. The app grows from the brand — not the other way around.
> Name: **So Brrr Streak App**
> Purpose: Daily tools for personal growth and awareness maintenance.

---

## APP PURPOSE

The So Brrr Streak App turns daily awareness into a practiced habit.
For the person in recovery or building self-awareness who needs a tool that meets them where they are — not a clinical app, not a generic meditation app — this is a grounded, culturally rooted daily companion. Mind, body, energy. One streak at a time.

> For [person in recovery / someone building self-awareness] who is [struggling with X], So Brrr Streak is an app that [delivers daily awareness tools] unlike [generic wellness apps], we [bring lived experience + MSAP framework + a community-rooted approach without requiring insurance or surrender].

## APP MISSION

Same as the brand — access awareness daily. Build transformation over time.

## NEXA (Personal Layer — Separate from App)

**Nexa** is Steven Moore's personal AI assistant.
- Not a customer-facing product.
- Functions as the internal operating layer for:
  - Brand thinking and refinement
  - Content development and strategic execution
  - Recovery program refinement and MSAP framework design
  - Business operations and financial discipline
  - Idea capture and prioritization
- Built and customized on this assistant platform (Hermes), trained to Steven's voice, brand, and mission.
- Think of it as the executive brain for Moore Awareness — not another revenue stream.

---

## TIER 1 — FREE

Goal: Reduce friction. Recovery apps are most valuable when people can start immediately.

### Free Features

| Feature | Description |
|---------|-------------|
| Streak tracking | Visual streak counter, milestone badges |
| Awareness Points | Gamified participation currency |
| Avatar | Basic avatar creation/customization |
| Basic journal | Prompted journal entries, limited history |
| Box breathing | Guided box-breathing exercise |
| Basic goals | Limited goal-setting (3 active goals) |
| Community access | Read-only or limited community feed |

**Design principle:** Everything in Free is useful enough to build the habit. Nothing in Free is essential enough to make them leave.

---

## TIER 2 — MOORE+ ($4.99–$9.99/month)

Goal: Recurring revenue through a companion that deepens over time.

### Premium Features

| Feature | Description |
|---------|-------------|
| AI Awareness Companion | Conversational AI guide (not generic chatbot) |
| Personalized pattern analysis | Trends across journal, streaks, mood |
| Advanced insights | Weekly/monthly reflection summaries |
| Unlimited journal history | No retention limits |
| Advanced statistics | Streak analytics, goal completion rates, awareness trends |
| Custom avatars | Expanded avatar customization, exclusive items |
| Seasonal events | Themed challenges, community events tied to seasons/cultural moments |
| Additional breathing exercises | Beyond box breathing |
| Meditation library | Guided meditations aligned with MSAP pillars |
| Exclusive challenges | Curated challenges for Moore+ members |
| Ad-free | No ads in app |

**The key message:** People aren't paying for "AI."
They're paying for a companion that becomes more useful over time.

---

## TIER 3 — PHYSICAL PRODUCTS (BRAND MERCH)

Goal: Physical brand reinforcement + additional revenue. App supports merch; merch reinforces app.

- **So Brrr Water** — aluminum eco-friendly bottles and practices
- **Apparel** — hoodies, t-shirts
- **Recovery Journals** — print journals aligned with app prompts
- **Reusable Water Bottles** — branded hydration
- **Challenge Coins** — milestone collectibles
- **Wristbands** — wearable reminders
- **Crypto Currency** *(note: requires feasibility review — tokenomics, regulatory, audience fit)*
- Other physical products that reinforce the brand

**Integration rule:** Every physical product should have an in-app connection (scan code, digital companion, exclusive content, challenge entry).

---

## TIER 4 — ORGANIZATIONS (B2B)

Goal: Long-term revenue through organizational licensing. Groups pay significantly more than individuals because they're supporting populations, not single users.

### Who Pays

| Organization Type | Why They Pay | Price Range (starting point) |
|-------------------|--------------|------------------------------|
| Treatment centers | Client engagement + outcome tracking | $500–$5,000/mo |
| Recovery coaches | Client management + branded tools | $99–$499/mo |
| Employee wellness programs | Population mental health + prevention | $2,000–$20,000/yr |
| Colleges/universities | Student wellness + retention | $3,000–$25,000/yr |
| Veterans organizations | Peer support + structured recovery tools | $500–$10,000/yr |
| Nonprofits | Program delivery + impact measurement | $500–$15,000/yr |

### What They Get

| Feature | Description |
|---------|-------------|
| Admin dashboard | Overview of participant engagement, streaks, journaling activity, mood trends |
| Group management | Create cohorts, assign challenges, track group progress |
| Privacy controls | User consent + data protection policies (HIPAA-aware where required) |
| Custom branding | Org-co-branded app experience where appropriate |
| Reporting/analytics | Impact metrics, completion rates, trend reports — useful for grants/funders |
| Bulk user provisioning | License seats, onboarding at scale |
| Integration hooks | Connection to existing EHR, wellness platforms, or org systems |

### Privacy & Consent Model

- **User consent is foundational.** Individual users opt in to sharing any data with an organization.
- Organizations see **aggregate data** by default (anonymized group trends).
- **Named/individual data** only visible to orgs with explicit user authorization, scoped to relevant staff.
- Compliance-aware design: HIPAA considerations for treatment centers, FERPA considerations for education, etc.
- Transparency: users know exactly what's shared, with whom, and for what purpose.

### Why This Works Long-Term

1. **Price-per-seat is much higher** than individual subscriptions
2. **Organizations have budget lines** wellness, treatment, prevention that individuals don't
3. **Stickiness:** once an org is onboarded, switching costs are high
4. **Flywheel:** org use drives individual acquisition (participants download the app to engage with their program)
5. **Impact storytelling:** org-level data becomes your most powerful marketing material

### Launch Timing

- **Phase 3-4** (Month 3-6): Define org-tier feature set and privacy architecture
- **Phase 4** (Month 4-6): Pilot with 1-2 organizations (likely treatment center or recovery coach first)
- **Phase 5** (Month 6+): Scale organizational sales as a dedicated revenue stream

*Note: Privacy architecture and compliance posture must be designed before first org pilot. Do not rush this tier.*

---

## REVENUE MODEL

| Stream | Type | Timing |
|--------|------|--------|
| Free tier | Acquisition / funnel | Launch |
| Moore+ subscriptions | Recurring MRR | Month 1 after free launch |
| Physical products | Transactional | Parallel with app launch |
| So Brrr Water | Transactional | Active now or near-term |

**Design principle:** The app supports the merchandise. The merchandise reinforces the app. Cross-pollination is the flywheel.

---

## USER PERSONA (App)

**Primary:** Person in early-to-mid recovery or active self-awareness work
- Needs a tool that feels like a companion, not a clinical system
- Has tried therapy, meditation apps, self-help books
- Culturally rooted but underserved by mainstream wellness platforms
- Holds phone daily — tool needs to meet them there consistently

**Secondary:** Someone spiritually curious, seeking structured growth without dogma
- Wants tools that integrate mind, body, energy
- Open to metaphysical practice as long as it's framed accessibly

---

## TECH STACK / INFRASTRUCTURE (Architecture)

**Domains:**
- mooreawareness.com — marketing/mission
- app.mooreawareness.com — app production
- admin.mooreawareness.com — org/admin dashboard
- api.mooreawareness.com — backend API
- sobrrrwater.mooreawareness.com — storefront (or separate domain later)

**Rationale:** modular subdomain architecture keeps authority centralized, enables future module spinouts without restructuring, presents a unified ecosystem to users and investors alike.

**Current status:** architecture decided; implementation follows MVP selection.

---

## MVP FEATURE RANKING

Ranked by user need:

### Must Have (V1)
1. Streak tracking + Awareness Points
2. Journal + Box breathing
3. Avatar system (basic)
4. Basic goals
5. Community access (read-only feed)

### Should Have (Moore+ Launch)
1. AI Awareness Companion
2. Advanced insights/statistics
3. Unlimited journal history
4. Meditation library
5. Custom avatars/exclusive items

### Nice to Have (Later)
1. Seasonal events
2. Advanced pattern analysis
3. Physical product integrations
4. Crypto utility

---

*This brief evolves as the brand, audience, and MSAP framework clarify. Revisit every 4-6 weeks.*
