# Motion Skill Workflow

A **cross-tool Agent Skill installer** with a curated motion-design workflow, a read-only [audit map of 15 repositories](references/catalog.md), and optional Markdown-only skills from LottieFiles and GSAP. It does not install video libraries, run upstream scripts, download models, upload media, or grant third-party instructions authority.

## Install on macOS or Linux

Requires Git and Python 3.9+. Review `install.py` before executing it.

```sh
git clone https://github.com/404kidwiz/motion-skill-workflow.git "$HOME/.local/share/motion-skill-workflow"
python3 "$HOME/.local/share/motion-skill-workflow/install.py" --dry-run
python3 "$HOME/.local/share/motion-skill-workflow/install.py"
python3 "$HOME/.local/share/motion-skill-workflow/install.py" --verify
```

Default installs **one original routing skill**, `motion-skill-workflow`, across the global skill directories for Hermes, Codex, Claude Code, Cursor, Gemini CLI/Antigravity, OpenCode, OpenClaude, Grok, ZCode and shared Agent Skills. It creates missing directories and links this checkout. It does not replace a different skill at the same name. Restart your CLI/IDE and verify that it discovers the skill; a file-path check is not runtime acceptance.

To add the vetted **official MIT Markdown skills** (one LottieFiles, eight GSAP), after reviewing [third-party provenance](THIRD_PARTY.md):

```sh
python3 "$HOME/.local/share/motion-skill-workflow/install.py" --official --dry-run
python3 "$HOME/.local/share/motion-skill-workflow/install.py" --official
python3 "$HOME/.local/share/motion-skill-workflow/install.py" --official --verify
```

Existing skill-name conflicts are **left untouched** and cause a nonzero exit; other unconflicted targets can still install. For a smaller selection, use `--skills motion-skill-workflow,lottiefiles-motion-design` or `--skills motion-skill-workflow,gsap-react` with any of the skill names in `install.py`. For one client, add `--tools codex` (or another listed tool). Official skills are pinned copies of Markdown and references, not installation of `gsap`, `@gsap/react`, Lottie, Remotion or rendering dependencies. Their instructions may describe external commands; choose whether to run anything in your own project.

## Windows PowerShell

Requires Git and Python 3.9+ (`py -3`). Auto mode uses managed copies rather than symlinks; rerun after pulling updates.

```powershell
git clone https://github.com/404kidwiz/motion-skill-workflow.git "$env:LOCALAPPDATA\motion-skill-workflow"
py -3 "$env:LOCALAPPDATA\motion-skill-workflow\install.py" --dry-run
py -3 "$env:LOCALAPPDATA\motion-skill-workflow\install.py"
py -3 "$env:LOCALAPPDATA\motion-skill-workflow\install.py" --verify
```

The installer checks files at conventional paths; tool support, skill-loading and account sign-in vary by installed version. It never writes MCP configuration or credentials. `--home PATH` targets a disposable home for testing.

## Refine and update

Edit `SKILL.md` for your workflow and `references/catalog.md` for the audited routing list. On a different machine:

```sh
git -C "$HOME/.local/share/motion-skill-workflow" pull --ff-only
python3 "$HOME/.local/share/motion-skill-workflow/install.py"
python3 "$HOME/.local/share/motion-skill-workflow/install.py" --verify
```

Add `--official` when updating managed official-skill copies. Symlink installs reflect source edits immediately. Conflicting or locally modified managed copies are never overwritten. Run `python3 -m unittest discover -s tests -v` before publishing changes. To refresh bundled upstream content, verify a pinned commit, review every new file and license, update `THIRD_PARTY.md`, then rerun tests; do not automate unreviewed upstream updates.

## Limits

The 15 upstream repositories were inspected statically, not run end-to-end. Several require Node, FFmpeg, Chromium, Remotion, paid media services, asset rights or licenses. Remotion's monorepo has custom licensing, and its separate skills repo had no license at audit time, so both remain **links only**. This installer does not enable those services or prove a finished video render. See [third-party notices](THIRD_PARTY.md) and the [MIT license for original code](LICENSE).
