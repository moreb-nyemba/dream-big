import { useState } from "react";
import "./MemeStudio.css";

const SAMPLE_TEMPLATES = [
  { url: "https://i.imgflip.com/1ur9b0.jpg", name: "Distracted Boyfriend" },
  { url: "https://i.imgflip.com/30b1gx.jpg", name: "Drake Hotline Bling" },
  { url: "https://i.imgflip.com/4t0m5.jpg", name: "Doge" },
  { url: "https://i.imgflip.com/2kbn1e.jpg", name: "Surprised Pikachu" },
  { url: "https://i.imgflip.com/1otk96.jpg", name: "Mocking SpongeBob" },
  { url: "https://i.imgflip.com/3cimak.jpg", name: "Woman Yelling at Cat" },
  { url: "https://i.imgflip.com/3lmzyx.jpg", name: "UNO Draw 25" },
  { url: "https://i.imgflip.com/1yxkcp.jpg", name: "Expanding Brain" },
  { url: "https://i.imgflip.com/1bhk.jpg", name: "Success Kid" },
  { url: "https://i.imgflip.com/1o00in.jpg", name: "Is This a Pigeon?" },
  { url: "https://i.imgflip.com/3oevdk.jpg", name: "Bernie Once Again" },
  { url: "https://i.imgflip.com/39t1o.jpg", name: "Leonardo Cheers" },
];

function MemeStudio() {
  const [selectedTemplate, setSelectedTemplate] = useState(SAMPLE_TEMPLATES[0]);
  const [topText, setTopText] = useState("");
  const [bottomText, setBottomText] = useState("");
  const [generatedUrl, setGeneratedUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState("");

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(""), 2000);
  };

  const handleGenerate = async () => {
    if (!selectedTemplate) return;
    setLoading(true);
    try {
      const resp = await fetch("/api/memes/generate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          image_url: selectedTemplate.url,
          top_text: topText,
          bottom_text: bottomText,
        }),
      });
      if (!resp.ok) throw new Error("Generation failed");
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      setGeneratedUrl(url);
      showToast("Meme generated!");
    } catch {
      showToast("Failed to generate meme. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleSticker = async () => {
    if (!selectedTemplate) return;
    setLoading(true);
    try {
      const resp = await fetch("/api/memes/sticker/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          image_url: selectedTemplate.url,
          top_text: topText,
          bottom_text: bottomText,
        }),
      });
      if (!resp.ok) throw new Error("Sticker creation failed");
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "sticker.webp";
      a.click();
      URL.revokeObjectURL(url);
      showToast("WhatsApp sticker downloaded!");
    } catch {
      showToast("Failed to create sticker. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!generatedUrl) return;
    const a = document.createElement("a");
    a.href = generatedUrl;
    a.download = "meme.png";
    a.click();
  };

  return (
    <section className="studio">
      <div className="studio__header">
        <p className="pill pill--soft">🎨 Meme Studio</p>
        <h2>Create your meme</h2>
        <p className="lede">
          Pick a template, add your text, and generate a meme or WhatsApp sticker powered by the
          Django + Pillow backend.
        </p>
      </div>

      <div className="studio__layout">
        {/* Template picker */}
        <div className="studio__templates">
          <h3>Choose a template</h3>
          <div className="template-grid">
            {SAMPLE_TEMPLATES.map((t) => (
              <button
                key={t.url}
                className={`template-thumb ${selectedTemplate?.url === t.url ? "template-thumb--active" : ""}`}
                onClick={() => setSelectedTemplate(t)}
                title={t.name}
              >
                <img src={t.url} alt={t.name} loading="lazy" />
              </button>
            ))}
          </div>
        </div>

        {/* Controls */}
        <div className="studio__controls">
          <h3>Add text</h3>
          <div className="studio__field">
            <label htmlFor="top-text">Top text</label>
            <input
              id="top-text"
              type="text"
              placeholder="e.g. WHEN YOU FINALLY…"
              value={topText}
              onChange={(e) => setTopText(e.target.value)}
              maxLength={300}
            />
          </div>
          <div className="studio__field">
            <label htmlFor="bottom-text">Bottom text</label>
            <input
              id="bottom-text"
              type="text"
              placeholder="e.g. …DEPLOY ON FRIDAY"
              value={bottomText}
              onChange={(e) => setBottomText(e.target.value)}
              maxLength={300}
            />
          </div>
          <div className="studio__actions">
            <button className="button primary" onClick={handleGenerate} disabled={loading}>
              {loading ? "⏳ Processing…" : "🖼️ Generate Meme"}
            </button>
            <button className="button ghost" onClick={handleSticker} disabled={loading}>
              📱 WhatsApp Sticker
            </button>
          </div>
        </div>

        {/* Preview */}
        <div className="studio__preview">
          <h3>Preview</h3>
          <div className="preview-frame">
            {generatedUrl ? (
              <img src={generatedUrl} alt="Generated meme" />
            ) : selectedTemplate ? (
              <div className="preview-placeholder">
                <img src={selectedTemplate.url} alt={selectedTemplate.name} />
                <div className="preview-overlay">
                  {topText && <span className="preview-text preview-text--top">{topText.toUpperCase()}</span>}
                  {bottomText && <span className="preview-text preview-text--bottom">{bottomText.toUpperCase()}</span>}
                </div>
              </div>
            ) : (
              <p className="preview-empty">Select a template to begin</p>
            )}
          </div>
          {generatedUrl && (
            <button className="button primary" onClick={handleDownload}>
              ⬇️ Download Meme
            </button>
          )}
        </div>
      </div>

      {toast && <div className="toast">{toast}</div>}
    </section>
  );
}

export default MemeStudio;
