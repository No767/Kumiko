# 🛠️ Kumiko v0.10.2 🛠️

This release fixes issues with the marketplace module and others.

For the full list of changes, please see them here: [`v0.10.1...v0.10.2`](https://github.com/No767/Kumiko/compare/v0.10.1...v0.10.2)

## :boom: Breaking Changes :boom:

- There are none :smile:

## ✨ TD;LR

- Fixed the owner-issue relationship bug

## 🛠️ Changes

- Fixed the owner-issue relationship bug (this was an issue with the marketplace where if someone made a job output and others bought it, it would throw errors)
- Applied foreign key constraints for item ids
- Changed the user_inv from an 1-n relationship to m-m relationship
- Fixed the prefix duplicates bug (before this, admins could set duplicate prefixes and it would work)
- Updated `Requirements/prod.txt` requirements

## ✨ Additions

- None

## ➖ Removals

- Removed `toml` (not from stdlib)

# ⬆️ Dependabot Updates

- (Security) Update certifi to 2023.07.22 (fixes CVE-2023-37920)