import { useState, useEffect } from "react";

function ThemeToggle() {
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "light");

  useEffect(() => {
    document.body.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  function cycleTheme() {
    const themes = ["light", "dark", "eyecare"];
    const next = (themes.indexOf(theme) + 1) % themes.length;
    setTheme(themes[next]);
  }

  const icons = { light: "\u2600\uFE0F", dark: "\uD83C\uDF19", eyecare: "\uD83D\uDCD6" };

  return (
    <button onClick={cycleTheme} className="theme-btn" title={"Theme: " + theme}>
      {icons[theme] || "\u2600\uFE0F"}
    </button>
  );
}

export default ThemeToggle;