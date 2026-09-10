# Delivery QA

Before delivering the reader, verify these observable invariants:

## Content

- English and Chinese paragraph counts are equal, and spot checks at the beginning, middle, and end confirm one-to-one alignment.
- Section and subsection order matches the PDF.
- No PDF headers, page numbers, line-break artifacts, duplicate passages, TODOs, ellipses used as placeholders, or invented text remain.
- Every main display figure appears once at the correct location.
- Every figure has one complete English legend and one complete Chinese legend.

## Reader behavior

- The HTML loads without network access and every image renders.
- Translation and reading-note toggles work.
- Paragraph and figure note editors save after reload.
- JSON backup/import, Markdown note export, and timestamped annotated-HTML export are present.
- English and Chinese full-text exports are present in the sidebar and preserve source order, headings, body paragraphs, and corresponding legends without AI notes or personal annotations.
- JavaScript parses without syntax errors.

## Presentation

- English and Chinese body text remain comfortable for long reading while showing useful context per screen.
- Major sections are more separated than Results subsections.
- Results and its first subsection do not produce a double-sized gap.
- Figures are visibly attached to the paragraphs that introduce them; their captions remain compact and secondary.
- Desktop and narrow-screen CSS both avoid clipping and unintended horizontal scrolling.

