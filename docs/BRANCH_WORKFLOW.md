# Branches, archives, and curation

## What changed

A Git branch names a commit containing a snapshot of files. Removing notebooks in a new commit on `main` does not remove those notebooks from other branches or erase their history.

1. Started from the existing `main` and checked it was up to date.
2. Created `codex/archive/previous-tutorials` and committed the local notebook 10 edits and new notebook 12 there. Existing notebooks, outputs, and notes were preserved unchanged.
3. Returned to `main` and made a normal cleanup commit removing its notebooks and replacing the old roadmap with a curation workflow. Shared Python tooling remains available.
4. Created `codex/archive/zixiong-tutorials` from the clean baseline and added only the ZiXiong collection, preserving its files and local notebook edits.
5. Created `codex/curation` from clean `main` for new work.

The ZiXiong folder was originally a separate nested Git repository from https://github.com/entropicalabs/QEC-Tutorials.git at commit `7d8ad90266293b77097b03c27d4d46e6355bfbaa`, with local edits. Its working files are archived as ordinary files, including its license, so a normal checkout contains the complete snapshot without submodule setup. Its original Git metadata is retained locally at `.git/local-backups/zixiong-original.git`; this metadata is not pushed. No changes are pushed to the upstream ZiXiong repository.

No force-push or history rewrite is needed. The archives retain notebooks in repository history, so this cleanup does not reduce clone size. Archive branches are read-only by convention, not enforced by branch protection.

## Browse an archive

Before switching, check for uncommitted work and commit it on its appropriate branch.

```bash
git status
git switch codex/archive/previous-tutorials
# Browse the old notebooks.
git switch codex/curation
```

To view the ZiXiong collection, switch to `codex/archive/zixiong-tutorials` instead. You can also browse published archive branches through GitHub's branch selector without switching your local checkout.

## Select one notebook

Start on curation and copy a specific file from an archive:

```bash
git switch codex/curation
git restore --source=codex/archive/previous-tutorials -- 01_stim_basics.ipynb
```

This copies the file into the working tree without merging the rest of the archive. If the destination already exists, the command overwrites that file, so first preserve any edits to it. Copy referenced assets as needed. ZiXiong notebooks may require their image folders and their own dependencies; preserve attribution and license when reusing their material.

Complete and review the selected notebook. Execute it top to bottom in its intended environment, check its explanations and outputs, and preserve learner answers. Update the README and learning records to match the newly curated sequence.

Commit only the intended files, for example:

```bash
git add -- 01_stim_basics.ipynb README.md docs/LEARNING_PATH.md docs/CURRENT_STATE.md
git commit -m "Curate and review Stim basics notebook"
git push -u origin codex/curation
```

A push backs up the curation branch; it does not change `main`.

## Publish reviewed material

Open a pull request on GitHub with base `main` and compare `codex/curation`. Its diff should contain only the notebooks and supporting changes you are ready to publish. Finish our review before merging the pull request.

After merging, update both local branches:

```bash
git switch main
git pull --ff-only
git switch codex/curation
git merge origin/main
git push
```

Keeping curation synchronized after each merge also handles a pull request merged using squash. If Git reports a conflict, resolve and review it before committing; do not force-push to bypass it.

Every unmerged curation change appears in the next pull request. For several independent drafts, create a separate `codex/curate-<topic>` branch from updated `main` for each notebook and review each separately.

Never merge either archive branch into `main`: doing so would bring the historical material back into the published collection. Use file selection for archives and pull requests for curated work.
