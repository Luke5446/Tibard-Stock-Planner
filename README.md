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

## Clockwork prices and container values

**Price list** in the editor's header opens the Clockwork price list. Paste
the container order template's Data tab into it (stock code through to the
Clockwork price, row 2 down) and press **Save prices**: once a year when the
prices change, or when new bought-in products are added, since pasting again
updates the codes it covers and keeps the rest. The button shows how many
codes are priced, and a warning sign when the list needs attention. The
prices are never in `data.json`, and the view-only page never shows a price,
a container value or the button itself.

### Where the prices are kept

- **On the editor's PC**, in their own browser store, so **Clear** (all saved
  data) leaves them alone.
- **In the repo**, as `prices.json`, locked with a **passphrase** (AES-GCM,
  key from the passphrase by PBKDF2-SHA256, 600,000 rounds). Save prices puts
  the file into the repo through the GitHub token on the PC; with no token it
  downloads the file to upload and commit by hand, after which **Check the
  repo** in the price list confirms it arrived. The file holds only the
  ciphertext, the date and the number of codes, so it is unreadable without
  the passphrase.

The first time, press **Save to repo** (or Save prices) and choose a
passphrase when asked: at least 12 characters, three or four words is
easiest. The repo is public, so a short passphrase could be guessed, and
every version of `prices.json` stays in the repo's history: a passphrase that
has leaked cannot be taken back by changing it, only kept from new saves.
**Passphrase** in the price list changes it (the saved copy is re-locked and
saved again) or removes it from the PC. The passphrase is kept on the PC like
the token. Anyone who knows it, and the site's address, can read the prices,
so keep it to the buying team.

When the editor's page opens it reads `prices.json` from the site and, if it
is newer than the PC's copy and the passphrase on the PC opens it, takes it:
a cleared browser or a new PC gets the prices back with nothing more than the
passphrase (the price list offers **Unlock with the passphrase**, which never
overwrites the repo). An older copy on the site never replaces newer prices
on the PC; **Save to repo** asks before replacing a newer copy the PC cannot
open. **Clear prices** removes the prices from the PC and asks whether to
clear the saved copy too: keep it, and the passphrase is removed from the PC
as well, so a handed-over PC holds nothing while another PC can still get the
prices back. **Clear** (all saved data) leaves the price list alone.

### What the prices do

- **Export container** and **Export air freight** add `Price` and `Total
  Price` columns to the CSV, with the total value on the TOTALS row. A line
  whose code is not in the list is left blank, and the export summary says
  how many lines are unpriced.
- **Mark as booked in** opens a box with the container's value in USD,
  worked out line by line from the list, which can be changed before booking
  in. The value is kept on the booked container (`valueUSD`) and is published
  with the plan, so the KPI dashboard reads it for Clockwork stock bought in.
  **✎ value** on a booked card changes it later; undoing a booking clears it.

Without prices, the book-in box is empty and the value can be typed from the
invoice, or left blank and added later.
