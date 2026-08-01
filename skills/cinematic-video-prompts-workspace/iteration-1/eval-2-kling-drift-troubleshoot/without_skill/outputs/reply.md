Nothing's wrong with your prompts as prompts — you're just asking Kling to do something it structurally cannot do. There's no memory between generations. Every click builds a new world from scratch. Eight clicks, eight films.

**The core diagnosis:**

- **Color drifts** because text-to-video color is an accident of unstated lighting. If you don't name the light sources and their color temperature, the model picks — differently each time. (Also: if any of those 8 were made on a different Kling version, that alone breaks color continuity. Never mix versions.)
- **The lighthouse changes shape** because you're re-describing it in words each shot. "A tall lighthouse on a rock" has a billion valid renderings and you're sampling from all of them. Especially fatal if it has stripes or countable windows — models cannot hold a count.
- **The cartoon one** is text-to-video with an empty negative prompt and the Creativity slider too high. Illustration and 3D-render are massive attractors in the training data and you have to actively push away from them on every single generation. Kling's negative prompt field also tends to silently blank between generations — check it every time.

**The fix is one shift:** stop writing 8 prompts, start building a set and shooting on it.

Generate five still plates first — lighthouse exterior, keeper portrait, quarters interior, spiral stair, lamp room — in a stills model where iteration is cheap. Get those five looking like one film. *Then* go to Kling, image-to-video only, using those plates as start frames. Zero text-to-video, not one shot.

Two things that follow from that, which most people miss:

1. **Once you're on start frames, your prompts must get much shorter.** The image already locks the look. If you also describe the look in the prompt, the model tries to satisfy both and you get morphing and texture crawl. In image-to-video the prompt describes **motion only** — one or two sentences.

2. **Render your lighthouse plate once at max resolution and crop into it** for every exterior framing. Same pixels, so the geometry physically cannot drift. I've built your shots 1 and 8 as crops of the same plate, which means your first and last shot will match perfectly and the whole piece reads as designed rather than assembled.

And the honest part: even done right, this gets you ~85% matched. The last 15% is post. One grade node across all 8 in Resolve, plus a single grain pass over everything — grain is phenomenal continuity glue and hides a huge amount of color mismatch. Anyone claiming they got 8 matching AI clips straight out of the box isn't showing you the ones they binned.

**One story note.** Your premise is doing you a favor you should cash in. "The light has been off for weeks" means the whole film is lit by one lantern — and a single practical source is the easiest thing in the world to keep consistent across generations. Your dramatic constraint and your technical constraint are the same constraint. So lean all the way in: no moonlight, no fill, no second source, ever.

Then the horror beat is **dust.** Weeks of it, thick on the brass, and *undisturbed* — no handprints, no footprints, nothing touched. That's your evidence, it lands with no dialogue, and it's shot 6. That shot is your film. I'd generate 5 variants of it and 3 of everything else.

Two files for you:

- **`diagnosis-and-continuity-kit.md`** — full breakdown, the locked style/negative/subject blocks to paste verbatim, the plate build order, your pinned Kling settings, and triage on which of your existing 8 are worth keeping (short answer: anything wrong on color, keep — that's a post fix. Anything wrong on geometry, rebuild.)
- **`shot-prompts.md`** — all 8 shots. Each has the stills prompt to build its start frame, the short Kling motion prompt, and a note on what to watch for. Cut order and a per-shot checklist at the bottom.

The one discipline that makes it work: **the locked blocks never change, by even one word.** The moment you "improve" the style block for shot 5, shot 5 stops matching. Copy-paste, don't paraphrase.
