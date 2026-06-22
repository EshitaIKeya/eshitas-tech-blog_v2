function AboutMe() {
  return (
    <div className="about-page">
      <h1>About Me</h1>
      <div className="about-card">
        <div className="about-avatar">E</div>
        <div className="about-body">
          <p>
            Hi! I'm <strong>Eshita Islam</strong>, an ICE student at BUP
            and intern at Apurba Technologies Inc. I'm passionate about backend
            development, web technologies, and learning in public.
          </p>
          <p>
            I built this blog from scratch as a learning project to understand
            full-stack web development with the guidance of my teamlead Jayanto Mondel. The backend is powered by
            <strong> FastAPI</strong> with <strong>PostgreSQL</strong>, and the
            frontend uses <strong>React</strong>. Everything runs in
            <strong> Docker</strong> containers. Posts even have <strong>AI-generated
            summaries</strong> and a <strong>read-aloud</strong> feature.
          </p>
          <h3>What I write about</h3>
          <p>
            I share my journey learning programming, databases, APIs, and
            software engineering. If you're a beginner like me, I hope my
            posts help you understand things in simple terms.
          </p>
          <h3>Tech I work with</h3>
          <div className="tech-pills">
            <span className="tech-pill">Python</span>
            <span className="tech-pill">FastAPI</span>
            <span className="tech-pill">PostgreSQL</span>
            <span className="tech-pill">SQLAlchemy</span>
            <span className="tech-pill">React</span>
            <span className="tech-pill">JavaScript</span>
            <span className="tech-pill">Docker</span>
            <span className="tech-pill">Git</span>
          </div>
          <h3>Connect</h3>
          <p>
            <a href="https://www.linkedin.com/in/eshita-islam-keya-5504b230a/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            {" "}&middot;{" "}
            <a href="https://github.com/EshitaIKeya" target="_blank" rel="noopener noreferrer">GitHub</a>
            {" "}&middot;{" "}
            <a href="mailto:eshita.isk@gmail.com">Email</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default AboutMe;
