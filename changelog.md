# ✨ Rin V2.2.1 (LTS) ✨

This update is a small patch update that updates some dependencies, and some other fixes

## Changes
- Use `pipenv requirements` instead of `pipenv lock` to export dependencies
- Bump Pycord to v2.0.1 to patch `CVE-2022-36024`
- Use Docker Meta Action instead of old prepare step
- Dev builds are marked as `edge` on Docker Hub, and `edge-hash` on GHCR
- Update contributing guidelines for a small change

## Additions


## Removals
- Old Prepare step in Docker Hub and GHCR build workflows 

## Dependency Updates
- \[pip](deps)\: Bump orjson from 3.7.11 to 3.7.12 (@dependabot)
- \[pip](deps)\: Bump rin-exceptions from 1.0.2 to 1.0.3 (@dependabot)
- \[pip](deps)\: Bump py-cord from 2.0.0 to 2.0.1  (@dependabot)