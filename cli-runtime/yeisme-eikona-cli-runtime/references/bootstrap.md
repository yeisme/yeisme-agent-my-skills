# Installed-binary bootstrap catalog

An installed Eikona binary is self-describing. Do not search for, clone, or require access to the private `yeisme/eikona` repository to determine environment names, configuration files, Skills, or next actions.

Start every fresh Homebrew, Scoop, package, archive, or public Bash installation with:

```bash
eikona setup --agent
```

Follow `action.next`. The default setup is a no-write preview. Only after local-write authority is clear may the Agent run:

```bash
eikona setup --yes --agent
```

Setup creates only missing user configuration and installs Agent Skills from the public `https://github.com/yeisme/yeisme-dist` release that exactly matches the running released CLI. It must not fall back to latest, replace a package-manager-owned binary, accept credentials, edit shell startup files, change Codex/Claude MCP configuration, probe a provider, or generate an image. `SKILLS_RELEASE_NOT_MIRRORED` is a real public-distribution blocker; config-only recovery is:

```bash
eikona setup --yes --skip-skills --agent
```

Persistent local credentials use stdin and the user-owned auth store:

```bash
eikona auth set openai --protocol openai --api-key-stdin --agent
```

Environment discovery must remain metadata-only:

```bash
eikona config env --provider openai --agent
eikona config env --all --json
```

These commands may expose variable names, sensitivity, set/unset state, source, and precedence, but never values. Ordinary Agents must not call `eikona auth env` because it is an advanced raw secret-export surface.

After configuration, inspect adapted models and local channel defaults before any probe. Missing credentials are configuration status, not lack of adapter support:

```bash
eikona models list --source adapted --all --agent
eikona models list --source adapted --provider openai --all
eikona models default show --agent
eikona auth list --agent
eikona providers show openai --agent
```

Bare `eikona models list` reads `models.lock` (`--source manifest`). An empty manifest is not an empty adapter catalog; next action is `--source adapted`. `auth list` shows channel `default_model` values, not every adapted model.

A user may then authorize the explicit non-generating probe:

```bash
eikona doctor --channel openai --model openai/gpt-5.4-image-2 --probe --agent
```

Do not run `--smoke` or any generation command during bootstrap without explicit user approval for the provider/model and potential cost.

Installed-binary bootstrap is `eikona setup --agent` → review → `eikona setup --yes --agent` → `eikona auth set ... --api-key-stdin` → an explicitly authorized `doctor --probe`; do not search the private repository or infer state by parsing `~/.eikona`.
