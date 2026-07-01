# One More Door

Fundraising site for the **Teen Living Center** (operated by Switchpoint), Davis County —
a 16-bed home for high-school students experiencing homelessness.

**Live:** https://onemoredoor.org

## Stack
Static HTML/CSS (no build step). Deployed to **Cloudflare Pages** (project `onemoredoor`).

## Structure
- `index.html` — the whole site
- `assets/` — photos, logos, generated sunburst mark

## Deploy
- **Auto (push to `main`):** `.github/workflows/deploy.yml` runs `wrangler pages deploy`.
  Requires one repo secret: `CLOUDFLARE_API_TOKEN` (scoped to *Cloudflare Pages → Edit*).
- **Manual:** `npx wrangler pages deploy . --project-name=onemoredoor`

## Donations
Buttons link to **Switchpoint's** own donation flow (`switchpoint.org/?campaign=775634`) and
Legacy Giving. Switchpoint is the 501(c)(3) merchant of record (EIN 76-0740457) — no funds
route through this site.
