# Branches and archived notebooks

`main` is the published notebook collection. It contains `shor_tutorial.ipynb`. Work on the next notebook in `codex/surface-code-tutorial`, which starts from `main`. Use a fresh topic branch from updated `main` for later notebooks.

The older notebook collections are preserved on two reference branches:

- `codex/archive/previous-tutorials` contains notebooks 01–12, the extra stabilizer notebook, older archived notebooks, and local learner work.
- `codex/archive/zixiong-tutorials` contains the ZiXiong collection, including its local edits, assets, dependencies, and license. The original ZiXiong project came from https://github.com/entropicalabs/QEC-Tutorials.git at commit `7d8ad90266293b77097b03c27d4d46e6355bfbaa`. Its Git metadata is retained only in a local backup; no changes are pushed to that upstream repository.

Archive branches are read-only by convention. Do not merge an entire archive into `main`. To reuse one notebook, copy that file and its required assets into a topic branch, then review them there. For example:

```bash
git switch codex/surface-code-tutorial
git restore --source=codex/archive/previous-tutorials -- 01_stim_basics.ipynb
```

The restore command overwrites a file of the same name in the working tree, so first preserve any edits to that path.

After finishing a new notebook, execute it, review the content and rendered output, update the README and learning path, and publish the reviewed topic branch to `main` when authorized. [Notebook review](NOTEBOOK_REVIEW.md) describes the review procedure. The sibling local `Overleaf/` folder has its own workflow and is outside this Git repository.
