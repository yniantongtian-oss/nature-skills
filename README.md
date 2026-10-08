# Nature Skills

An extensible research workflow library for reading scientific papers, locating academic evidence, drafting manuscripts, checking citations, creating figures, and preparing presentations.

This repository contains reusable `SKILL.md` packages and their supporting scripts, references, and assets. It is intended for qualified human review of research materials; generated scientific claims and citations must be verified against primary sources.

## Source and attribution

This repository is based on the open research-skills project maintained by Yizhe Yuan and contributors: [original project](https://github.com/Yuan1z0825/nature-skills). Preserve existing authorship, licenses, and third-party asset notices when redistributing resources.

## Available modules

| Module | Purpose |
| --- | --- |
| [Academic Search](skills/nature-academic-search/) | Literature discovery and source lookup |
| [Citation](skills/nature-citation/) | Reference formatting and citation checks |
| [Data](skills/nature-data/) | Research data and analysis workflows |
| [Figure](skills/nature-figure/) | Scientific figure creation and inspection |
| [Paper to Slides](skills/nature-paper2ppt/) | Research presentation preparation |
| [Polishing](skills/nature-polishing/) | Academic language and clarity |
| [Reader](skills/nature-reader/) | Structured full-paper reading |
| [Response](skills/nature-response/) | Reviewer-response preparation |
| [Reviewer](skills/nature-reviewer/) | Peer-review-style analysis |
| [Writing](skills/nature-writing/) | Manuscript drafting and structure |

A module's exact behavior is defined by its own `SKILL.md` and supporting resources. Some modules require external applications or optional dependencies; consult their individual instructions before execution.

## Install

Clone this repository:

```bash
git clone https://github.com/yniantongtian-oss/nature-skills.git
cd nature-skills
```

To install a standalone module in a client that supports directory-based skills, copy the complete module directory along with the shared resources. Replace `$SKILL_DIR` with the supported directory for that client.

```bash
mkdir -p "$SKILL_DIR"
cp -R skills/_shared "$SKILL_DIR/"
cp -R skills/nature-reader "$SKILL_DIR/"
```

To install the complete collection:

```bash
mkdir -p "$SKILL_DIR"
cp -R skills/_shared "$SKILL_DIR/"
for module in skills/nature-*; do
  cp -R "$module" "$SKILL_DIR/"
done
```

Avoid copying a single `SKILL.md` in isolation: scripts, assets, and relative references can be required for normal operation. The `plugins/nature-skills/` directory is another distribution layout and is not an independent research implementation.

## Project structure

```text
skills/                  Main installable research modules
skills/_shared/          Shared resources
plugins/nature-skills/   Packaged distribution copy
scripts/                 Maintenance helpers
install.md               Historical installation reference
LICENSE                  Applicable repository license
```

## Quality checks

The offline validation workflow checks shell syntax, selected Python modules, and module entry-point files. These checks do not validate scientific accuracy, online literature services, rendering quality, or optional third-party APIs.

Manual checks:

```bash
python -m compileall -q skills/nature-academic-search skills/nature-citation
find scripts -type f -name '*.sh' -print0 | xargs -0 -r -n 1 bash -n
```

## Research integrity

- Verify paper titles, authors, identifiers, publication dates, and quotations before citing.
- Keep clear provenance for figures, data, and external media.
- Do not represent an inferred reference or fabricated result as verified evidence.
- Keep reproducible computational steps separate from unsupported scientific conclusions.
- Respect publisher policies, individual asset licenses, and confidential research data.

## Contributing

Use English for new repository-level documentation and operational guidance. Keep updates scoped to a module, preserve citations and licenses, and include evidence or tests where applicable. Avoid changing tool interfaces solely to alter surface terminology.
