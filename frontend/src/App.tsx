import React, { useEffect, useState } from "react";
import type { Hotel, RoomType, PriceRecommendationResponse } from "./apiTypes";
import { fetchHotels, fetchRoomTypesForHotel, fetchPriceRecommendation } from "./apiClient";

const App: React.FC = () => {
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [selectedHotelId, setSelectedHotelId] = useState<number | "">("");
  const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
  const [selectedRoomTypeId, setSelectedRoomTypeId] = useState<number | "">("");

  const [checkInDate, setCheckInDate] = useState("");
  const [stayLength, setStayLength] = useState(1);
  const [bookingWindow, setBookingWindow] = useState(7);

  const [recommendation, setRecommendation] = useState<PriceRecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Load hotels
  useEffect(() => {
    (async () => {
      try {
        const data = await fetchHotels();
        setHotels(data);
        if (data.length > 0) setSelectedHotelId(data[0].id);
      } catch {
        setErrorMsg("Failed to load hotels. Is backend running on 127.0.0.1:8000?");
      }
    })();
  }, []);

  // Load room types when hotel changes
  useEffect(() => {
    (async () => {
      if (selectedHotelId === "") return;
      try {
        const data = await fetchRoomTypesForHotel(selectedHotelId);
        setRoomTypes(data);
        setSelectedRoomTypeId(data.length > 0 ? data[0].id : "");
      } catch {
        setErrorMsg("Failed to load room types.");
      }
    })();
  }, [selectedHotelId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setRecommendation(null);

    if (selectedHotelId === "" || selectedRoomTypeId === "" || !checkInDate) {
      setErrorMsg("Please select hotel, room type, and check-in date.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetchPriceRecommendation({
        hotel_id: selectedHotelId,
        room_type_id: selectedRoomTypeId,
        check_in_date: checkInDate,
        stay_length: stayLength,
        booking_window: bookingWindow,
      });
      setRecommendation(res);
    } catch {
      setErrorMsg("Failed to fetch price recommendation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-900/80 backdrop-blur-xl flex flex-col">
        <div className="px-6 py-5 border-b border-slate-800">
          <h1 className="text-xl font-semibold tracking-tight">
            SmartRate <span className="text-indigo-400">AI</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">Hotel Revenue Intelligence</p>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-1 text-sm">
          <NavItem label="Overview" active />
          <NavItem label="Pricing Engine" />
          <NavItem label="Hotels & Rooms" />
          <NavItem label="Bookings" />
          <NavItem label="Reports" />
        </nav>

        <div className="px-4 py-4 text-xs text-slate-500 border-t border-slate-800">
          v0.1 • Local dev
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col">
        <header className="border-b border-slate-800 px-8 py-4 flex items-center justify-between bg-slate-950/60 backdrop-blur-xl">
          <div>
            <h2 className="text-lg font-semibold tracking-tight">Revenue Overview</h2>
            <p className="text-xs text-slate-400 mt-1">
              Dynamic pricing engine connected to FastAPI.
            </p>
          </div>

          <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 text-xs">
            Backend: Online
          </span>
        </header>

        <section className="flex-1 px-8 py-6 space-y-6 overflow-y-auto">
          {/* KPI */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <KpiCard label="Occupancy (Today)" value="78%" trend="+4.3% vs last week" />
            <KpiCard label="ADR" value="$142" trend="+$12 vs last week" />
            <KpiCard label="RevPAR" value="$111" trend="+8.1% vs last week" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Form */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
              <h3 className="text-sm font-semibold mb-1">Dynamic Pricing Engine</h3>
              <p className="text-xs text-slate-400 mb-4">
                Generate AI price recommendations in real time.
              </p>

              {errorMsg && (
                <div className="mb-3 text-xs text-red-300 bg-red-950/40 border border-red-800 rounded-lg px-3 py-2">
                  {errorMsg}
                </div>
              )}

              <form
                onSubmit={handleSubmit}
                className="space-y-3 text-xs bg-slate-950/40 border border-slate-800 rounded-xl px-4 py-4"
              >
                <div className="flex flex-col gap-1">
                  <label className="text-slate-300">Hotel</label>
                  <select
                    className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    value={selectedHotelId}
                    onChange={(e) => setSelectedHotelId(e.target.value ? Number(e.target.value) : "")}
                  >
                    {hotels.map((h) => (
                      <option key={h.id} value={h.id}>
                        {h.name} — {h.city}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex flex-col gap-1">
                  <label className="text-slate-300">Room type</label>
                  <select
                    className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    value={selectedRoomTypeId}
                    onChange={(e) =>
                      setSelectedRoomTypeId(e.target.value ? Number(e.target.value) : "")
                    }
                  >
                    {roomTypes.map((rt) => (
                      <option key={rt.id} value={rt.id}>
                        {rt.name} • sleeps {rt.capacity} • base ${rt.base_price}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="flex flex-col gap-1">
                    <label className="text-slate-300">Check-in date</label>
                    <input
                      type="date"
                      className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      value={checkInDate}
                      onChange={(e) => setCheckInDate(e.target.value)}
                    />
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-slate-300">Stay length</label>
                    <input
                      type="number"
                      min={1}
                      className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      value={stayLength}
                      onChange={(e) => setStayLength(Number(e.target.value))}
                    />
                  </div>

                  <div className="flex flex-col gap-1">
                    <label className="text-slate-300">Booking window</label>
                    <input
                      type="number"
                      min={0}
                      className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      value={bookingWindow}
                      onChange={(e) => setBookingWindow(Number(e.target.value))}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center justify-center rounded-lg bg-indigo-500 hover:bg-indigo-400 disabled:opacity-60 px-4 py-2 text-xs font-medium"
                >
                  {loading ? "Calculating..." : "Generate recommendation"}
                </button>
              </form>
            </div>

            {/* Result */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
              <h3 className="text-sm font-semibold mb-1">Latest Recommendation</h3>
              <p className="text-xs text-slate-400 mb-4">Result from FastAPI pricing model.</p>

              {!recommendation ? (
                <div className="rounded-xl border border-dashed border-slate-700/70 p-4 text-xs text-slate-500">
                  No recommendation yet. Submit the form to generate one.
                </div>
              ) : (
                <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 space-y-3">
                  <div className="flex items-end justify-between">
                    <div>
                      <p className="text-[11px] uppercase tracking-[0.16em] text-slate-500">
                        Recommended Rate
                      </p>
                      <p className="text-3xl font-semibold text-emerald-400">
                        {recommendation.currency} {recommendation.recommended_price.toFixed(2)}
                      </p>
                    </div>
                    <div className="text-right text-xs text-slate-400">
                      <div>Model: {recommendation.model_price.toFixed(2)}</div>
                      <div>Base: {recommendation.base_price.toFixed(2)}</div>
                    </div>
                  </div>

                  <div className="border-t border-slate-800 pt-3 grid grid-cols-2 gap-3 text-xs">
                    <div>
                      <div className="text-[11px] text-slate-500">Hotel ID</div>
                      <div className="text-slate-200">{recommendation.hotel_id}</div>
                    </div>
                    <div>
                      <div className="text-[11px] text-slate-500">Room Type ID</div>
                      <div className="text-slate-200">{recommendation.room_type_id}</div>
                    </div>
                    <div>
                      <div className="text-[11px] text-slate-500">Check-in</div>
                      <div className="text-slate-200">{recommendation.check_in_date}</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

type NavItemProps = { label: string; active?: boolean };

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

type KpiCardProps = { label: string; value: string; trend: string };

const KpiCard: React.FC<KpiCardProps> = ({ label, value, trend }) => (
  <div className="rounded-2xl border border-slate-800 bg-slate-900/70 px-4 py-4 flex flex-col justify-between">
    <div>
      <p className="text-[11px] uppercase tracking-[0.16em] text-slate-500 mb-1">{label}</p>
      <p className="text-2xl font-semibold text-slate-50">{value}</p>
    </div>
    <p className="mt-3 text-xs text-emerald-400">{trend}</p>
  </div>
);

export default App;
