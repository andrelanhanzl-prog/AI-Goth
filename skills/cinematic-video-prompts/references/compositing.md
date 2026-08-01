# Compositing the shots that can't be generated

When triage (step 5) finds a shot the model can't hold, don't just water the shot
down — offer the compositing route as well and let the user choose. These recipes
use ffmpeg only, on clips they already generated.

All examples assume clips in `out/shot_01.mp4` … and 1080p 16:9.

## Contents

- [Concatenate the film](#concatenate-the-film)
- [Reverse replay](#reverse-replay)
- [Circular mask / picture-in-picture](#circular-mask--picture-in-picture)
- [Mosaic of many worlds](#mosaic-of-many-worlds)
- [Subtle overlay](#subtle-overlay)
- [Frame chaining for continuity](#frame-chaining-for-continuity)
- [Fixing drift after the fact](#fixing-drift-after-the-fact)

## Concatenate the film

```bash
printf "file 'shot_%02d.mp4'\n" $(seq 1 10) > out/concat.txt
ffmpeg -y -f concat -safe 0 -i out/concat.txt -c copy out/film.mp4
```

`-c copy` avoids recompression. If clips differ in resolution or codec, drop it and
let ffmpeg re-encode.

## Reverse replay

For "the film rewinds", "the system reboots", "it all happens again" — the model
cannot do this because it never saw the earlier clips. Build it from them:

```bash
# earlier clips, played backwards, 8x faster
ffmpeg -y -f concat -safe 0 -i out/concat.txt -c copy out/_a.mp4
ffmpeg -y -i out/_a.mp4 -vf "reverse,setpts=PTS/8" -an out/_rev.mp4
```

`reverse` loads the whole clip into memory — keep the input under ~15 s or split it.

## Circular mask / picture-in-picture

Put one clip inside a circle in the centre of another:

```bash
ffmpeg -y -i out/shot_07.mp4 -i out/_rev.mp4 -filter_complex \
"[1:v]scale=360:-1,format=rgba, \
 geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':\
a='if(lte(hypot(X-W/2,Y-H/2),H/2),255,0)'[disc]; \
 [0:v][disc]overlay=(W-w)/2:(H-h)/2:enable='between(t,1,5)'" \
-c:a copy out/shot_07_final.mp4
```

`enable='between(t,1,5)'` gates when the inset appears. The empty beats on either
side usually matter more than the inset itself — silence, then the event, then
silence again.

## Mosaic of many worlds

Genuine variety beats asking one generation for variety. Generate 4 short clips of
different subjects, then tile them:

```bash
ffmpeg -y -i w1.mp4 -i w2.mp4 -i w3.mp4 -i w4.mp4 -filter_complex \
"[0:v]scale=960:540[a];[1:v]scale=960:540[b]; \
 [2:v]scale=960:540[c];[3:v]scale=960:540[d]; \
 [a][b]hstack[top];[c][d]hstack[bot];[top][bot]vstack" \
-c:a copy out/mosaic.mp4
```

For vertical slivers instead of quadrants, `crop` each source to a narrow strip
before stacking with `hstack=inputs=8`.

## Subtle overlay

For detail the model renders too large or not at all — a small symbol, a mark, a
glint. Keep it near the threshold of visibility:

```bash
ffmpeg -y -i out/shot_10.mp4 -i assets/detail.mov -filter_complex \
"[1:v]scale=48:48,format=rgba,colorchannelmixer=aa=0.55[fx]; \
 [0:v][fx]overlay=(W-w)/2:(H-h)/2:enable='gte(t,5.5)'" \
-c:a copy out/shot_10_final.mp4
```

Rule of thumb: if someone who isn't looking for it can spot it, it's too strong. A
detail that announces itself stops being a detail and becomes a statement — which
often decides something the piece was deliberately leaving open.

## Frame chaining for continuity

Extract the last frame of a clip to feed the next generation as its opening image:

```bash
ffmpeg -y -sseof -0.1 -i out/shot_05.mp4 -frames:v 1 out/shot_05_last.png
```

Most APIs accept this as the `image` parameter for image-to-video. Use it at the
seams where a location or character must persist; it costs nothing and beats any
amount of prompt wording.

## Fixing drift after the fact

When one clip came back warmer or brighter than the rest, match it in the grade
rather than regenerating:

```bash
ffmpeg -y -i out/shot_04.mp4 -vf "eq=saturation=0.85:contrast=1.08:gamma=0.95, \
colorbalance=rs=-0.05:bs=0.08" -c:a copy out/shot_04_graded.mp4
```

A shared grade pass over every clip at the end is the fastest way to make
independently generated shots read as one piece — often more effective than any
prompt-level consistency work.
