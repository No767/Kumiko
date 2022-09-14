# 🛠️ Rin V2.2.6 (LTS) 🛠️

This update fixes some issues that were present in v2.2.5
## 🛠️ Changes
- Bump version to `v2.2.6`
- Condense Docker build workflows (from 4 to 2)
- Use `github.actor` instead of `github.repository_owner` for Docker GHCR workflow 
- Update docs (getting started guide)
- Update `docker-compose-example.yml` file
- Display Pycord version when using `/botinfo` command
- Update Alpine and Debian Dockerfile to Python 3.10.7

## ✨ Additions

## ➖ Removals

- Remove `global-error-handling.py` cog (caused 403 errors)
## ⬆️ Dependency Updates

- \[Actions](deps)\: Bump actions/checkout from 2 to 3 (@dependabot)
- \[Actions](deps)\: Bump actions/cache from 2 to 3 (@dependabot)
- \[pip](deps)\: Bump py-cord from 2.1.1 to 2.1.2 (@dependabot)
- \[pip](deps)\: Bump py-cord from 2.1.2 to 2.1.3 (@dependabot)
- \[pip](deps)\: Bump numpy from 1.23.2 to 1.23.3 (@dependabot)
- \[pip](deps)\: Bump pysimdjson from 5.0.1 to 5.0.2 (@dependabot)
