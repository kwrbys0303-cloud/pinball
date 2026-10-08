# 「悪魔ノ消エタ日」生成AIプロンプト集（2026年10月8日）

背景画像と、場面1〜4の音源（BGM）を別のAIで作るためのプロンプト。
スライドの生徒の写真の枠（オープニング・エンディングなど）は別に空けておく。

## 共通の考え方
- 音源：ハ長調／イ短調。C・Am・F・G7 の4コードのみ。各コード最低1小節（遅い場面は2小節）。セリフの下で流すので音数少なく。
- 画像：全場面同じ絵のタッチ。人物・文字なし。下3分の1は字幕用に暗め・模様少なめ。
- プロンプトは英語（生成AIに通りやすい）。

---

## 音源（場面1〜4）

### 共通の一文（各プロンプトの後ろにつける）
```
Instrumental only, no vocals. Key of C major / A minor. Use ONLY these four chords: C, Am, F, G7 — no other chords. Each chord must last at least one full bar (4 beats). Steady tempo, clear downbeat, no tempo or key changes. Sparse arrangement that leaves space for spoken dialogue and a live ukulele group playing along. About 90 seconds, loopable.
```

### 場面1　王女の城（コミカル＋不穏）
コード進行（各1小節・104BPM）：C｜C｜Am｜Am｜F｜F｜G7｜G7｜Am｜Am｜F｜G7｜Am｜Am｜F｜G7｜
```
A comedic yet sinister royal march for a spoiled, cruel princess in her castle. Playful and mischievous on the surface, with an ominous undertone hinting at something dark. Pizzicato strings, bassoon, harpsichord, tuba bass, light glockenspiel accents, soft low string swells on the A minor bars. 104 BPM, 4/4.
Chord progression (one chord per bar): C | C | Am | Am | F | F | G7 | G7 | Am | Am | F | G7 | Am | Am | F | G7 | then repeat.
```
ウクレレ：1拍目と3拍目に「ジャン、ジャン」と短く切って弾く。

### 場面2　ひとりの剣士（さびしさ＋戦いの予兆）
コード進行（各2小節・72BPM）：Am｜Am｜F｜F｜C｜C｜G7｜G7｜×2（2回目で緊張が高まる）
```
A lonely swordsman alone on a windswept hill at the edge of a kingdom. Melancholic and quiet at first, then a growing sense that a battle is about to begin. Solo wooden flute, soft cello, gentle wind ambience. In the second half, add a low drum like a heartbeat and tremolo strings that slowly grow in tension. 72 BPM, 4/4.
Chord progression (each chord held for two bars): Am | Am | F | F | C | C | G7 | G7 | — play twice; the second time builds tension and ends on G7.
```
ウクレレ：1小節に1回ゆっくりかき下ろして響かせる。後半は語り部4人が少しずつ回数を増やす。

### 場面3　戦い（テンポよく・うきうきするコミカルな戦い）
コード進行（各1小節・132BPM）：Am｜F｜G7｜C｜×2 → F｜G7｜Am｜Am｜→ くり返し
```
A fun, bouncy, comedic battle scene — exciting but playful, like a cartoon action chase. Brass stabs, snare drum march rhythm, pizzicato strings, quick xylophone runs. Upbeat and cheerful. IMPORTANT: no bongos, no congas, no busy hand percussion — leave space for live bongo and ukulele. 132 BPM, 4/4.
Chord progression (one chord per bar): Am | F | G7 | C | Am | F | G7 | C | F | G7 | Am | Am | then repeat.
```
ウクレレ：ダウン・アップの速いストローク。ボンゴが主役。最後の「ジャーン！！」は生演奏なので、音源はその手前でフェードアウト。

### 場面4　はんぶんこ（静かで真剣な対峙）
コード進行（各2小節・60BPM）：Am｜Am｜F｜F｜C｜C｜G7｜G7｜（G7で終わり、糸の前奏へ）
```
A quiet, serious confrontation between a cornered princess and a lonely swordsman. Still, tense, but with a hint of tenderness. Very sparse: soft solo piano with long sustained strings, lots of space between notes. No drums. 60 BPM, 4/4.
Chord progression (each chord held for two bars): Am | Am | F | F | C | C | G7 | G7 | — end unresolved on G7.
```
ウクレレ：基本は弾かない。「おいしい。」の直前などに C を1回だけそっと鳴らす。

### 場面5
いきものがかり「YELL」（ピアノ）を流すので作らない。

---

## 背景画像（人物なし・風景中心）

### 共通の一文（各プロンプトの後ろにつける）
```
Wide 16:9 storybook fantasy illustration, painterly, soft lighting, rich colors, family-friendly and not scary. No people, no characters, no faces, no human silhouettes, no text, no letters, no logos. Keep the lower third of the image simple and slightly darker so white subtitles are easy to read.
```

### プロローグ・題名
```
A distant fantasy kingdom at twilight. A castle on a hill under a deep purple sky with the first stars appearing. A faint dark mist drifts around the castle, hinting at a hidden curse. Mysterious and beautiful.
```

### 場面1　王女の城
```
A grand royal throne room. A golden throne at the end of a long table piled high with sweets — donuts, puddings, cakes — and many empty chairs. Candles and red velvet curtains, luxurious, but cold purple light from tall windows and deep shadows make it feel lonely and slightly sinister.
```

### 場面2　ひとりの剣士
```
A windswept rocky hill at the border of a neighboring kingdom. A single large flat rock, dry grass bending in the wind, one bare tree, grey clouds. A castle silhouette far away on the horizon. Dark storm clouds gather on one side of the sky, as if a battle is coming. Lonely and quiet.
```

### 場面3　戦い
```
The same windswept hill, now full of energy: a dramatic sky with sunbeams breaking through moving clouds, grass and dust swirling in the wind. Bright, bold colors, exciting adventure mood.
```

### 場面4　はんぶんこ
```
The same hill at dusk, very quiet. Moonlight shines down on the large flat rock like a spotlight. Deep blue tones, still air, a few fireflies. Calm, serious, and gentle.
```

### 場面5　新しい道
```
Sunrise. A winding country road leads from the hill across green fields toward a small, warmly lit town in the distance. Golden morning light, hopeful and warm, the road continuing far ahead.
```

---

## コツ
- 音源：指定外のコードが混ざることがある。ウクレレで C・Am・F・G7 を合わせて確かめ、ずれたら作り直すか、その部分を使わない。
- 画像：場面2〜4は同じ丘。場面2を先に作り、それを参考画像にして天気・時間帯だけ変えると場所がつながる。
- 画像のNG指定欄があれば：people, person, character, face, text, watermark, blood
