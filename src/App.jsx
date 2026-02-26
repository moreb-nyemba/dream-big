import { useMemo, useState } from "react";
import { memes } from "./data/memes";
import "./App.css";

const vibes = [
  { id: "all", label: "All vibes" },
  { id: "wholesome", label: "Wholesome" },
  { id: "chaotic", label: "Chaotic" },
  { id: "savage", label: "Savage" },
  { id: "classic", label: "Classics" },
];

function MemeCard({ meme, onCopy, isSpotlight }) {
  return (
    <article className={`meme-card ${isSpotlight ? "meme-card--spotlight" : ""}`}>
      <div className="meme-card__media">
        <img src={meme.image} alt={meme.alt} loading="lazy" />
        {isSpotlight && <span className="pill pill--spotlight">Spotlight</span>}
        {meme.vibe && <span className="pill pill--vibe">{meme.vibe}</span>}
      </div>
      <div className="meme-card__body">
        <div className="meme-card__header">
          <div>
            <p className="eyebrow">Since {meme.year}</p>
            <h3>{meme.title}</h3>
          </div>
          <span className="score">🔥 {meme.score}</span>
        </div>
        <p className="description">{meme.description}</p>
        <div className="tags">
          {meme.tags.map((tag) => (
            <span key={tag} className="tag">
              #{tag}
            </span>
          ))}
        </div>
        <div className="card-actions">
          <a className="button ghost" href={meme.source} target="_blank" rel="noreferrer">
            Open source
          </a>
          <button className="button primary" onClick={() => onCopy(meme)}>
            Copy image link
          </button>
        </div>
      </div>
    </article>
  );
}

function App() {
  const [query, setQuery] = useState("");
  const [vibeFilter, setVibeFilter] = useState("all");
  const [spotlight, setSpotlight] = useState(memes[0]);
  const [toast, setToast] = useState("");

  const filtered = useMemo(() => {
    return memes.filter((meme) => {
      const matchesQuery =
        meme.title.toLowerCase().includes(query.toLowerCase()) ||
        meme.tags.some((tag) => tag.toLowerCase().includes(query.toLowerCase()));
      const matchesVibe =
        vibeFilter === "all" ||
        (vibeFilter === "classic" ? meme.classic : meme.vibe === vibeFilter);
      return matchesQuery && matchesVibe;
    });
  }, [query, vibeFilter]);

  const ordered = useMemo(() => {
    const withoutSpotlight = filtered.filter((meme) => meme.title !== spotlight.title);
    return [spotlight, ...withoutSpotlight];
  }, [filtered, spotlight]);

  const stats = useMemo(() => {
    const vibesSet = new Set(memes.map((m) => m.vibe));
    return {
      total: memes.length,
      vibes: vibesSet.size,
      classics: memes.filter((m) => m.classic).length,
    };
  }, []);

  const surprise = () => {
    const pool = filtered.length ? filtered : memes;
    const random = pool[Math.floor(Math.random() * pool.length)];
    setSpotlight(random);
    setToast(`Brought ${random.title} back to the stage.`);
    setTimeout(() => setToast(""), 1800);
  };

  const copyLink = async (meme) => {
    try {
      await navigator.clipboard.writeText(meme.image);
      setToast("Copied! Drop it in your chat.");
    } catch (error) {
      console.error("Copy failed", error);
      setToast("Clipboard blocked. Try opening the source.");
    } finally {
      setTimeout(() => setToast(""), 1600);
    }
  };

  return (
    <main className="page">
      <header className="hero">
        <p className="pill pill--soft">Dream Big · Meme lab</p>
        <div className="hero__title">
          <h1>Build the perfect meme drop</h1>
          <p className="lede">
            A modern, lightweight meme repository with curated classics, chaotic bangers, and
            wholesome vibes ready to remix.
          </p>
        </div>
        <div className="hero__controls">
          <div className="input">
            <span>🔍</span>
            <input
              type="search"
              placeholder="Search by title or tag…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          <div className="vibes">
            {vibes.map((v) => (
              <button
                key={v.id}
                className={`chip ${vibeFilter === v.id ? "chip--active" : ""}`}
                onClick={() => setVibeFilter(v.id)}
              >
                {v.label}
              </button>
            ))}
          </div>
          <div className="hero__actions">
            <button className="button primary" onClick={surprise}>
              🔀 Surprise me
            </button>
            <button className="button ghost" onClick={() => setVibeFilter("wholesome")}>
              🌈 Wholesome only
            </button>
          </div>
        </div>
        <div className="hero__stats">
          <div>
            <p className="eyebrow">Memes curated</p>
            <strong>{stats.total}</strong>
          </div>
          <div>
            <p className="eyebrow">Vibe buckets</p>
            <strong>{stats.vibes}</strong>
          </div>
          <div>
            <p className="eyebrow">Certified classics</p>
            <strong>{stats.classics}</strong>
          </div>
        </div>
      </header>

      <section className="grid" aria-live="polite">
        {ordered.map((meme, index) => (
          <MemeCard key={meme.title + index} meme={meme} onCopy={copyLink} isSpotlight={index === 0} />
        ))}
        {!ordered.length && (
          <div className="empty">
            <p>No memes found. Try resetting your filters.</p>
            <button className="button primary" onClick={() => setVibeFilter("all")}>
              Reset filters
            </button>
          </div>
        )}
      </section>

      {toast && <div className="toast">{toast}</div>}
    </main>
  );
}

export default App;
