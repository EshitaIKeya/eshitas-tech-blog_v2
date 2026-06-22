import { useState, useEffect, useRef } from "react";

function ReadAloud({ content }) {
  const [playing, setPlaying] = useState(false);
  const voiceRef = useRef(null);

  // Load the female voice once, handling the browser's async voice loading
  useEffect(() => {
    function pickFemaleVoice() {
      const voices = window.speechSynthesis.getVoices();
      if (voices.length === 0) return; // not loaded yet

      const femaleVoice = voices.find((v) =>
        ["Female", "Samantha", "Zira", "Susan", "Google US English"].some(
          (name) => v.name.includes(name)
        )
      );
      voiceRef.current = femaleVoice || voices[0] || null;
    }

    pickFemaleVoice();
    // Voices may load asynchronously after the page first renders
    window.speechSynthesis.onvoiceschanged = pickFemaleVoice;

    return () => window.speechSynthesis.cancel();
  }, []);

  function stripHtml(html) {
    const div = document.createElement("div");
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
  }

  function handleToggle() {
    if (playing) {
      window.speechSynthesis.cancel();
      setPlaying(false);
    } else {
      const text = stripHtml(content);
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1.1; // slightly higher pitch reads as softer
      if (voiceRef.current) utterance.voice = voiceRef.current;
      utterance.onend = () => setPlaying(false);
      utterance.onerror = () => setPlaying(false);
      window.speechSynthesis.speak(utterance);
      setPlaying(true);
    }
  }

  return (
    <button onClick={handleToggle} className="read-aloud-btn">
      {playing ? "\u23F8 Stop reading" : "\uD83D\uDD0A Listen to this post"}
    </button>
  );
}

export default ReadAloud;