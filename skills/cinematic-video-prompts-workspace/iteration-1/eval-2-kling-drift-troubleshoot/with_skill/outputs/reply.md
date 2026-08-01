Nothing's wrong with your prompting technique — you're fighting a structural fact. Kling has no memory between generations. Each clip is a separate film shot by a separate crew who've never met. Consistency isn't something you ask for, it's something you *build in*, and there are five specific places it leaks:

1. **The lighthouse changes shape** because you described it differently each time. Any paraphrase — "the lighthouse", "the tower", "the old lighthouse" — is a fresh invention. The fix is a locked string: one word-for-word description pasted identically into all eight prompts. Same for the keeper.
2. **Colour drifts** because the palette wasn't restated per shot, and because no amount of prompting replaces a shared grade pass at the end.
3. **The cartoon one** is the tell that nothing in that prompt said *photographed*, and your negative box was empty. A prompt that reads like a story synopsis drifts toward illustration. Kling has a separate negative prompt field — leaving it blank is the single most common cause of this, and pasting negatives into the *main* box is the second most common, because naming "cartoon" positively tends to summon one.
4. **Floating seed / mixed model version** across a session. Lock both before shot 1.
5. **Interiors of the same building** aren't solvable by prompting at all, at any wording quality. That one needs frame chaining.

So I rebuilt the short with those closed. Files:

- **`KLING_PASTE.json`** — the working doc. Eight entries, each with a complete `paste` prompt and its own `negative`. Nothing needs appending.
- **`THE_KEEPER_shotlist.md`** — the same shots explained, so you can direct and recut rather than just paste.
- `scenario.json` + `build_kling.py` — edit the scenario, re-run the script, and the style/palette block gets merged into all eight mechanically. Hand-merging is exactly where packages drift apart.

**The spine I gave it:** he believes he is keeping the light; he is not, and hasn't been for a long time. Eight shots at 5 s = 40 s (run 3, 7 and 8 at 10 s if you want room to breathe).

**The consistency anchor** is a brass hurricane lamp in his hand — the only working light in the film. Every shot is lit by it, so light quality can't drift far, and it runs a clock: steady amber, guttering, bent flat by wind, blue at the base, gone. The tower's own light is absent for seven shots, which means the anchor is doing story work as well as continuity work. There's one deliberate palette break: cold mercury white-green, forbidden until shot 8. Don't grade it back toward warm when you're matching clips.

Structure: dark tower → the climb → the dead lens → the same logbook entry, page after page → **the turn**, unopened supply crates grown over with weed outside → a hull passing unwarned in the dark → he strikes a match and the stairwell has a shape in it → the opening framing repeated, the light on, the lamp gone. Shot 3 ends on the lens as a circle and shot 4 opens on a soot ring on the page — cut on the circle and those two clips read as causally linked. Shots 3 and 7 use the identical camera line; so do 1 and 8.

**Four things Kling can't hold, and what I did about each:**

- **The repeated handwriting (shot 4).** Legible text is still unreliable — you get mush or large legible nonsense. The prompt asks for unreadable ink strokes; the *rhythm* of identical lines carries it. If you want it real, overlay a photographed page in the editor.
- **The figure in the lens (shot 7).** Reflected second figures duplicate or melt. The prompt asks instead for "one tall vertical absence where the reflections do not appear" — a hole in the pattern beats a rendered ghost. ffmpeg overlay recipe in the md if you want the literal version.
- **Shot 8 matching shot 1.** The model has never seen shot 1, so it can't match a framing on request. Generate shot 8 as **image-to-video from shot 1's first frame** and let the prompt only describe what changed. This is the highest-leverage move in the whole package.
- **The building across all eight.** Generate in order and frame-chain the interior seams — last frame of shot N becomes the start frame of shot N+1. Costs nothing, beats any amount of wording.

Two more things before you start. Set Kling's camera movement to **none/custom**, never auto — auto camera is a drift source and every shot already specifies its move in words. And when you regenerate a shot, swap only the subject sentence; leave the camera, lighting, style and palette lines untouched. Editing those is how one shot quietly leaves the film.

Audio is an edit job — Kling's text-to-video won't give you dependable native sound. Constant sea-and-wind bed under every shot never ducking at the cuts (that alone glues clips that don't quite match), one 30 Hz drone entering at shot 4 and never leaving, dry close foley, half a second of total silence before shot 8. No dialogue.

Last shot shows a working light and no keeper, and doesn't say which of those is the horror. I'd leave it there.
