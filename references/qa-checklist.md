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
- Main-text paragraph and figure note editors save after reload. Methods exposes exactly one aggregate note control after its final paragraph; References exposes none.
- Main-figure citations in body text and all sidebar figure links scroll to the embedded figure. Extended Data citations in body text open a modal preview, and closing the modal returns focus to the source citation.
- JSON backup/import, Markdown note export, and timestamped annotated-HTML export are present.
- English and Chinese full-text exports are present in the sidebar and preserve source order, headings, body paragraphs, and corresponding legends without AI notes or personal annotations.
- JavaScript parses without syntax errors.

## Presentation

- English and Chinese body text remain comfortable for long reading while showing useful context per screen.
- Major sections are more separated than Results subsections.
- Results and its first subsection do not produce a double-sized gap.
- Figures are visibly attached to the paragraphs that introduce them; their captions remain compact and secondary.
- Methods is visually continuous: compact method labels, smaller bilingual text, no repeated reading-note cards, and no repeated note buttons. Its method headings remain in the sidebar.
- References uses smaller plain bilingual rows with no colored translation panels, reading-note card, or note button.
- Desktop and narrow-screen CSS both avoid clipping and unintended horizontal scrolling.
