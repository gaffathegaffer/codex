# Review findings and recommended follow-up activities

## Fix a typo

- **Issue:** `codex-cli/src/text-buffer.ts` starts with the lint directive `/* eslint‑disable no-bitwise */`, but the hyphen is a non-breaking hyphen character, so ESLint will not recognize the disable comment. This is effectively a typo in the directive.
- **Recommended activity:** Replace the non-breaking hyphen with a regular hyphen (`eslint-disable`) so the directive works as intended and the file is linted consistently.

## Fix a bug

- **Issue:** `detectInstallerByPath` only checks for `npm`, `pnpm`, and `bun` even though update rendering supports additional managers (e.g., `yarn`, `deno`). Users who installed globally with other supported managers will never be auto-detected, leading to incorrect or missing update instructions.
- **Recommended activity:** Extend the supported manager list in `detectInstallerByPath` (and related bin-dir lookups) to cover all managers supported by `renderUpdateCommand`, so the CLI suggests the correct update command for yarn- or deno-based installs.

## Resolve a documentation/comment deviation

- **Issue:** The update prompt generated in `renderUpdateMessage` reads “To update, run <command> to update,” repeating the phrase and producing awkward, low-quality output.
- **Recommended activity:** Reword the message to a single, clear instruction (e.g., “Update with <command>.”) to align the user-facing text with standard CLI copy guidelines and avoid redundant phrasing.

## Improve a test

- **Issue:** `codex-cli/tests/dummy.test.ts` asserts `1 === 1`, providing no coverage of application behavior.
- **Recommended activity:** Replace this placeholder with a meaningful test (or remove it) that exercises real logic—e.g., a small utility function—so the suite offers actionable regression protection.
