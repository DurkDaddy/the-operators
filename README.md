# The Operators

A one-page public website for The Operators, the sports agency for tech talent.

Durkin and a team of humans and AIs support career, health, finances, EA responsibilities, network, and travel.

## Build

Run `python3 build.py` and `python3 check.py`. GitHub Actions publishes only the generated `dist/` directory to Pages. The build uses an explicit asset allowlist and contains no roster, profiles, collection pages, or private archive data.

The entry URL https://durkdaddy.github.io/the-operators/ currently redirects to https://massaicoalition.com/the-operators/ because the account's root Pages site uses that domain. For the eventual Operators custom-domain cutover, set `BASE_PATH='' SITE_ORIGIN='https://www.theoperators.co'` for both build and validation. Change only necessary web DNS records; preserve all email records.

Calls to action use an in-page link to Durkin or open an email addressed to contact@ryandurkin.com. The site stores no contact submissions and does not claim to have sent messages.

Profile source and history are retained separately in a private repository and excluded from this public repository. Removed URLs return 404 and are absent from the sitemap. Search engines may retain previously indexed pages until recrawling.

The original Operators logo and Durkin's yellow-background portrait are supplied assets. The graffiti mural was generated for this project. Font licenses are in `assets/`.
