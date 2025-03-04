import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

import { ThemeProvider } from "@material-tailwind/react";

const theme = {
  colors: {
    primary: "#1E40AF",
    secondary: "#DBEAFE",
    accent: "#3B82F6",
    background: "#F3F4F6",
    text: "#1F2937",
  },
  fontFamily: {
    sans: ["Inter", "sans-serif"],
    serif: ["Merriweather", "serif"],
  },
  spacing: {
    72: "18rem",
    84: "21rem",
    96: "24rem",
  },
};

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <ThemeProvider value={theme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
