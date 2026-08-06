# Merge PDFs (pdfunite)

Use when combining multiple PDFs in strict order without re-rendering pages.

## Requirement

```bash
command -v pdfunite
```

## Quick examples

Explicit order:

```bash
pdfunite "封面.pdf" "part1.pdf" "part2.pdf" "merged.pdf"
```

Safer scripted merge (spaces + sorting + collision-safe output):

```bash
bash ./.agents/skills/pdf/scripts/pdfunite_merge.sh \
  --cover "封面.pdf" \
  --pattern "*.chrome-nohf.pdf" \
  --output "5B-worksheet-all.pdf" \
  --dir "."
```

Without cover:

```bash
bash ./.agents/skills/pdf/scripts/pdfunite_merge.sh \
  --pattern "*.pdf" \
  --output "merged.pdf"
```

## Script behavior

- Optional cover prepend
- Pattern collection in target directory
- Lexicographic sort
- Excludes cover duplicate and output file itself
- Collision-safe output (`name.pdf`, `name-2.pdf`, ...)
- Prints only generated output filename on success
