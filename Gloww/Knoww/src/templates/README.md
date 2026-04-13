# src/templates/

Starter templates for writing new posts. Copy one into the matching `src/content/` folder.

## Usage

```bash
# writing a new TIL post
cp src/templates/til-template.mdx src/content/til/my-new-til.mdx

# writing a product thought
cp src/templates/product-template.mdx src/content/product/my-product-thought.mdx

# adding a new build
cp src/templates/builds-template.mdx src/content/builds/my-project.mdx
```

Then open the file, fill in the frontmatter fields, replace the placeholder text, and set `draft: false` when you're ready to publish.

## Templates

| Template | For | Key fields |
|----------|-----|-----------|
| `til-template.mdx` | Today I Learned posts | title, pubDate, tags, emoji |
| `product-template.mdx` | Product thoughts/teardowns | title, pubDate, type, tags |
| `builds-template.mdx` | Project showcases | title, techStack, status, github |
