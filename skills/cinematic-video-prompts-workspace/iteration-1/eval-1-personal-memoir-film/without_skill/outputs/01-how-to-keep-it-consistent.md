# Keeping 8 AI clips from looking like 8 different movies

Your instinct is right — this is *the* failure mode. A generator treats every prompt as a
fresh film. Left alone it will give you one gauzy Netflix period drama, one video-game
cutscene, one drone shot over a suspiciously Alpine Hungary, and one thing that looks like
a pharmaceutical ad. Here is how people actually beat it.

---

## 1. The single biggest lever: pick a conceit that makes variance invisible

Don't fight for photoreal consistency. Choose a look where drift reads as *texture*.

**Recommended conceit for this film: "recovered 16mm, 1956."**

Everything is grainy, desaturated, overcast, handheld, slightly damaged. Under that
treatment, two clips that don't quite match read as two different rolls of film from the
same box — which is exactly what real archival footage looks like. You get consistency for
free because the *degradation* is the through-line.

The alternative conceits that also work: pure silhouette/shadow-play, or heavy
grain-and-shadow black-and-white. What does *not* work is clean, bright, modern
photorealism — that's the mode where every mismatch screams.

## 2. Never show your grandmother's face

Two reasons, one practical and one that matters more.

Practical: faces are where inconsistency is most visible and least forgivable. The model
will not hold the same face across eight generations, and the audience's eye goes straight
there.

The one that matters more: the room will be full of people who know her actual face.
A synthetic near-miss of a beloved 90-year-old lands in the uncanny valley and can read as
slightly ghoulish, at a party, in front of her. Don't.

**So: AI supplies the world. Real photographs supply the person.**

Shoot her in the AI clips from behind, in silhouette, at distance, hands only, feet only,
reflected, out of focus in the foreground. Then cut to a real scanned photo of her at 20
for the emotional payoff. That contrast — grainy invented world, then *her actual face* —
is a far better film than anything fully synthetic, and it's the version that makes people
cry.

## 3. Make an object the character, not a person

Since the face can't carry continuity, give the job to wardrobe and props. Write one
description and repeat it **word for word** in every single prompt:

> a young woman in a brown wool coat with the top button missing, dark green headscarf,
> carrying a small dark leather case

Viewers track the coat. The coat becomes her. This works startlingly well and it's the
trick most people miss.

## 4. Paste an identical style block into every prompt

Not paraphrased. Not "same style as before." Literally copy-pasted, character for
character. Paraphrasing is how you get drift. Keep it in a text file and paste it every
time. The block is in `03-style-block.txt`, and it's already appended to every prompt in
`02-shot-list-and-prompts.md`.

Structure of every prompt:

```
[SHOT: what happens, one or two sentences]
[SUBJECT: the verbatim wardrobe string, if she's in it]
+
[THE STYLE BLOCK — identical every time]
```

## 5. Lock these five things and never vary them

| Thing | Lock it to |
|---|---|
| Aspect ratio | one ratio, all clips, no exceptions |
| Clip length | one length (~8s) — mixed lengths make edit rhythm lumpy |
| Time of day / weather | overcast winter, no sun, no blue sky, ever |
| Camera behaviour | handheld, slow, static-ish. **Zero** drone, crane, zoom, orbit, slow-mo |
| Palette | slate grey, olive brown, bone white, dull ochre — name them every time |

Camera behaviour is the sneaky one. A single soaring drone shot in the middle of eight
handheld shots destroys the illusion harder than any color mismatch.

## 6. Anchor to a first clip

Generate shot 1 until you love it. That clip is now your reference. If your app offers
**remix / extend / storyboard / reference-image** features, build the rest *from* that clip
rather than from scratch — anything generated as a variation of an existing clip will match
it far better than a fresh prompt ever can. Multi-shot storyboard modes are especially
good: shots generated inside one job are consistent with each other by construction.

Also: generate everything in one stretch of a few days. Models get updated, and the same
prompt looks different a month later.

## 7. Expect a 1-in-4 keep rate

Eight shots in the film means roughly 30 generations. That's normal, not failure. Budget
for it. Keep a folder of rejects — some of them will turn out to be better than what you
were aiming for.

## 8. Fix the rest in the edit — this is not optional

This step does more work than all the prompting combined, and almost every guide skips it.

In a free editor (DaVinci Resolve, or CapCut if you want easy):

1. **One color grade across all clips.** Drop the same adjustment layer over the whole
   timeline — crush saturation, lift the blacks slightly, warm the highlights a touch.
   Instantly, eight clips become one film.
2. **One grain/scratch overlay across everything.** Same source, same opacity, top of the
   stack. This is the single most effective consistency tool that exists.
3. **Same subtle vignette.** Ties the frames together.

Mismatches you can see in the raw exports largely stop being visible once everything is
sitting under the same grade and the same grain.

## 9. Audio is the real glue

Visual continuity is what you're worried about. Audio continuity is what will actually
carry the film. A single unbroken sound bed — one piece of music, or wind and footsteps
running continuously *across* the cuts — makes the audience read discontinuous images as
one continuous memory. Let sound cross every cut; never let music and picture change at the
same moment.

**And the thing to do first, before any of this:** she is 90 in March, and you have months.
Go record her telling the story. Phone voice memo is fine. Her own voice, in her own
accent, over these images, is worth more than every prompt in this document put together —
and it is the one asset you cannot generate later. Even if you end up not using it in the
film, record it.

---

## Three things to avoid

- **Don't recreate documented atrocity or specific real people.** Keep it to her journey:
  streets, a train, the border, the marsh. Not synthetic footage of real killings.
- **Don't caption it with invented specifics.** If you don't know she crossed at Andau,
  don't put "Andau" on screen. Check the details you can with her or with family; leave the
  rest unstated. Nobody minds an unnamed border. Everybody minds a wrong fact at her party.
- **Don't over-cut.** Sixty seconds is 7–8 shots, not 20. Long, quiet, held shots read as
  confident and archival. Fast cutting reads as a trailer, and exposes every inconsistency
  by putting mismatches next to each other.
