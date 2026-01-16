## Kumiko [0.12.0-beta](https://github.com/No767/Kumiko/tree/0.12.0-beta) - 2026-01-16

### Bug fixes

- Fix and upgrade meta module (#559)
- More additional fixes (#584)

### Features

- Add [Taskfile](https://taskfile.dev/) (#554)
- Rewrite redirects module (#555)
- Implement better help command (#561)
- Entirely rewrite blacklist system (#562)
- Implement Prometheus exporter (#563)
- Add new hardened systemd config based from Catherine-Chan; rewrite code to account for hardened systemd config (#594)

### Removals and backward incompatible breaking changes

- Drop Python 3.9 support (#560)
- Rewrite custom prefixes module (no user changes) (#565)
- Modernize and restructure codebase
      Removes Task in favor of mise (#582)
- Drop pre-commits in favor of CI-based checks (#594)

### Miscellaneous internal changes

- Add Opengraph metadata support and preview cards for documentation (#594-1)
- Update `docker-compose` PostgreSQL versions to 18 (#594-2)
- Consolidate utilities and align towards stricter ruff rules (#594-3)
- Use v0 of `no767/get-releasenote` for release extractions (#557)
- Use custom `no767/get-releasenote` action instead of `changelog.md` for obtaining release notes (#573)
- Remove `wait-for` and improve Docker startup and configurations (#576)
- Rewrite documentation using newer Sphinx extensions and features (#594)
