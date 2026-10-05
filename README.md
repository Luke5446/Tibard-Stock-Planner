# Tibard-Stock-Planner

The stock planner is a single page, `index.html`, served by GitHub Pages.
The buying team opens it with `?edit` on the end of the address and works in
it; everyone else opens the plain address and sees the last published plan.

## Publishing

**Publish for team** writes the plan to `data.json` in this repo, which the
viewers read. There are two ways it can do that:

- **Straight from the page** (the normal way): the editor's PC holds a GitHub
  token, and Publish puts the file into the repo itself. The team sees it
  within a minute. Nothing to download or upload.
- **By hand**: with no token on the PC, Publish downloads `data.json` to
  upload to the repo and commit, as before. Publish also falls back to this,
  saying why, if GitHub refuses the token or is not reachable.

### Setting up the token (once, on the editor's PC)

1. On GitHub, **Settings → Developer settings → Personal access tokens →
   Fine-grained tokens**. Either **Generate new token** (name it "Tibard
   stock planner", expiry one year) or edit the cutting-log token the
   production planner uses and add this repo to it. Under **Repository
   access** choose **Only select repositories** and tick `Tibard-Stock-Planner`
   (and `Tibard-Cutlog`, if it is the shared token). Under **Permissions →
   Repository permissions** set **Contents: Read and write**. Save, and copy
   the token: it is shown once.
2. In the planner (with `?edit`), **Set up this PC** in the header: paste the
   token. The button changes to **Token**. The token lives in that browser
   only; **Set up this PC** again with an empty box removes it.
3. Press **Publish for team**. The header says "✓ Published" and the
   published time updates.

A token that can write this repo can change anything in it, the page
included, so keep it to the one PC that publishes. Every publish is a commit,
so the repo's history holds every version of the plan.
