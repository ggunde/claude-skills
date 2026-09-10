---
name: github-migration
description: migrate one or more GitHub repos between orgs/instances (GHES, GHEC.com, GHEC EMU/US) using the gh-gei CLI extension. use when user asks to migrate, move, or import repos between GitHub orgs or GitHub instances (e.g. "migrate these repos from our GHES server to GHEC", "move this org to GHEC EMU/US", "import repos into the new GitHub instance").
---

# GitHub Repo Migration

Wraps `gh gei migrate-repo` (from the [GitHub Enterprise Importer](https://docs.github.com/en/migrations/using-github-enterprise-importer)) to migrate repositories between GitHub orgs, including across instances (GHES, GHEC.com, GHEC EMU/US).

## Prerequisites

Check these before running anything:

1. GitHub CLI with the `gh-gei` extension:
   ```
   gh extension list | grep gh-gei || gh extension install github/gh-gei
   ```
2. Two environment variables set in the shell that will run the script:
   - `GH_SOURCE_PAT` — PAT with access to the source org
   - `GH_PAT` — PAT with access to the target org
   - If either is missing, ask the user to export it (don't ask them to paste the token value into chat).

### Required token scopes

Both tokens must be **classic** PATs (fine-grained tokens aren't supported by gh-gei). If SAML SSO is enabled on the org, each token needs to be SSO-authorized for it.

- `GH_SOURCE_PAT` (source org):
  - Org **owner**: `admin:org`, `repo`
  - Org **migrator role** (if not an owner): `admin:org`, `repo`
- `GH_PAT` (target org):
  - Org **owner**: `repo`, `admin:org`, `workflow`
  - Org **migrator role** (if not an owner): `repo`, `read:org`, `workflow`
  - Note: only an org owner on the target can actually *receive* migrated repos, even if a migrator token runs the command.

If either org has an IP allow list, it must permit GitHub Enterprise Importer's service traffic or the migration will fail to authenticate.

### Additional requirement for GHES sources

If the source is GHES **3.7 or earlier**, gh-gei stages the migration through a blob storage account you provide — pass `--azure-storage-connection-string` (or set `AZURE_STORAGE_CONNECTION_STRING` in the environment; AWS S3 credentials work too, see gh-gei docs). This script doesn't add its own flag for it, but since it just shells out to `gh gei`, setting `AZURE_STORAGE_CONNECTION_STRING` in the environment before running is picked up automatically.

If the source is GHES **3.8+**, you can instead avoid provisioning your own storage entirely by passing `--use-github-storage` (not currently exposed by `scripts/migration.py` — mention this to the user if they hit blob-storage errors on a modern GHES source, and add the flag to the script's `cmd` list on request).

## Gather migration parameters

Ask the user (or infer from context) for:

- **Source org** and **target org** (org names, not full URLs)
- **Source instance type**:
  - GHES (on-prem) → need its API URL, e.g. `https://git.example.com/api/v3`
  - GHEC.com → no URL needed
- **Target instance type**:
  - GHEC.com → no URL needed
  - GHEC EMU/US (a dedicated `*.ghe.com` host) → need its API URL, e.g. `https://api.<host>.ghe.com`
- **Which repos** to migrate — a list of names, or a org-wide migration. If a repo should be renamed during the move, note it as `source-name:target-name`.

Never guess org names, hostnames, or repo lists — these are destructive/irreversible-ish operations against real GitHub orgs, so get them explicitly from the user or from a file they point you to.

## Running the migration

1. Do a dry run first and show the user the exact `gh gei` commands before executing for real:
   ```
   python3 scripts/migration.py \
     --source-org SOURCE_ORG --target-org TARGET_ORG \
     [--source-api-url SOURCE_API_URL] \
     [--target-api-url TARGET_API_URL] \
     --repo repo1 --repo repo2 ... \
     --dry-run
   ```
   (or `--repos-file path/to/repos.txt`, one repo per line, `#` for comments)
2. Confirm with the user before running for real — this touches external systems and can be slow/costly to re-run.
3. Re-run the same command without `--dry-run`.
4. Report the summary printed at the end, including any failed repos, and the script's exit code (non-zero if anything failed).

## Notes

- Omit `--source-api-url` for a GHEC.com source; omit `--target-api-url` for a GHEC.com target. Only set the one(s) that apply — see the type mapping above.
- Repos are migrated one at a time, sequentially; a failure on one repo doesn't stop the rest.
- This does not run inside a venv — it only uses the Python standard library (`argparse`, `subprocess`, `os`, `sys`), so the system `python3` is fine.
