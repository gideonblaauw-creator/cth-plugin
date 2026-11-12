# Monday read-only access for Aris Woodyear

**Date:** 21 Oct 2026
**Status:** Blocked in the API. Needs a Monday UI step by Gideon.
**Awaiting Gideon's approval** before anyone sends the link.

## Result

Monday has no API route that returns a read-only board view link. No link was created. No email was sent. Aris was not added to the board.

## Board

- Account: `cleantechhub-foundation`
- Board: `18407932632`, REIN Hubs 2026 — Fundraising Leads
- URL: https://cleantechhub-foundation.monday.com/boards/18407932632
- `board_kind`: `public` (not `share`)
- `permissions`: `everyone`
- Owner and only subscriber: Gideon Blaauw (`61633390`)
- Workspace: REIN Hubs — CTH × Pvblic (`14985829`)

Board items were not read. Columns, items, and other people's permissions were not changed.

## Guest

- Aris Woodyear, `aris.woodyear@pvblic.org`, user id `120126684`
- `kind`: `guest`
- `status`: `PENDING`
- `invitation_method`: `USER`
- Created: `2026-10-21T19:37:12Z`
- Not a subscriber on this board

The pending guest invite was not resent.

## How the API was called

`MONDAY_API_TOKEN` and `MONDAY_API_KEY` were not in this process environment. The Infisical CLI and a machine identity were not on this VM. Calls used the active Monday connector for `cleantechhub-foundation`. No token was printed. Keys stay in Infisical project `cth-agents`, path `/`.

## API errors

1. Earlier attempt, not repeated: `add_users_to_board` returned **403**, `Cannot add guest users to non-shareable boards`. Guests can only join boards with `board_kind: share`. Retrying that mutation can notify people, so it was not sent again.

2. `BoardView` has no share URL field. Exact error:

```text
Cannot query field "share_url" on type "BoardView"., Cannot query field "share_link" on type "BoardView"., Cannot query field "public_url" on type "BoardView"., Cannot query field "url" on type "BoardView".
```

3. No share-link mutation. Exact errors:

```text
Cannot query field "share_board_view" on type "Mutation". Did you mean "change_board_kind" or "restore_view"?
```

```text
Cannot query field "create_shareable_board_view_link" on type "Mutation".
```

These were schema validation errors. They did not run a change.

4. View mutations that do exist are `create_view`, `create_view_table`, `update_view`, `update_view_table`, `delete_view`, `duplicate_view`, and `restore_view`. TABLE, FORM, and APP settings schemas have no share or public URL property. Monday's docs assistant found no mutation that generates a public or read-only share link for a board view. The developer community says the same: the board URL requires a login, and no query returns the shareable link.

5. The only view on the board is **Build Vibe view** (`258162847`, type `FeatureBoardView`). Its stored address is an in-account embed, not a public `view.monday.com` link:

https://cleantechhub-foundation.monday.com/app_feature_embedded/15528052/board_view/168879764

`settings_str` is `{"view_subtype":"monday-vibe-app"}`. Do not send that URL as the read-only link.

## Stopped on purpose

- `change_board_kind` was not called. The live schema describes it as changing privacy (`public` / `private` / `share`). Monday's coverage-gaps page says `board_kind` cannot be changed after creation. Calling it would change board privacy.
- `set_board_permission`, `invite_users`, `add_users_to_board`, and `add_subscribers_to_object` were not called.
- `create_form`, `activate_form`, and `shorten_form_url` were not called. A form accepts submissions. It is not a read-only view of the leads.
- Aris was not made a member. Gideon is still the only subscriber.

## Manual step for Gideon

Only a board owner can do this. Source: [How to share a board view publicly](https://support.monday.com/hc/en-us/articles/360009695080-How-to-share-a-board-view-publicly) (modified 8 Sep 2026).

1. Open https://cleantechhub-foundation.monday.com/boards/18407932632.
2. Select the **main table**, not Build Vibe view.
3. Click the three-dot menu to the right of that view name.
4. Choose **Share**.
5. Click **Copy** on the shareable link. It looks like `https://view.monday.com/<token>`.
6. Send that link to Aris yourself. Anyone with the link can view it in a browser, without a Monday login and without a paid seat.

Monday limits on a shared view: files columns are not downloadable, hidden or restricted columns are omitted, updates are not shown, and mirrored items are omitted. A board with item-viewing permissions cannot be shared this way. This board's general permission is `everyone`. If **Share** is missing, stop. Do not convert the board to a shareable board, and do not invite Aris as a member.

Aris's guest user is still `PENDING`. The public view link does not require that invite to be accepted.
