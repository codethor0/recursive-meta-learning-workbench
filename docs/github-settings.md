# GitHub Repository Settings

Configure these via GitHub's web UI (Settings). They cannot be set from this repository.

## Branch Protection (main)

1. Settings > Branches > Add rule (or edit existing)
2. Branch name pattern: `main`
3. Enable:
   - Require a pull request before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging
   - Require at least one approval
   - Do not allow bypassing the above settings
4. Status checks to require: `lint-and-test`, `docker-build` (or the job names from ci.yml)
5. Disable: Allow force pushes
6. Disable: Allow deletions

## Security

- **Dependabot alerts**: Enable (Settings > Security > Dependabot alerts)
- **Secret scanning**: Enable if available for your plan
- **Code scanning**: Optional; add a workflow if desired

## General

- Ensure "Allow merge commits" or "Allow squash merging" is enabled as preferred
- Consider enabling "Automatically delete head branches" after merge

## Enabling the Wiki

1. Go to Settings > General
2. Under "Features", check **Wiki**
3. Save

## GitHub Wiki Setup

The repo contains wiki source material in `docs/wiki/`. To publish it:

**Option A: Create pages via the GitHub UI**

1. After enabling the Wiki, click "Wiki" in the repo sidebar
2. Create a new page for each file in `docs/wiki/`:
   - `Home.md` -> Home (or paste as the wiki front page)
   - `Getting-Started.md` -> Getting-Started
   - `Architecture.md` -> Architecture
   - `Contributing.md` -> Contributing
   - `Security-and-Scope.md` -> Security-and-Scope
3. Copy the contents of each file from `docs/wiki/` and paste into the corresponding wiki page
4. Save each page

**Option B: Clone the wiki repo and sync**

1. After enabling the Wiki, GitHub creates a `recursive-meta-learning-workbench.wiki` repo
2. Clone it: `git clone https://github.com/codethor0/recursive-meta-learning-workbench.wiki.git`
3. Copy the contents of `docs/wiki/*.md` into the wiki repo (e.g. `Home.md`, `Getting-Started.md`, etc.)
4. Commit and push: `git add . && git commit -m "Add wiki pages" && git push origin main`

Do not attempt to operate on the `.wiki.git` repo from within this project; these steps are manual guidance for the maintainer.
