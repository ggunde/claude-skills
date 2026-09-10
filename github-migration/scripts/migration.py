#!/usr/bin/env python3
"""Migrate repositories between GitHub instances using the GitHub Enterprise
Importer (`gh gei`) CLI extension.

Supports any source/target combination gh-gei supports:
  - GHES -> GHEC.com                 (--source-api-url only)
  - GHES -> GHEC EMU/US              (--source-api-url and --target-api-url)
  - GHEC.com -> GHEC EMU/US          (--target-api-url only)
  - GHEC.com -> GHEC.com             (neither flag)
"""

import argparse
import os
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Migrate GitHub repositories between orgs/instances using gh-gei.",
    )
    parser.add_argument("--source-org", required=True, help="Org name on the source instance")
    parser.add_argument("--target-org", required=True, help="Org name on the target instance")
    parser.add_argument(
        "--source-api-url",
        help="API URL of the source instance. Only needed when the source is GHES "
             "(e.g. https://github.example.com/api/v3). Omit for a GHEC.com source.",
    )
    parser.add_argument(
        "--target-api-url",
        help="API URL of the target instance. Only needed when the target is not "
             "GHEC.com (e.g. https://api.<host>.ghe.com for a GHEC EMU/US target). "
             "Omit for a GHEC.com target.",
    )
    parser.add_argument(
        "--repo", dest="repos", action="append", default=[],
        help="Repository to migrate; pass multiple times, or use --repos-file. "
             "Use 'source-name:target-name' to rename during migration.",
    )
    parser.add_argument(
        "--repos-file",
        help="Path to a file with one repo name per line ('#' starts a comment).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the gh gei commands that would run, without executing them.",
    )
    return parser.parse_args()


def load_repos(args):
    repos = list(args.repos)

    if args.repos_file:
        with open(args.repos_file) as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    repos.append(line)

    if not repos:
        raise SystemExit("No repositories specified; use --repo or --repos-file")

    return repos


def migrate_repo(args, repo):
    if ":" in repo:
        source_repo, target_repo = repo.split(":", 1)
    else:
        source_repo = target_repo = repo

    cmd = [
        "gh", "gei", "migrate-repo",

        "--github-source-org", args.source_org,
        "--source-repo", source_repo,

        "--github-target-org", args.target_org,
        "--target-repo", target_repo,
    ]

    if args.source_api_url:
        cmd += ["--ghes-api-url", args.source_api_url]

    if args.target_api_url:
        cmd += ["--target-api-url", args.target_api_url]

    print(f"Migrating {args.source_org}/{source_repo}")
    print(f"         -> {args.target_org}/{target_repo}")

    if args.dry_run:
        print("  [dry run] " + " ".join(cmd))
        return True

    result = subprocess.run(cmd)

    return result.returncode == 0


def main():
    args = parse_args()

    if not os.environ.get("GH_SOURCE_PAT"):
        raise RuntimeError("GH_SOURCE_PAT is not set")

    if not os.environ.get("GH_PAT"):
        raise RuntimeError("GH_PAT is not set")

    repos = load_repos(args)
    failed = []

    for repo in repos:
        if not migrate_repo(args, repo):
            failed.append(repo)

    print("\n=== Migration Summary ===")

    if failed:
        print("FAILED:")
        for repo in failed:
            print(f"  {repo}")
        sys.exit(1)
    else:
        print("All repositories migrated successfully.")


if __name__ == "__main__":
    main()
