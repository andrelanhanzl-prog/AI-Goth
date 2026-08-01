Your worry is the right one, and I want to be straight with you about it: it's mostly not a prompting problem. Eight Sora clips look like eight different movies because they *are* eight independent generations with no memory of each other. Prompting narrows the gap. Three things in the edit close it.

So here's the package, and then the honest part.

**The film: "The Green Coat."** Eight shots, 8 seconds each. A woman takes a coat off a hook in Budapest in November 1956 and walks out of Hungary. Seventy years later the same coat hangs on a hook in a kitchen where a table is being laid. Shot 1 and shot 8 are the same framing; shots 3 and 6 are the same framing — she turns her head and looks back, once under a streetlamp, once standing in a marsh. That repetition is the structure, and it's most of what makes it feel like one film.

**The anchor is the coat** — dark green wool, a hand-stitched grey repair on the left cuff. It's in all eight prompts in identical words, and its condition is the clock: clean on a hook, on her back, mud to the knee, frozen in marsh water, steaming in a doorway, clean on a hook. If a take comes back with the wrong coat, bin it. That's the one thing worth being strict about.

**Three things I'd push back on, or want you to know before you spend credits:**

*No faces. Anywhere.* Sora won't give you her likeness, and what it will give you is eight different twenty-year-old women — your exact fear, in its worst form, in front of a room of people who know her face. So the whole film is shot from behind, beside, and below her: hands, a silhouette, a coat hem, boots, one tiny figure in a huge marsh. It's a real style — a film that follows someone rather than looks at them. And it means the last four seconds can be **a real photograph of her at twenty**, held still, slow push in, black. After fifty-six seconds of never seeing her face, that's the payoff, and nothing generated will beat it.

*The continuity fix is in the edit, not the prompt.* In order of how much they matter: (1) one continuous piece of music across the whole minute, with every clip's generated audio muted — this is the single biggest one and it's free; (2) one shared colour grade over all eight clips; (3) then the anchor and the identical style sentences. I've put the ffmpeg commands for 1 and 2 in the doc. Do them. Prompting alone won't get you there.

*Ask her first.* I've written it as the common route — Budapest, the border marshes near Andau, an Austrian farmhouse at dawn. About 200,000 people left that way that winter, so it may well be hers. But four prompts assume it: where she left from, how she crossed, what she carried, where she arrived. Ask her, then change those four lines in `scenario.json` and rerun the build script. Every real detail beats the generic version.

And the optional thing that will wreck the room in the best way: record twenty seconds of her telling it, on your phone, and lay her voice over the middle of the film with the music underneath. One sentence in her own voice over the marsh shot is enough. That's the film — the generated part is the illustration.

**Files** (in `/home/user/AI-Goth/skills/cinematic-video-prompts-workspace/iteration-1/eval-1-personal-memoir-film/with_skill/outputs/`):

- `SORA_PASTE.json` — paste-ready. Eight complete prompts; each is self-contained, nothing to append.
- `THE_GREEN_COAT.md` — the same prompts laid out per shot with what each one is doing, what Sora will refuse or mangle and what to do instead, and the assembly steps.
- `scenario.json` — the source file. Edit this and rerun `build_paste.py`, rather than editing the paste file by hand — hand-editing is exactly how one shot drifts.

Two practical notes. Generate shot 1 and shot 8 first so you can compare the two hook framings and regenerate whichever is worse before spending anything on the middle. And check on your very first clip whether your Sora plan puts a watermark on downloads — that decides whether you can project this, and you want to know now, not in March.
