import React from "react";

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-900/80 backdrop-blur-xl flex flex-col">
        <div className="px-6 py-5 border-b border-slate-800">
          <h1 className="text-xl font-semibold tracking-tight">
            SmartRate <span className="text-indigo-400">AI</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Hotel Revenue Intelligence
          </p>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-1 text-sm">
          <NavItem label="Overview" active />
          <NavItem label="Pricing Engine" />
          <NavItem label="Hotels & Rooms" />
          <NavItem label="Bookings" />
          <NavItem label="Reports" />
        </nav>

        <div className="px-4 py-4 text-xs text-slate-500 border-t border-slate-800">
          v0.1 • Internal sandbox
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 flex flex-col">
        {/* Top bar */}
        <header className="border-b border-slate-800 px-8 py-4 flex items-center justify-between bg-slate-950/60 backdrop-blur-xl">
          <div>
            <h2 className="text-lg font-semibold tracking-tight">
              Revenue Overview
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Monitor demand, pricing performance, and booking trends.
            </p>
          </div>

          <div className="flex items-center gap-3 text-xs">
            <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
              Backend: Online
            </span>
            <button className="px-3 py-1 rounded-full bg-slate-800 hover:bg-slate-700 border border-slate-600 text-slate-200">
              Refresh metrics
            </button>
          </div>
        </header>

        {/* Content area */}
        <section className="flex-1 px-8 py-6 space-y-6 overflow-y-auto">
          {/* KPI cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <KpiCard
              label="Occupancy (Today)"
              value="78%"
              trend="+4.3% vs last week"
            />
            <KpiCard
              label="ADR (Average Daily Rate)"
              value="$142"
              trend="+$12 vs last week"
            />
            <KpiCard
              label="RevPAR"
              value="$111"
              trend="+8.1% vs last week"
            />
          </div>

          {/* Placeholder for pricing engine panel */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
              <h3 className="text-sm font-semibold mb-1">
                Dynamic Pricing Engine
              </h3>
              <p className="text-xs text-slate-400 mb-4">
                Select a hotel, room type, and stay dates to generate AI-driven
                price recommendations.
              </p>
              <div className="rounded-xl border border-dashed border-slate-700/70 p-4 text-xs text-slate-400">
                Pricing form will go here — next step.
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
              <h3 className="text-sm font-semibold mb-1">
                Recent Price Recommendations
              </h3>
              <p className="text-xs text-slate-400 mb-4">
                Once wired to the backend, this will show the last N price
                decisions, with model price vs final applied rate.
              </p>
              <div className="rounded-xl border border-dashed border-slate-700/70 p-4 text-xs text-slate-500">
                No recommendations yet. Generate one using the pricing engine
                panel.
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

type NavItemProps = {
  label: string;
  active?: boolean;
};

const NavItem: React.FC<NavItemProps> = ({ label, active }) => (
  <button
    className={[
      "w-full flex items-center px-3 py-2 rounded-lg transition text-left",
      active
        ? "bg-slate-800 text-slate-50"
        : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/60",
    ].join(" ")}
  >
    <span className="text-sm">{label}</span>
  </button>
);

type KpiCardProps = {
  label: string;
  value: string;
  trend: string;
};

const KpiCard: React.FC<KpiCardProps> = ({ label, value, trend }) => (
  <div className="rounded-2xl border border-slate-800 bg-slate-900/70 px-4 py-4 flex flex-col justify-between">
    <div>
      <p className="text-[11px] uppercase tracking-[0.16em] text-slate-500 mb-1">
        {label}
      </p>
      <p className="text-2xl font-semibold text-slate-50">{value}</p>
    </div>
    <p className="mt-3 text-xs text-emerald-400">{trend}</p>
  </div>
);

export default App;
