"use client";

import { useState } from "react";
import styles from "./page.module.css";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";

export default function Log() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  return (
    <div className={styles.LogContainer}>
      <div className={styles.LeftBox} />
      <div className={styles.LogLeft}>
        <h1>Witaj w Dronder</h1>
        <p>Pierwszy raz w naszym serwisie?</p>
        <Button
          className={styles.LeftButton}
          variant="outlined"
          sx={{ textTransform: "none !important" }}
        >
          Zarejestruj się!
        </Button>
      </div>
      <div className={styles.LogRight}>
        <img
          className={styles.appLogo}
          src="/dronder_logo.png"
          alt="App logo"
        />
        <TextField
          className={styles.Input}
          id="outlined-basic"
          label="login"
          variant="outlined"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          className={styles.Input}
          id="outlined-basic"
          label="hasło"
          type="password"
          variant="outlined"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && (
          <div className={styles.errorMessage}>
            <p>{error}</p>
          </div>
        )}
        <Button
          className={styles.RightButton}
          sx={{ textTransform: "none !important" }}
        >
          Zaloguj
        </Button>
      </div>
    </div>
  );
}
