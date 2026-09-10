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
  "source_pdf": "absolute/or/json-relative/path/to/paper.pdf",
  "sections": [
    {
      "id": "abstract",
      "heading_en": "Abstract",
      "heading_zh": "摘要",
      "note_zh": "本节在论证中的作用。",
      "level": "major",
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
- Blocks are emitted exactly in array order.
- Every paragraph requires non-empty `en` and `zh` strings.
- Every figure requires a unique number, a readable local image, and complete bilingual captions.
- `source_pdf` is copied into the output folder as `source-paper.pdf`.
- Image paths may be absolute or relative to the JSON file. The builder embeds them in the HTML so the reader itself is portable.

