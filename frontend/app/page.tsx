'use client';

import { useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [status, setStatus] = useState('Idle');

  async function runAnalysis() {
    if (!file) {
      setStatus('Please upload a CSV file first.');
      return;
    }

    setStatus('Analyzing FTIR spectrum...');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/api/spectra/analyze`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
      setStatus(response.ok ? 'Analysis completed' : 'Analysis failed');
    } catch (error) {
      setStatus('Backend API is not connected yet.');
      setResult({ error: String(error) });
    }
  }

  return (
    <main style={{ padding: 32, fontFamily: 'Arial, sans-serif', maxWidth: 1100, margin: '0 auto' }}>
      <section style={{ marginBottom: 32 }}>
        <p style={{ textTransform: 'uppercase', letterSpacing: 2, color: '#2f6f5e' }}>
          AI-driven environmental resilience intelligence
        </p>
        <h1 style={{ fontSize: 54, margin: '8px 0' }}>SHUBAAD</h1>
        <p style={{ fontSize: 20, lineHeight: 1.6 }}>
          شُبعاد — منصة ذكاء بيئي تربط FTIR spectroscopy، GIS، مؤشرات التربة، والنمذجة التنبؤية
          لتقييم الملوحة، الكربون، والجفاف في النظم الجافة وشبه الجافة.
        </p>
      </section>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 16, marginBottom: 32 }}>
        {[
          ['Spectral Engine', 'FTIR preprocessing, peak detection, spectral zones'],
          ['GIS Engine', 'Sample coordinates, salinity layers, NDVI/LST integration'],
          ['AI Engine', 'PLS, salinity prediction, resilience scoring']
        ].map(([title, text]) => (
          <div key={title} style={{ border: '1px solid #ddd', borderRadius: 16, padding: 20 }}>
            <h2>{title}</h2>
            <p>{text}</p>
          </div>
        ))}
      </section>

      <section style={{ border: '1px solid #ddd', borderRadius: 16, padding: 24 }}>
        <h2>FTIR Dataset Upload Engine</h2>
        <p>Upload CSV with two columns: wavenumber and absorbance.</p>

        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <br /><br />

        <button
          onClick={runAnalysis}
          style={{ padding: '12px 18px', borderRadius: 10, cursor: 'pointer' }}
        >
          Run SHUBAAD FTIR Analysis
        </button>

        <p><strong>Status:</strong> {status}</p>

        {result && (
          <pre style={{ background: '#f6f6f6', padding: 16, borderRadius: 12, overflowX: 'auto' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </section>
    </main>
  );
}
