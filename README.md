# screen-warriorsimport { Link } from "react-router-dom";
import "../styles/home.css";

function Home() {
  return (
    <div className="home">

      {/* Hero Section */}
      <section className="hero">
        <h1>🧠 ResearchPilot</h1>
        <p>
          Autonomous Research Intelligence Hub powered by AI agents.
          Discover, analyze, and synthesize knowledge instantly.
        </p>

        <div className="hero-buttons">
          <Link to="/research">
            <button className="primary-btn">Start Research</button>
          </Link>
          <button className="secondary-btn">Learn More</button>
        </div>
      </section>

      {/* Features */}
      <section className="features">
        <h2>Why ResearchPilot?</h2>

        <div className="feature-grid">
          <div className="feature-card">
            <h3>🤖 Autonomous AI Agents</h3>
            <p>Multi-step reasoning agents that conduct deep research automatically.</p>
          </div>

          <div className="feature-card">
            <h3>🌐 Web Intelligence</h3>
            <p>Collects data from multiple sources and synthesizes insights.</p>
          </div>

          <div className="feature-card">
            <h3>📊 Structured Insights</h3>
            <p>Summaries, key insights, and sources organized in one dashboard.</p>
          </div>

          <div className="feature-card">
            <h3>⚡ Fast & Scalable</h3>
            <p>Built for researchers, analysts, and enterprises.</p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works">
        <h2>How It Works</h2>

        <div className="steps">
          <div className="step">
            <h3>1️⃣ Enter Topic</h3>
            <p>Provide a research question or subject.</p>
          </div>

          <div className="step">
            <h3>2️⃣ AI Analysis</h3>
            <p>Autonomous agents gather, analyze, and synthesize information.</p>
          </div>

          <div className="step">
            <h3>3️⃣ Get Insights</h3>
            <p>Receive structured reports with summaries and sources.</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta">
        <h2>Ready to Supercharge Your Research?</h2>
        <Link to="/research">
          <button className="primary-btn">Launch Research Hub</button>
        </Link>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>© 2026 ResearchPilot AI • Autonomous Intelligence Platform</p>
      </footer>

    </div>
  );
}

export default Home;
