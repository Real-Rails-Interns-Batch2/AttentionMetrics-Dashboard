"use client";
import { useState, useEffect } from "react";
import styles from "./page.module.css";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://attention-metrics-api.onrender.com";

export default function Dashboard() {
  const [platforms, setPlatforms] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/platforms`)
      .then(res => res.json())
      .then(data => setPlatforms(data))
      .catch(err => console.error("Data fetch error:", err));
  }, []);

  return (
    <div className={styles.root}>
      <h1>Attention Economy Revenue Simulator</h1>
      <div className={styles.kpiGrid}>
        {platforms.map((p) => (
          <div key={p.id} className={styles.card} style={{ borderLeft: `4px solid ${p.color}` }}>
            <h3>{p.icon} {p.name}</h3>
            <p>Category: {p.category}</p>
            <p>Daily Revenue: ${(((p.dau * 1_000_000 * p.session) / 60 * p.adLoad / 1000) * p.cpm / 1_000_000).toFixed(1)}M</p>
          </div>
        ))}
      </div>
    </div>
  );
}
