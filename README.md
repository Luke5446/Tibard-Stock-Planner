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
- **No token on the PC**: nothing is published. A red **Please add a token
  to publish** warning appears beside the button until one is set up
  (26 Oct 2026; before that Publish downloaded `data.json` to upload by
  hand, which looked like a publish to anyone not expecting it). If GitHub
  refuses the token or is not reachable, Publish still downloads `data.json`
  and says why.

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

## Changing a container

A container card opens its contents. **Edit quantities** changes the units on
a line (0 removes it). **+ Add code** (24 Oct 2026) puts one more code on the
container: type or pick the stock code and the units. A code already on the
container has the units added to its line; a code not in the stock data is
allowed, but named, since the projected-stock list only shows codes it knows.

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

- **Air wks** column: weeks cover on the day the air freight lands (date in the
  bar, default 3 weeks) = stock left that day + Air qty, divided by weekly usage,
  with the SKU's next container or works order beside it. Air freight is a top-up
  to bridge to that arrival, not a 12-week target. The Export air freight modal
  summarises the same for the ticked rows.
- The header checkbox in the tick column ticks or unticks only the rows in the
  current filter (e.g. the Needs air freight tile).
- **Export container** and **Export air freight** add `Price` and `Total
  Price` columns to the CSV, with the total value on the TOTALS row. A line
  whose code is not in the list is left blank, and the export summary says
  how many lines are unpriced.
- **Mark as booked in** opens a box with the container's value in USD,
  worked out line by line from the list, which can be changed before booking
  in. The value is kept on the booked container (`valueUSD`) and is published
  with the plan, so the KPI dashboard reads it for Clockwork stock bought in.
  **✎ value** on a booked card changes it later; undoing a booking clears it.

- **Sage PO file** on a container card makes the purchase order as the file
  the Sage routine imports from the `B2B_PO_TIB` folder: the routine's own
  39-column layout, supplier CLO003, order date today, requested date the day
  the container lands, the reference typed when the file is made as the
  supplier document number. A code that has a **BULK** item in Sage goes on
  its BULK code to the Bulk warehouse; every other code, and every NHSP code
  whatever Sage holds, goes as itself to Home. Which codes have a BULK item is
  a list in the page (Sage's Bulk stock view of 18 Jun 2026 plus
  WAGHTM016015); the BULK codes are on their way out, so it is not meant to
  grow. The unit price is the price list, in USD. The Sage import fails on
  a blank price (C128, 19 Oct 2026), so a line with no price on the list is
  named before the file is made, and again in the summary, to be priced
  first or filled in by hand; the summary also says how many lines went on
  BULK and how many on the plain code. The line requested date is left blank,
  as it was on the C127 file that imported. The card notes when the file was
  made.

Without prices, the book-in box is empty and the value can be typed from the
invoice, or left blank and added later.

## Fabric usage (Clockwork's monthly fabric report)

Clockwork send a fabric usage report each month: every cloth they hold for
us, metres on hand, metres on order with their ETAs, and (column D) the
styles each cloth is cut for. The **Fabric usage** tab (24 Oct 2026) takes
that file and sets our own demand against it, so a shortage is seen while a
container is being planned rather than when Clockwork say so.

- **Import Clockwork report** (editor only): choose the `.xlsx`, or paste
  the sheet, and give the report's date (it sets the year on ETAs written
  like "NOV 23"). Columns are read by heading, so their order does not
  matter; every column headed ETA is read, and "IN PRODUCTION" or "TBC" is
  kept as a line with no date. Black precure and Teredo black vat dye are
  interchangeable and shown as one line (`FABRIC_POOLS` in the page).
- **The table**: cloth, description, colour, in stock, on PO, our demand,
  free (in stock − demand), after PO, status and the next ETA. Click a row
  for the ETA lines and the container-by-container cover; click a heading
  to sort. *Critical* is short with no PO landing within 3 weeks; *Low* is
  short but covered by a PO within 3 weeks, or free stock under a month of
  Clockwork's own average usage.
- **The container PO check** (29 Oct 2026). On the day a container PO is
  created, when it is saved to the tracker or its Sage PO file is made,
  every cloth it cuts is checked, after the containers ahead of it in
  priority: enough at Clockwork, or short but their cloth PO lands within
  3 weeks of that day, is OK; short with the cloth landing later, or no
  cloth PO at all, is **Check with supplier**, to confirm with Clockwork
  before committing. The result and its date sit on the container's card
  (`fabricCheck` on the PO), the Sage PO file asks before going ahead on a
  flag, and the check runs again when the container's lines change or the
  badge on the card is clicked. Codes with no cloth or metres figure are
  listed as unchecked.
- **Our demand** is the metres the open containers will cut, in priority
  order: air freight first, then the C numbers in order, then the container
  being planned on the Stock planner tab. A container is **shipped** (its
  cloth already cut, so not counted) when the Shipped box on its card is
  ticked; left alone, an air freight within 2 weeks of landing and a sea
  container within 5 weeks are taken as shipped.
- **The planner's Fabric column** shows, for each code, the free metres of
  its cloth once everything above is cut, and updates as the Actual cartons
  change. Short, it shows the PO ETA that covers it: amber within 3 weeks,
  red beyond (the date the cartons could go on), or "no PO".
- **Which cloth a code takes** comes from Clockwork's own style list on the
  report, with the colour in our Sage description choosing between cloths
  (CJ0193 in 03 is black, in 01 white; a colour the list leaves out is found
  in the same cloth, so a black mesh-back jacket is black precure). Mesh
  backs take the bird-eye mesh too. **Metres per garment** is `CKW_USAGE`
  in the page, copied from the production planner's costing and lay-plan
  figures by `tools/build-fabric-usage.py` (run it again, with the
  production planner checked out beside this repo, when its figures change);
  a customer variant with no figure takes its base style's, marked as such.
  The **Codes and their cloth** panel under the table lists every style the
  tab could not work out: pick the cloth, type the metres (and mesh metres),
  Save, and every size of that style follows. Tick "show every style" to
  review the automatic choices too.
- The report, the mappings and the Shipped ticks are saved with the plan
  and published with it, so the view-only page shows the same tab, without
  the import or the mapping controls.
