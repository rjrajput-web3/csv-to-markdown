# csv-to-markdown

Turn a CSV file into a clean GitHub-flavoured Markdown table. Stdlib only — no dependencies.

## What it does

- Reads a CSV file, or CSV from stdin.
- Prints a Markdown table with an alignment row.
- Escapes `|` inside cells so the table never breaks.
- Pads short rows and strips surrounding whitespace.
- Optionally truncates long cells with `--max-col-width`.

## How to run

```bash
python csv_to_markdown.py data.csv
cat data.csv | python csv_to_markdown.py
python csv_to_markdown.py data.csv --align center --max-col-width 30
```

## Example

Input (`sample.csv`):

```csv
name,price,stock
Keyboard,49.99,12
Mouse | wireless,19.99,0
```

Output:

```
| name | price | stock |
| :--- | :--- | :--- |
| Keyboard | 49.99 | 12 |
| Mouse \| wireless | 19.99 | 0 |
```

With `--align center`:

```
| name | price | stock |
| :---: | :---: | :---: |
| Keyboard | 49.99 | 12 |
| Mouse \| wireless | 19.99 | 0 |
```

With `--max-col-width 8` (stdin):

```
| name | price | stock |
| :--- | :--- | :--- |
| Keyboard | 49.99 | 12 |
| Mouse \… | 19.99 | 0 |
```

## Exit codes

- `0` — ok
- `1` — malformed CSV or file not found
- `2` — empty input or bad argument
