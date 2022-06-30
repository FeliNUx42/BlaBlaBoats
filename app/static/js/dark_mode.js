var darkMode = false;
const KEY = "color-scheme";
const darkModeBtn = document.querySelector("input#dark-mode-switch");


darkModeBtn.addEventListener("click", toggleThemeMode);

if (mode = localStorage.getItem(KEY)) {
  darkMode = (mode == "dark-mode");
} else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
  darkMode = true;
}

if (darkMode) document.body.classList.add("dark-mode");
darkModeBtn.checked = darkMode;

function toggleThemeMode() {
  darkMode = !darkMode;
  localStorage.setItem(KEY, darkMode ? "dark-mode" : "light-mode");
  document.body.classList.toggle("dark-mode");
}