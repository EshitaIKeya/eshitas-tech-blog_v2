import { useState } from "react";

function ShareButtons({ title }) {
  const [copied, setCopied] = useState(false);

  // Get the current page URL
  const url = window.location.href;

  function copyLink() {
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const twitterUrl = "https://twitter.com/intent/tweet?text=" +
    encodeURIComponent(title) + "&url=" + encodeURIComponent(url);

  const linkedinUrl = "https://www.linkedin.com/sharing/share-offsite/?url=" +
    encodeURIComponent(url);

  return (
    <div className="share-buttons">
      <span className="share-label">Share:</span>
      <button onClick={copyLink} className="share-btn">
        {copied ? "Copied!" : "Copy link"}
      </button>
      <a href={twitterUrl} target="_blank" rel="noopener noreferrer" className="share-btn">
        X / Twitter
      </a>
      <a href={linkedinUrl} target="_blank" rel="noopener noreferrer" className="share-btn">
        LinkedIn
      </a>
    </div>
  );
}

export default ShareButtons;
