# claude-skills

A collection of [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) — each is a directory containing a `SKILL.md` (plus any supporting scripts) that Claude Code can discover and invoke.

## Available skills

| Skill (`name:` in SKILL.md) | Path to the `SKILL.md` directory | What it does |
| --- | --- | --- |
| `github-migration` | `github-migration/` | Migrate repos between GitHub orgs/instances (GHES, GHEC.com, GHEC EMU/US) via `gh gei`. |
| `led-gif-generator` | `led_gif_tool_with_examples/skill/` | Generate LED blink/fade pattern GIFs from natural-language descriptions. |

Note the second one is nested a level deeper (`skill/` subfolder) — always link the directory that directly *contains* `SKILL.md`, not its parent.

## Installing a skill

Claude Code loads skills from a `skills/` folder inside a `.claude/` directory, either:

- **Personal, all projects**: `~/.claude/skills/`
- **This project only**: `<project>/.claude/skills/`

Clone this repo somewhere, then symlink (recommended, so `git pull` here keeps skills up to date) or copy the relevant skill directory in:

```sh
git clone https://github.com/ggunde/claude-skills.git ~/repos/claude-skills

# personal, available in every project
ln -s ~/repos/claude-skills/github-migration ~/.claude/skills/github-migration
ln -s ~/repos/claude-skills/led_gif_tool_with_examples/skill ~/.claude/skills/led-gif-generator

# or, project-scoped instead
mkdir -p .claude/skills
ln -s ~/repos/claude-skills/github-migration .claude/skills/github-migration
```

To copy instead of symlink (won't pick up future updates from this repo):

```sh
cp -r ~/repos/claude-skills/github-migration ~/.claude/skills/github-migration
cp -r ~/repos/claude-skills/led_gif_tool_with_examples/skill ~/.claude/skills/led-gif-generator
```

The destination folder name under `skills/` doesn't have to match the `name:` field, but keeping them the same avoids confusion.

After linking, restart Claude Code (or start a new session) so it picks up the new skill; it will be listed as available and Claude will invoke it automatically when a request matches its `description:`.
