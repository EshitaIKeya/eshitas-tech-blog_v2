function Contact() {
  return (
    <div className="contact-page">
      <h1>Get in Touch</h1>
      <div className="contact-grid">
        <a href="mailto:eshita.isk@gmail.com" className="contact-card">
          <span className="contact-icon">&#9993;</span>
          <h3>Email</h3>
          <p>eshita.isk@gmail.com</p>
        </a>
        <a href="https://www.linkedin.com/in/eshita-islam-keya-5504b230a/" target="_blank" rel="noopener noreferrer" className="contact-card">
          <span className="contact-icon">in</span>
          <h3>LinkedIn</h3>
          <p>Eshita Islam Keya</p>
        </a>
        <a href="https://github.com/EshitaIKeya" target="_blank" rel="noopener noreferrer" className="contact-card">
          <span className="contact-icon">&lt;/&gt;</span>
          <h3>GitHub</h3>
          <p>EshitaIKeya</p>
        </a>
      </div>
    </div>
  );
}

export default Contact;
