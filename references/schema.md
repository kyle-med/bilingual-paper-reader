# Builder input schema

Prepare one UTF-8 JSON file with this structure:

```json
{
  "paper_id": "doi-or-stable-short-id",
  "title": "Original English title",
  "authors": "Author list",
  "journal": "Journal · Article",
  "published": "Published online 1 January 2026",
  "doi": "10.xxxx/xxxxx",
  "supplementary_url": "https://publisher.example/supplement.pdf",
  "source_pdf": "absolute/or/json-relative/path/to/paper.pdf",
  "sections": [
    {
      "id": "abstract",
      "heading_en": "Abstract",
      "heading_zh": "摘要",
      "note_zh": "本节在论证中的作用。",
      "level": "major",
      "kind": "methods",
      "blocks": [
        {"type": "paragraph", "en": "Original paragraph.", "zh": "忠实翻译。"},
        {
          "type": "figure",
          "number": "1",
          "image": "figures/figure-1.png",
          "caption_en": "Fig. 1 | Complete original legend.",
          "caption_zh": "图 1｜完整忠实的中文图注。",
          "source_page": "4"
        }
      ]
    }
  ]
}
```

Rules:

- Section IDs must be unique lowercase slugs. Use `major` for Abstract, Introduction, Results, Discussion and `subsection` for headings within Results.
- `kind` is optional. Use `methods` on the Methods heading, `post-methods` on the first section after Methods, and `references` on References when headings or IDs are unconventional. The builder normally infers these standard headings. Method subheadings stay in the sidebar but render as compact labels, with one aggregate note control after the last Methods paragraph. References render as compact bilingual rows without note controls.
- `supplementary_url` is optional. When present, supplementary-figure citations and the header button open this source.
- Blocks are emitted exactly in array order.
- Every paragraph requires non-empty `en` and `zh` strings.
- Every figure requires a unique number, a readable local image, and complete bilingual captions.
- `source_pdf` is copied into the output folder as `source-paper.pdf`.
- Image paths may be absolute or relative to the JSON file. The builder embeds them in the HTML so the reader itself is portable.
- Use plain main-figure numbers (`"1"`) and prefix Extended Data figure numbers with `E` (`"E1"`). Main-figure citations and sidebar links scroll to the embedded figure. Extended Data citations in body paragraphs open a modal preview; sidebar links still scroll.
