# MoviePicker AI/ML Pivot — Brainstorm Resume Notes

**Status:** Brainstorm paused mid-Section 5 (roadmap), awaiting user approval to write the formal design doc.
**Paused:** 2026-05-04
**Resume protocol:** approve Section 5 → write design spec to `docs/superpowers/specs/2026-05-04-moviepicker-aiml-design.md` → user reviews → invoke `superpowers:writing-plans` for v3.0 implementation plan.

---

## Path locked: Path B (staged release)

- **v3.0** = content-based recommender on Jellyfin catalog (this weekend's target)
- **v3.1** = MovieLens 25M collaborative-filtering model + hybrid serving (separate brainstorm later)

Path A (replace v3.0 entirely with MovieLens-trained CF) was considered and rejected to avoid schedule risk pre-internship-deadline.

---

## v3.0 design decisions (Sections 1-4 approved)

### Scope

**Ships in v3.0:**
1. Jellyfin export script (one-shot dump of 851-movie catalog + per-movie watch signal to normalized JSON)
2. Three recommenders behind a shared protocol, selectable at call time:
   - Existing rule-based engine (kept as Baseline 0, wrapped in protocol unchanged)
   - New TF-IDF recommender (Baseline 1, sklearn)
   - New sentence-transformer recommender (Production, `all-MiniLM-L6-v2`)
3. Eval harness: P@10, HR@10, NDCG@10, MRR — 5 random seeds, mean ± std
4. CLI integration via `--strategy {rule,tfidf,embed,all}` flag on existing `recommend` command
5. README rewrite framing project as ML portfolio piece, plus auto-generated `EVAL.md`

**Explicitly deferred** to v3.1+:
- Live Jellyfin sync (one-shot export only for v3.0)
- Plex adapter
- Letterboxd CSV import
- React frontend changes
- LLM/RAG layer
- Multi-user support

### Architecture seam

Single `RecommenderProtocol`:

```python
class RecommenderProtocol(Protocol):
    name: str  # "rule" | "tfidf" | "embed"

    def fit(self, db: Session) -> None: ...

    def recommend(
        self,
        user_id: int,
        k: int = 10,
        exclude_watched: bool = True,
    ) -> list[Recommendation]: ...

@dataclass
class Recommendation:
    movie_id: int
    score: float       # normalized to [0, 1] for cross-recommender comparability
    reason: str
```

### Data pipeline (3 stages)

1. `scripts/export_jellyfin.py` — paginated Jellyfin `/Items` dump → `data/catalog/jellyfin-{YYYY-MM-DD}.json` + `latest.json` symlink. Credentials read from `~/.config/moviepicker/.env` (gitignored, outside repo). ~80 LOC.
2. `src/core/ingest.py` — JSON → SQLAlchemy upsert. Idempotent. Returns `IngestReport`. ~120 LOC.
3. `src/core/recommendation/embeddings/build.py` — generates both TF-IDF (`tfidf_matrix.npz` + `vectorizer.pkl`) and semantic (`semantic_embeddings.npy`, 851 × 384 ≈ 1.3 MB) artifacts in `data/embeddings/` (gitignored). ~60 LOC.

### Schema (confirmed against real Jellyfin response)

```json
{
  "source": "jellyfin",
  "exported_at": "2026-05-04T20:00:00Z",
  "movies": [
    {
      "title": "...",
      "year": 1957,
      "tmdb_id": 389,
      "imdb_id": "tt0050083",
      "overview": "...",
      "genres": ["Drama"],
      "director": "Sidney Lumet",
      "cast": ["Henry Fonda", "Lee J. Cobb", "..."],
      "runtime_min": 96,
      "tmdb_rating": 8.5,
      "language": "en",
      "user_data": {
        "watched": true,
        "play_count": 1,
        "is_favorite": false,
        "last_played_at": "2025-10-23T08:06:16Z",
        "user_rating": null
      }
    }
  ]
}
```

Field derivations from raw Jellyfin response:
- `tmdb_id` ← `ProviderIds.Tmdb`
- `runtime_min` ← `RunTimeTicks // 600_000_000` (Jellyfin uses 100ns ticks)
- `director` ← join of `People[Type=="Director"]`
- `cast` ← top 10 `People[Type=="Actor"]` in billing order
- `tmdb_rating` ← `CommunityRating`
- `user_data.user_rating` is null because Jellyfin doesn't expose numeric per-user ratings; favorites + play counts are the only signal

### Preference vector weighting

```python
weight = log(1 + play_count + (1.0 if is_favorite else 0.0)) * exp(-days_since_last_watched / 365)
```

- Implicit-feedback formula (Hu, Koren, Volinsky 2008) × time-decay
- Cited in README as "production-correct, but at single-user scale weighting differences are within eval noise floor — chosen because it's what production systems do, not because we measured a lift over equal weighting"

### Eval (Section 4)

**Four metrics**, all implemented by hand (no sklearn for NDCG):
- **Precision@10** — headline number, position-blind
- **Hit Rate @10** — at least one held-out item in top-10
- **NDCG@10** — position-aware (Järvelin & Kekäläinen 2002)
- **MRR** — reciprocal rank of first relevant item

**Method:**
- Held-out: 20% of liked movies (favorites + watched), 5 random seeds (42-46)
- Binary relevance (no numeric rating signal from Jellyfin)
- Reports `mean ± std` across seeds — no significance claims (small N)
- Side-by-side qualitative output via `moviepicker recommend --strategy all`

**Auto-generated `EVAL.md`** with `Honest limitations` section that names the small-N problem before a reviewer can.

---

## Roadmap (Section 5 — presented, awaiting approval)

| Release | Scope | Effort |
|---|---|---|
| v3.0 | Content-based recommender + eval (this design) | 1 weekend |
| v3.0.5 | Diversity reranking, basic filters | half-weekend |
| v3.1 | MovieLens 25M CF + hybrid serving | 2-3 weekends |
| v3.2 | Letterboxd CSV import | 1 weekend |
| v3.3 | LLM/RAG mood query layer | 1 weekend |
| v3.4 | Plex client (multi-source adapter) | half-weekend |
| v3.5 | Live Jellyfin sync | 1 weekend |
| v3.6+ | Frontend, multi-user, cold-start, hyperparameter tuning | open-ended |

Each release independently shippable. No release retroactively breaks v3.0 eval.

---

## Outstanding security item

The new Jellyfin API key (`6f9a…27cd`) is currently active and was pasted into chat during reconnaissance. **Revoke it in Jellyfin → Dashboard → API Keys before shipping.** When export script is built, credentials live in `~/.config/moviepicker/.env` (gitignored, outside repo).

---

## Resume actions for next session

1. **Approve or redirect Section 5 roadmap.**
2. **Write design doc** to `docs/superpowers/specs/2026-05-04-moviepicker-aiml-design.md` consolidating Sections 1-5.
3. **Self-review** the spec (placeholder scan, internal consistency, scope check, ambiguity check) — fix inline.
4. **User reviews the spec** — request changes or approve.
5. **Invoke `superpowers:writing-plans`** to produce v3.0 implementation plan with TDD task breakdown.

Move this file out of `_pending/` once the formal design doc exists.
