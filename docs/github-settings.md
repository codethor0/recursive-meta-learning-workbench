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
