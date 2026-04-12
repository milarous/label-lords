## Label Lords — A Clear Path Forward

### 🟢 Easy Wins (Make it "playable" fast)

These are low-effort, high-impact additions that bring the game to life without deep systems work.

**1. Artist Stats & Personality Traits**
Right now artists are probably just names. Give each one 3–5 stats — *Hype, Talent, Marketability, Work Ethic, Loyalty* — randomly generated on creation. These feed into existing release outcomes, so you get variety without building new systems. It also makes "which artist do I sign?" an actual decision.

**2. A Proper Dashboard / Home Screen**
A single page showing your label name, current week, cash balance, total artists signed, and a "trending releases" widget. This immediately makes the game feel like it has a state and a heartbeat. Even a simple styled card layout goes a long way here.

**3. Chart Position Display**
Show a Top 10 chart that updates each week. Your releases compete against AI label releases for chart spots. This is the "Chart Wars" element — without a visible chart, the game has no tension. You can fake the AI competitors for now with random entries.

**4. Win/Lose Conditions**
Even a simple one: if your cash drops below zero, game over. If you reach a certain revenue milestone or chart position, you "win the season." This gives the player something to play *toward*.

**5. A Weekly "Events" Feed**
After each "Finish Week" action, show a brief news feed — *"Your single debuted at #7!", "Artist X's popularity dropped", "A rival label poached unsigned talent"*. This makes the week-end feel like something happened.

---

### 🟡 Medium Effort (Core gameplay depth)

**6. Rival AI Labels**
2–3 competing labels that also sign artists, release music, and compete for chart spots. You don't need clever AI — just simple weekly logic (they release a song every N weeks, their artists have stats too). This creates the adversarial pressure the game needs.

**7. Budget & Expenses**
Artists should have weekly wages. Promotions should cost money. Releasing an album should be a bigger investment than a single. Suddenly every decision has a cost, and cash management becomes the core loop.

**8. Artist Morale / Loyalty System**
If you underpromote an artist or they keep missing the charts, their loyalty drops. Low loyalty = they ask to be dropped or demand a pay rise. This creates roster management tension.

**9. Genre System**
Artists have a genre (pop, hip-hop, indie, etc.) and the current weekly "trend" favours certain genres. Signing artists ahead of a trend pays off. This could just be a simple rotating cycle to start.

---

### 🔵 Bigger Features (Once it's playable)

**10. A&R Scouting Screen**
Instead of a flat list of unsigned artists, make it a "scouting" action — you pay a small fee to reveal an artist's full stats before deciding to sign. Adds risk vs. reward to the signing phase.

**11. Label Reputation / Prestige**
A label-wide stat that affects which artists are willing to sign with you, how well your releases do, and what sponsorship deals you get. Rises with chart success, falls with dropped artists or poor releases.

**12. Album Campaign System**
Albums shouldn't just be "release and wait." A 4–6 week campaign with actions each week: *drop a single, do a promo run, shoot a video, book a TV slot*. Each action costs money but boosts chart performance. This would be the deepest gameplay loop.

---

### 🚀 Suggested Order of Attack

The fastest path to a genuinely playable game is:

1. Artist stats (random generation) — feeds everything else
2. A visible Top 10 chart with dummy AI entries
3. Win/lose condition (go broke = game over, reach $X = season win)
4. Weekly events feed
5. Rival labels (even just cosmetic at first)

That's probably 5–8 Cline sessions and you'd have something you could actually share with someone to play. The chart is the emotional core of the game — once people can see their release climb it, they're hooked.

---

One thing worth noting: since this is Flask + HTML templates, you might want to consider migrating the front-end to something more reactive (even just vanilla JS with fetch calls to your Flask API) so the UI can update without full page reloads. That'll make the weekly progression feel much smoother. It's a medium lift but would really elevate the feel of the game.