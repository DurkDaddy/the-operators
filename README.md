# The Operators

The public website for The Operators, agent and manager to 100x AI talent.

Durkin and a team of humans and AIs support Career, Network, EA, Health, Finances, and Travel.

## Build

Run `python3 build.py` and `python3 check.py`. Vercel configuration is ready to publish only the generated `dist/` directory. The build uses an explicit asset allowlist and contains no roster, profiles, collection pages, or private archive data.

The Operators is an independent personal project. It must have its own Vercel project and domain, with no hosting or navigation links to the Mass AI Coalition/Alliance website. Durkin's other personal projects follow the same separation rule.

Migration status: the standalone build is prepared; Vercel authentication is pending. Root paths are the default. Canonical URLs use `SITE_ORIGIN` when specified, otherwise Vercel's production domain, otherwise `https://www.theoperators.co`. After the independent Vercel deployment is verified, connect the public GitHub repository for automatic updates and disable this repository's legacy Pages deployment. Do not change the Coalition's root Pages settings.

The temporary Pages workflow still serves the existing preview with an explicit legacy base and origin. Remove that workflow after the Vercel deployment is verified. For the Operators custom-domain cutover, set `SITE_ORIGIN='https://www.theoperators.co'` and use the DNS records supplied by the actual Vercel project. Change only necessary web DNS records; preserve all email records.

All calls to action lead to `/learn-more/`. Its only main text is “Durkin is currently building the Mass AI Coalition right now and is putting 100% of his focus into that.”. There are no public contact invitations or email links.

Profile source and history are retained separately in a private repository and excluded from this public repository. Removed URLs return 404 and are absent from the sitemap. Search engines may retain previously indexed pages until recrawling.

The original Operators logo and Durkin's yellow-background portrait are supplied assets. The agent and tech talent graffiti artwork was generated for this project. This repository is the canonical source for subsequent direct edits. Font licenses are in `assets/`.
