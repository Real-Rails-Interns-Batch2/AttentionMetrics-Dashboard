"use client";

import { useState, useEffect, useMemo } from "react";
import styles from "./page.module.css";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://attention-metrics-api.onrender.com";

export type Platform = {
  id: number;
  user: string;
  status: string;
  is_synthetic: boolean;
  dau: number;
  session: number;
  adLoad: number;
  cpm: number;
  creatorSplit: number;
  color: string;
};

export default function AttentionEconomyDashboard() {
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/platforms`);
        const data = await res.json();
        setPlatforms(data);
        if (data.length > 0) setSelectedId(data[0].id);
      } catch (err) {
        console.error("Error loading data:", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const activePlatform = useMemo(() => platforms.find((p) => p.id === selectedId), [platforms, selectedId]);

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className={styles.root}>
      <h1>Attention Economy Simulator</h1>
      <select value={selectedId || ""} onChange={(e) => setSelectedId(Number(e.target.value))}>
        {platforms.map((p) => <option key={p.id} value={p.id}>{p.user}</option>)}
      </select>
      {activePlatform && (
        <section>
          <h2>{activePlatform.user}</h2>
          <p>Status: {activePlatform.status}</p>
          <p>DAU: {activePlatform.dau}</p>
        </section>
      )}
    </div>
  );
}
