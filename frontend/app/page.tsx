"use client";

import { useState, useEffect, useMemo } from "react";
import styles from "./page.module.css";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// പുതിയ ഡാറ്റാ സ്ട്രക്ചറിന് അനുസരിച്ചുള്ള ടൈപ്പ്
export type Platform = {
  id: number;
  user: string;
  status: string;
  is_synthetic: boolean;
  // പഴയ ഫീൽഡുകൾ നിലനിർത്തി (data.json-ൽ ഇത് ഉണ്ടെന്ന് ഉറപ്പാക്കുക)
  dau?: number;
  session?: number;
  adLoad?: number;
  cpm?: number;
  creatorSplit?: number;
};

export default function AttentionEconomyDashboard() {
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Simulation states
  const [simDau, setSimDau] = useState(0);
  const [simSession, setSimSession] = useState(0);
  const [simAdLoad, setSimAdLoad] = useState(0);
  const [simCpm, setSimCpm] = useState(0);
  const [creatorSplitOverride, setCreatorSplitOverride] = useState(0);

  const activePlatform = useMemo(
    () => platforms.find((p) => p.id === selectedId) || platforms[0],
    [platforms, selectedId]
  );

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      try {
        const res = await fetch(`${API_BASE_URL}/api/platforms`);
        const data = await res.json();
        setPlatforms(data);
        if (data.length > 0) setSelectedId(data[0].id);
      } catch (err) {
        setError("Error loading data.");
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  useEffect(() => {
    if (activePlatform) {
      setSimDau(activePlatform.dau || 100);
      setSimSession(activePlatform.session || 30);
      setSimAdLoad(activePlatform.adLoad || 5);
      setSimCpm(activePlatform.cpm || 10);
      setCreatorSplitOverride(activePlatform.creatorSplit || 50);
    }
  }, [activePlatform]);

  const stats = useMemo(() => {
    const totalHours = (simDau * 1_000_000 * simSession) / 60;
    const totalImpressions = totalHours * simAdLoad;
    const simDailyRev = (totalImpressions / 1000) * simCpm;
    const simCreatorRev = simDailyRev * (creatorSplitOverride / 100);
    return {
      simDailyRev,
      simCreatorRev,
      simPlatformNet: simDailyRev - simCreatorRev,
    };
  }, [simDau, simSession, simAdLoad, simCpm, creatorSplitOverride]);

  if (isLoading) return <div className={styles.center}>Loading dashboard...</div>;
  if (error) return <div className={styles.center}>{error}</div>;

  return (
    <div className={styles.root}>
      <h1>Attention Economy Simulator</h1>

      <section className={styles.controls}>
        <label>Select User/Platform:</label>
        <select value={selectedId || ""} onChange={(e) => setSelectedId(Number(e.target.value))}>
          {platforms.map((p) => (
            <option key={p.id} value={p.id}>{p.user}</option>
          ))}
        </select>
      </section>

      <section className={styles.kpiGrid}>
        <div className={styles.card}>
          <h3>Daily Revenue</h3>
          <p>${(stats.simDailyRev / 1e6).toFixed(1)}M</p>
        </div>
        <div className={styles.card}>
          <h3>Platform Net</h3>
          <p>${(stats.simPlatformNet / 1e6).toFixed(1)}M</p>
        </div>
      </section>

      <section className={styles.sliders}>
        <div>
          <label>DAU (Millions): {simDau}</label>
          <input type="range" min="1" max="500" value={simDau} onChange={(e) => setSimDau(Number(e.target.value))} />
        </div>
        <div>
          <label>Session (mins): {simSession}</label>
          <input type="range" min="1" max="120" value={simSession} onChange={(e) => setSimSession(Number(e.target.value))} />
        </div>
      </section>
    </div>
  );
}
