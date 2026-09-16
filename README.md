# The Operators

The public website for The Operators, agent and manager to 100x AI talent.

Durkin and a team of humans and AIs support Career, Network, EA, Health, Finances, and Travel.

## Build

Run `python3 build.py` and `python3 check.py`. GitHub Actions publishes only the generated `dist/` directory to Pages. The build uses an explicit asset allowlist and contains no roster, profiles, collection pages, or private archive data.

The entry URL https://durkdaddy.github.io/the-operators/ currently redirects to https://massaicoalition.com/the-operators/ because the account's root Pages site uses that domain. For the eventual Operators custom-domain cutover, set `BASE_PATH='' SITE_ORIGIN='https://www.theoperators.co'` for both build and validation. Change only necessary web DNS records; preserve all email records.

All calls to action lead to `/learn-more/`. Its only main text is “Durkin is currently building other companies right now”. There are no public contact invitations or email links.

Profile source and history are retained separately in a private repository and excluded from this public repository. Removed URLs return 404 and are absent from the sitemap. Search engines may retain previously indexed pages until recrawling.

The original Operators logo and Durkin's yellow-background portrait are supplied assets. The vibrant square Boston graffiti mural was generated for this project. The Chief of Staff preview is the current design source of truth. Font licenses are in `assets/`.
