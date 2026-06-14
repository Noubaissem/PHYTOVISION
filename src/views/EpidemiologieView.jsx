import { useMemo, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Icon from '../components/Icon';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell
} from 'recharts';

const ZONE_DATA = [
  { zone: "Adamaoua", total: 20, virusStrie: 6, brulure: 5, tacheGrise: 5, sain: 4, position: "left-[52%] top-[38%]" },
  { zone: "Centre", total: 47, virusStrie: 18, brulure: 15, tacheGrise: 10, sain: 4, position: "left-[47%] top-[58%]" },
  { zone: "Est", total: 18, virusStrie: 5, brulure: 4, tacheGrise: 5, sain: 4, position: "left-[68%] top-[62%]" },
  { zone: "Extreme-Nord", total: 24, virusStrie: 7, brulure: 6, tacheGrise: 8, sain: 3, position: "left-[64%] top-[12%]" },
  { zone: "Littoral", total: 29, virusStrie: 9, brulure: 10, tacheGrise: 6, sain: 4, position: "left-[33%] top-[69%]" },
  { zone: "Nord", total: 31, virusStrie: 10, brulure: 8, tacheGrise: 9, sain: 4, position: "left-[58%] top-[26%]" },
  { zone: "Nord-Ouest", total: 27, virusStrie: 8, brulure: 9, tacheGrise: 6, sain: 4, position: "left-[25%] top-[47%]" },
  { zone: "Ouest", total: 38, virusStrie: 12, brulure: 14, tacheGrise: 8, sain: 4, position: "left-[31%] top-[56%]" },
  { zone: "Sud", total: 16, virusStrie: 4, brulure: 4, tacheGrise: 3, sain: 5, position: "left-[49%] top-[79%]" },
  { zone: "Sud-Ouest", total: 22, virusStrie: 7, brulure: 8, tacheGrise: 4, sain: 3, position: "left-[23%] top-[72%]" },
];

const ALERT_DATA = [
  { zone: "Adamaoua", maladie: "Virus de la Strie", cas: 6, niveau: "Modere" },
  { zone: "Centre", maladie: "Virus de la Strie", cas: 18, niveau: "Critique" },
  { zone: "Est", maladie: "Virus de la Strie", cas: 5, niveau: "Modere" },
  { zone: "Extreme-Nord", maladie: "Virus de la Strie", cas: 7, niveau: "Modere" },
  { zone: "Littoral", maladie: "Brulure Foliaire", cas: 10, niveau: "Eleve" },
  { zone: "Nord", maladie: "Tache Grise", cas: 9, niveau: "Eleve" },
  { zone: "Nord-Ouest", maladie: "Brulure Foliaire", cas: 9, niveau: "Eleve" },
  { zone: "Ouest", maladie: "Brulure Foliaire", cas: 14, niveau: "Eleve" },
  { zone: "Sud", maladie: "Virus de la Strie", cas: 4, niveau: "Faible" },
  { zone: "Sud-Ouest", maladie: "Brulure Foliaire", cas: 8, niveau: "Modere" },
];

const DISEASE_COLORS = {
  virusStrie: "#DC2626",
  brulure: "#D97706",
  tacheGrise: "#2563EB",
  sain: "#15803D",
};

function getRisk(total) {
  if (total > 40) return { label: "Critique", className: "bg-red-50 text-danger border-danger/20", dot: "bg-danger" };
  if (total > 25) return { label: "Eleve", className: "bg-amber-50 text-warning border-warning/20", dot: "bg-warning" };
  if (total > 10) return { label: "Modere", className: "bg-blue-50 text-info border-info/20", dot: "bg-info" };
  return { label: "Faible", className: "bg-primary/5 text-primary border-primary/20", dot: "bg-primary" };
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-card border border-border rounded-2xl p-3 text-xs shadow-lg">
      <p className="text-ink font-semibold mb-2">{label}</p>
      {payload.map(p => (
        <div key={p.name} className="flex items-center justify-between gap-4">
          <span style={{ color: p.color }}>{p.name}</span>
          <span className="text-ink font-semibold">{p.value}</span>
        </div>
      ))}
    </div>
  );
}

function MetricCard({ label, value, sub, icon, color = "text-ink" }) {
  return (
    <div className="bg-card border border-border rounded-2xl p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs text-sub uppercase tracking-wide mb-1">{label}</p>
          <p className={`text-2xl font-semibold ${color}`}>{value}</p>
          <p className="text-xs text-sub mt-1">{sub}</p>
        </div>
        <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
          <Icon name={icon} className="w-5 h-5" />
        </span>
      </div>
    </div>
  );
}

function ZoneCard({ zone, total, virusStrie, brulure, tacheGrise, sain, selected, onSelect }) {
  const risk = getRisk(total);
  const maxVal = Math.max(virusStrie, brulure, tacheGrise, sain);

  return (
    <button
      onClick={onSelect}
      className={`text-left bg-card border rounded-2xl p-4 shadow-sm hover:shadow-md transition-all ${
        selected ? "border-primary ring-4 ring-primary/10" : "border-border"
      }`}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
            <Icon name="pin" className="w-5 h-5" />
          </span>
          <div>
            <h3 className="text-sm font-semibold text-ink">{zone}</h3>
            <p className="text-xs text-sub mt-0.5">{total} cas detectes</p>
          </div>
        </div>
        <span className={`text-xs px-2.5 py-1 rounded-full font-semibold border ${risk.className}`}>
          {risk.label}
        </span>
      </div>

      <div className="flex flex-col gap-2.5">
        {[
          { label: "Virus Strie", val: virusStrie, color: "bg-danger" },
          { label: "Brulure", val: brulure, color: "bg-warning" },
          { label: "Tache Grise", val: tacheGrise, color: "bg-info" },
          { label: "Sain", val: sain, color: "bg-primary" },
        ].map(d => (
          <div key={d.label}>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-sub">{d.label}</span>
              <span className="text-ink font-medium">{d.val}</span>
            </div>
            <div className="h-2 bg-border rounded-full">
              <div
                className={`h-full rounded-full ${d.color}`}
                style={{ width: `${(d.val / maxVal) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </button>
  );
}

function MapPanel({ zones, selectedZone, onSelect }) {
  return (
    <div className="bg-card border border-border rounded-2xl p-5 shadow-sm min-h-[420px]">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-base font-semibold text-ink">Carte de surveillance</h2>
          <p className="text-xs text-sub mt-1">Vue schematique des foyers suivis.</p>
        </div>
        <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
          <Icon name="map" className="w-5 h-5" />
        </span>
      </div>

      <div className="relative h-[330px] overflow-hidden rounded-2xl bg-primary/5 border border-primary/10">
        <div className="absolute inset-x-[18%] top-5 bottom-5 rounded-[45%] border-2 border-primary/20 bg-white/70 shadow-inner" />
        <div className="absolute left-[38%] top-[8%] h-[84%] w-px bg-primary/10" />
        <div className="absolute left-[18%] right-[18%] top-[50%] h-px bg-primary/10" />

        {zones.map(zone => {
          const risk = getRisk(zone.total);
          const active = selectedZone === "Toutes" || selectedZone === zone.zone;
          return (
            <button
              key={zone.zone}
              onClick={() => onSelect(zone.zone)}
              className={`absolute -translate-x-1/2 -translate-y-1/2 ${zone.position} transition-all ${
                active ? "opacity-100 scale-100" : "opacity-40 scale-95"
              }`}
            >
              <span className={`block w-4 h-4 rounded-full ${risk.dot} ring-4 ring-white shadow-md`} />
              <span className="mt-2 block bg-white border border-border rounded-xl px-2 py-1 text-[11px] font-semibold text-ink shadow-sm whitespace-nowrap">
                {zone.zone}
              </span>
            </button>
          );
        })}

        <div className="absolute bottom-4 left-4 right-4 bg-white/90 border border-border rounded-2xl p-3 shadow-sm">
          <p className="text-xs font-semibold text-ink">Lecture rapide</p>
          <div className="grid grid-cols-2 gap-2 mt-2 text-[11px] text-sub">
            {["Critique", "Eleve", "Modere", "Faible"].map(label => {
              const color = {
                Critique: "bg-danger",
                Eleve: "bg-warning",
                Modere: "bg-info",
                Faible: "bg-primary",
              }[label];
              return (
                <span key={label} className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${color}`} />
                  {label}
                </span>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

function EpidemiologieView() {
  const [selectedZone, setSelectedZone] = useState("Toutes");
  const zoneOptions = ["Toutes", ...ZONE_DATA.map(zone => zone.zone)];

  const filteredZones = selectedZone === "Toutes"
    ? ZONE_DATA
    : ZONE_DATA.filter(z => z.zone === selectedZone);

  const filteredAlerts = selectedZone === "Toutes"
    ? ALERT_DATA
    : ALERT_DATA.filter(row => row.zone === selectedZone);

  const totals = useMemo(() => {
    const totalCas = ZONE_DATA.reduce((s, z) => s + z.total, 0);
    const totalSains = ZONE_DATA.reduce((s, z) => s + z.sain, 0);
    const zoneAlerte = ZONE_DATA.reduce((a, b) => a.total > b.total ? a : b);
    const diseaseMix = [
      { name: "Virus Strie", value: ZONE_DATA.reduce((s, z) => s + z.virusStrie, 0), color: DISEASE_COLORS.virusStrie },
      { name: "Brulure", value: ZONE_DATA.reduce((s, z) => s + z.brulure, 0), color: DISEASE_COLORS.brulure },
      { name: "Tache Grise", value: ZONE_DATA.reduce((s, z) => s + z.tacheGrise, 0), color: DISEASE_COLORS.tacheGrise },
      { name: "Sain", value: totalSains, color: DISEASE_COLORS.sain },
    ];

    return { totalCas, totalSains, zoneAlerte, diseaseMix };
  }, []);

  return (
    <div className="flex min-h-screen bg-bg">
      <Sidebar />

      <main className="flex-1 flex flex-col min-w-0">
        <header className="bg-card/95 border-b border-border px-6 py-4 flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4 shadow-sm">
          <div>
            <h1 className="text-xl font-semibold text-ink">Suivi Epidemiologique</h1>
            <p className="text-sm text-sub mt-1">Surveillance territoriale, priorites IRAD et evolution des foyers.</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs text-sub mr-1">Zone:</span>
            {zoneOptions.map(z => (
              <button
                key={z}
                onClick={() => setSelectedZone(z)}
                className={`text-xs px-3 py-2 rounded-xl border transition-colors ${
                  selectedZone === z
                    ? "bg-primary text-white border-primary shadow-sm shadow-primary/20"
                    : "bg-card border-border text-sub hover:border-primary/40 hover:text-primary"
                }`}
              >
                {z}
              </button>
            ))}
          </div>
        </header>

        <div className="flex-1 p-5 lg:p-6 flex flex-col gap-5">
          <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            <MetricCard label="Pression totale" value={totals.totalCas} color="text-danger" icon="shield" sub="cas detectes toutes zones" />
            <MetricCard label="Zone critique" value={totals.zoneAlerte.zone} color="text-warning" icon="pin" sub={`${totals.zoneAlerte.total} cas a prioriser`} />
            <MetricCard label="Feuilles saines" value={totals.totalSains} color="text-primary" icon="leaf" sub="echantillons confirmes" />
            <MetricCard label="Foyers actifs" value={ALERT_DATA.length} color="text-info" icon="activity" sub="points sous surveillance" />
          </section>

          <section className="grid grid-cols-1 2xl:grid-cols-[1.05fr_1.25fr] gap-5">
            <MapPanel zones={ZONE_DATA} selectedZone={selectedZone} onSelect={setSelectedZone} />

            <div className="grid grid-cols-1 xl:grid-cols-[1fr_0.8fr] gap-5">
              <div className="bg-card border border-border rounded-2xl p-5 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-base font-semibold text-ink">Cas par maladie</h2>
                    <p className="text-xs text-sub mt-1">Comparaison des maladies detectees par zone.</p>
                  </div>
                  <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                    <Icon name="chart" className="w-5 h-5" />
                  </span>
                </div>
                <ResponsiveContainer width="100%" height={320}>
                  <BarChart data={filteredZones} margin={{ top: 8, right: 4, left: -18, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#DCECE1" vertical={false} />
                    <XAxis dataKey="zone" tick={{ fill: "#64748B", fontSize: 11 }} axisLine={{ stroke: "#DCECE1" }} tickLine={false} />
                    <YAxis tick={{ fill: "#64748B", fontSize: 11 }} axisLine={false} tickLine={false} />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontSize: "12px", color: "#64748B" }} />
                    <Bar dataKey="virusStrie" name="Virus Strie" fill={DISEASE_COLORS.virusStrie} radius={[6, 6, 0, 0]} />
                    <Bar dataKey="brulure" name="Brulure" fill={DISEASE_COLORS.brulure} radius={[6, 6, 0, 0]} />
                    <Bar dataKey="tacheGrise" name="Tache Grise" fill={DISEASE_COLORS.tacheGrise} radius={[6, 6, 0, 0]} />
                    <Bar dataKey="sain" name="Sain" fill={DISEASE_COLORS.sain} radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-card border border-border rounded-2xl p-5 shadow-sm">
                <div className="mb-4">
                  <h2 className="text-base font-semibold text-ink">Profil sanitaire</h2>
                  <p className="text-xs text-sub mt-1">Composition globale des diagnostics.</p>
                </div>
                <ResponsiveContainer width="100%" height={210}>
                  <PieChart>
                    <Pie data={totals.diseaseMix} dataKey="value" innerRadius={58} outerRadius={86} paddingAngle={3}>
                      {totals.diseaseMix.map(item => (
                        <Cell key={item.name} fill={item.color} />
                      ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="grid grid-cols-1 gap-2 mt-2">
                  {totals.diseaseMix.map(item => (
                    <div key={item.name} className="flex items-center justify-between text-xs">
                      <span className="flex items-center gap-2 text-sub">
                        <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                        {item.name}
                      </span>
                      <span className="font-semibold text-ink">{item.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <section className="grid grid-cols-1 xl:grid-cols-[1fr_1.25fr] gap-5">
            <div className="flex flex-col gap-3">
              <div>
                <h2 className="text-base font-semibold text-ink">Regions suivies</h2>
                <p className="text-xs text-sub mt-1">Cliquez une carte pour isoler la zone.</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {ZONE_DATA.map(z => (
                  <ZoneCard
                    key={z.zone}
                    {...z}
                    selected={selectedZone === z.zone}
                    onSelect={() => setSelectedZone(selectedZone === z.zone ? "Toutes" : z.zone)}
                  />
                ))}
              </div>
            </div>

            <div className="bg-card border border-border rounded-2xl overflow-hidden shadow-sm">
              <div className="px-5 py-4 border-b border-border flex items-center justify-between">
                <div>
                  <h2 className="text-base font-semibold text-ink">Priorites d'intervention</h2>
                  <p className="text-xs text-sub mt-1">Actions recommandees par niveau d'alerte.</p>
                </div>
                <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                  <Icon name="alert" className="w-5 h-5" />
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-primary/5">
                      {["Zone", "Maladie dominante", "Cas", "Alerte", "Action IRAD"].map(h => (
                        <th key={h} className="text-left text-sub uppercase tracking-wide font-semibold px-4 py-3 whitespace-nowrap">
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {filteredAlerts.map((row) => {
                      const style = {
                        Critique: "bg-red-50 text-danger border-danger/20",
                        Eleve: "bg-amber-50 text-warning border-warning/20",
                        Modere: "bg-blue-50 text-info border-info/20",
                        Faible: "bg-primary/5 text-primary border-primary/20",
                      }[row.niveau];
                      const action =
                        row.niveau === "Critique" ? "Elimination foyer" :
                        row.niveau === "Eleve" ? "Traitement curatif" :
                        row.niveau === "Faible" ? "Surveillance" :
                        "Traitement preventif";
                      return (
                        <tr key={`${row.zone}-${row.maladie}`} className="border-b border-border/60 hover:bg-primary/5 transition-colors">
                          <td className="px-4 py-3 text-ink font-semibold whitespace-nowrap">
                            <span className="flex items-center gap-2">
                              <Icon name="pin" className="w-4 h-4 text-primary" />
                              {row.zone}
                            </span>
                          </td>
                          <td className="px-4 py-3">
                            <span className="bg-primary/5 text-primary border border-primary/20 px-2.5 py-1 rounded-full whitespace-nowrap">
                              {row.maladie}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-ink font-semibold">{row.cas}</td>
                          <td className="px-4 py-3">
                            <span className={`px-2.5 py-1 rounded-full font-semibold border ${style}`}>
                              {row.niveau}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-warning font-semibold whitespace-nowrap">{action}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default EpidemiologieView;
