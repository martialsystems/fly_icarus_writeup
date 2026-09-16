# fly_icarus_writeup

Note on the fly_icarus chain. Not a finding. Locks stay on the trees.

The argument is [NOTE.md](NOTE.md). The PDF is [docs/fly_icarus_chain_note.pdf](docs/fly_icarus_chain_note.pdf). Pasteable copy: gist [f979586a](https://gist.github.com/martialsystems/f979586a1142ff4f3b7785a5130eb837). The SHA index is gist [12835f74](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178). Do not restamp `@2cf5fd6`, `@45aa064`, `@e16856c`, `@de95257`, or `@01155c3`.

## How to run

```
.venv/bin/python -m pytest
.venv/bin/python scripts/build_stack_fig.py
.venv/bin/python scripts/build_note_pdf.py
```

## Files

| Path | Role |
|------|------|
| `NOTE.md` | The argument |
| `docs/fly_icarus_chain_note.pdf` | Research-format PDF of the same argument |
| `figures/stack.png` | One stack diagram |
| `AGENTS.md` | Project rules |

[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)
