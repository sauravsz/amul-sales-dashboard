'use client';
import React, { useState, useMemo } from 'react';
import TopNav from './TopNav';
import FilterPill from './FilterPill';
import KpiCard from './KpiCard';
import { DailyTrendChart, ConversionBarChart, GenericBarMetricChart } from './Charts';
import type { SalesRecord, SauravDataset, DailyTrendItem, ConversionItem, BeatMetricItem } from '@/types/sales';
import { 
  Building2, 
  ShoppingBag, 
  TrendingUp, 
  MapPin, 
  AlertCircle, 
  CheckCircle2, 
  Store, 
  Search,
  ExternalLink,
  DollarSign
} from 'lucide-react';

interface DashboardProps {
  rawData: SalesRecord[];
  dataset?: SauravDataset | null;
}

export default function Dashboard({ rawData, dataset }: DashboardProps) {
  const [selectedIntern, setSelectedIntern] = useState('Saurav Sinha');
  const [selectedDistributor, setSelectedDistributor] = useState('');
  const [selectedBeat, setSelectedBeat] = useState('');
  const [selectedProduct, setSelectedProduct] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [currentTab, setCurrentTab] = useState('Dashboard');
  const [surveySearchQuery, setSurveySearchQuery] = useState('');
  const [surveyBeatFilter, setSurveyBeatFilter] = useState('');

  // Extract cascaded filter options
  const interns = useMemo(() => Array.from(new Set(rawData.map(d => d.intern_name).filter(Boolean))) as string[], [rawData]);
  
  const distributors = useMemo(() => {
    const data = selectedIntern ? rawData.filter(d => d.intern_name === selectedIntern) : rawData;
    return Array.from(new Set(data.map(d => d.distributor_name).filter(Boolean))).sort() as string[];
  }, [rawData, selectedIntern]);

  const beats = useMemo(() => {
    const data = rawData.filter(d => 
      (selectedIntern ? d.intern_name === selectedIntern : true) &&
      (selectedDistributor ? d.distributor_name === selectedDistributor : true)
    );
    return Array.from(new Set(data.map(d => d.beat_name).filter(Boolean))).sort() as string[];
  }, [rawData, selectedIntern, selectedDistributor]);

  const products = useMemo(() => {
    const data = rawData.filter(d => 
      (selectedIntern ? d.intern_name === selectedIntern : true) &&
      (selectedDistributor ? d.distributor_name === selectedDistributor : true) &&
      (selectedBeat ? d.beat_name === selectedBeat : true)
    );
    return Array.from(new Set(data.map(d => d.product_name).filter(Boolean))).sort() as string[];
  }, [rawData, selectedIntern, selectedDistributor, selectedBeat]);

  const categories = useMemo(() => {
    const data = rawData.filter(d => 
      (selectedIntern ? d.intern_name === selectedIntern : true) &&
      (selectedDistributor ? d.distributor_name === selectedDistributor : true) &&
      (selectedBeat ? d.beat_name === selectedBeat : true) &&
      (selectedProduct ? d.product_name === selectedProduct : true)
    );
    return Array.from(new Set(data.map(d => d.product_group).filter(Boolean))).sort() as string[];
  }, [rawData, selectedIntern, selectedDistributor, selectedBeat, selectedProduct]);

  // Filter the data based on selected filters
  const filteredData = useMemo(() => {
    return rawData.filter(d => {
      const matchIntern = selectedIntern ? d.intern_name === selectedIntern : true;
      const matchDistributor = selectedDistributor ? d.distributor_name === selectedDistributor : true;
      const matchBeat = selectedBeat ? d.beat_name === selectedBeat : true;
      const matchProduct = selectedProduct ? d.product_name === selectedProduct : true;
      const matchCategory = selectedCategory ? d.product_group === selectedCategory : true;
      return matchIntern && matchDistributor && matchBeat && matchProduct && matchCategory;
    });
  }, [rawData, selectedIntern, selectedDistributor, selectedBeat, selectedProduct, selectedCategory]);

  // Compute Overview Metrics
  const metrics = useMemo(() => {
    let totalPitches = 0;
    let successfulPitches = 0;
    let piecesOrdered = 0;
    let totalValue = 0;
    const dateMap = new Map<string, { pitches: number; orders: number }>();
    const productMap = new Map<string, { pitches: number; orders: number }>();
    const objectionMap = new Map<string, number>();

    filteredData.forEach(row => {
      totalPitches++;
      const isSuccessful = String(row.order_booked || '').toLowerCase() === 'yes';
      if (isSuccessful) successfulPitches++;
      
      const qty = parseInt(String(row.pieces_ordered || '0'), 10) || 0;
      piecesOrdered += qty;
      totalValue += parseFloat(String(row.order_value_if_known || '0')) || 0;

      // Daily Trend
      const d = row.date;
      if (d) {
        if (!dateMap.has(d)) dateMap.set(d, { pitches: 0, orders: 0 });
        const dayData = dateMap.get(d)!;
        dayData.pitches++;
        if (isSuccessful) dayData.orders++;
      }

      // Product Conversion
      const p = row.product_name;
      if (p) {
        if (!productMap.has(p)) productMap.set(p, { pitches: 0, orders: 0 });
        const pData = productMap.get(p)!;
        pData.pitches++;
        if (isSuccessful) pData.orders++;
      }

      // Objections
      const obj = row.retailer_objection_category;
      if (obj && obj !== 'None') {
        objectionMap.set(obj, (objectionMap.get(obj) || 0) + 1);
      }
    });

    const strikeRate = totalPitches > 0 ? (successfulPitches / totalPitches) * 100 : 0;
    const avgPieces = successfulPitches > 0 ? piecesOrdered / successfulPitches : 0;

    const dailyTrendData: DailyTrendItem[] = Array.from(dateMap.entries())
      .map(([date, data]) => ({ date, pitches: data.pitches, orders: data.orders }))
      .sort((a, b) => a.date.localeCompare(b.date));

    const productConvData: ConversionItem[] = Array.from(productMap.entries())
      .filter(([, data]) => data.pitches > 0)
      .map(([name, data]) => ({
        name: name.replace('Amul ', ''),
        rate: Number(((data.orders / data.pitches) * 100).toFixed(1)),
        pitches: data.pitches,
        orders: data.orders
      }))
      .sort((a, b) => Number(b.rate) - Number(a.rate))
      .slice(0, 6);

    const objectionData = Array.from(objectionMap.entries())
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 5);

    return { totalPitches, strikeRate, piecesOrdered, avgPieces, totalValue, dailyTrendData, productConvData, objectionData };
  }, [filteredData]);

  // Compute Beat-wise Metrics
  const beatMetrics: BeatMetricItem[] = useMemo(() => {
    if (!dataset?.daily_reports) return [];
    const map = new Map<string, { distributor: string; days: number; visited: number; converted: number; totalValue: number }>();
    
    dataset.daily_reports.forEach(d => {
      const b = d.beat;
      if (!map.has(b)) {
        map.set(b, { distributor: d.distributor, days: 0, visited: 0, converted: 0, totalValue: 0 });
      }
      const item = map.get(b)!;
      item.days += 1;
      item.visited += d.visited;
      item.converted += d.converted;
      item.totalValue += d.total_value;
    });

    return Array.from(map.entries()).map(([beat, v]) => ({
      beat,
      distributor: v.distributor,
      days: v.days,
      visited: v.visited,
      converted: v.converted,
      conversionRate: v.visited > 0 ? Number(((v.converted / v.visited) * 100).toFixed(1)) : 0,
      totalValue: v.totalValue
    })).sort((a, b) => b.visited - a.visited);
  }, [dataset]);

  // Filtered Survey Responses
  const filteredSurveys = useMemo(() => {
    if (!dataset?.survey_responses) return [];
    return dataset.survey_responses.filter(s => {
      const matchesSearch = surveySearchQuery === '' || 
        s.retailer_name.toLowerCase().includes(surveySearchQuery.toLowerCase()) ||
        s.beat_name.toLowerCase().includes(surveySearchQuery.toLowerCase()) ||
        s.challenges.toLowerCase().includes(surveySearchQuery.toLowerCase()) ||
        s.support_needed.toLowerCase().includes(surveySearchQuery.toLowerCase());
      const matchesBeat = surveyBeatFilter === '' || s.beat_name === surveyBeatFilter;
      return matchesSearch && matchesBeat;
    });
  }, [dataset, surveySearchQuery, surveyBeatFilter]);

  const surveyBeatOptions = useMemo(() => {
    if (!dataset?.survey_responses) return [];
    return Array.from(new Set(dataset.survey_responses.map(s => s.beat_name).filter(Boolean))).sort() as string[];
  }, [dataset]);

  return (
    <>
      <TopNav currentTab={currentTab} onTabChange={setCurrentTab} />
      
      {/* TAB 1: DASHBOARD OVERVIEW */}
      {currentTab === 'Dashboard' && (
        <div className="animate-fadeIn">
          {/* Hero Banner Section */}
          <div className="pt-14 pb-16 px-6 md:px-16 text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-bold tracking-wide uppercase mb-4 border border-primary/20">
              Silchar Summer Internship · 34 Market Days
            </div>
            <h1 className="text-ink text-[40px] md:text-[54px] font-bold tracking-tight leading-tight mb-4">
              Saurav Sinha Field Sales Intelligence
            </h1>
            <p className="text-muted text-[17px] leading-relaxed">
              Comprehensive field execution analytics tracking {dataset?.total_visits || 695} retailer visits, {dataset?.total_converted || 480} order conversions, distributor route productivity, and competitive SKU benchmarks across Silchar beats.
            </p>
          </div>

          <FilterPill 
            interns={interns} 
            distributors={distributors} 
            beats={beats} 
            products={products} 
            categories={categories}
            selectedIntern={selectedIntern} 
            selectedDistributor={selectedDistributor} 
            selectedBeat={selectedBeat} 
            selectedProduct={selectedProduct} 
            selectedCategory={selectedCategory}
            onInternChange={setSelectedIntern} 
            onDistributorChange={(val) => {
              setSelectedDistributor(val);
              setSelectedBeat('');
              setSelectedProduct('');
              setSelectedCategory('');
            }} 
            onBeatChange={(val) => {
              setSelectedBeat(val);
              setSelectedProduct('');
              setSelectedCategory('');
            }} 
            onProductChange={(val) => {
              setSelectedProduct(val);
              setSelectedCategory('');
            }} 
            onCategoryChange={setSelectedCategory}
          />

          <div className="px-6 md:px-16 max-w-[1440px] mx-auto">
            {/* KPI Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
              <KpiCard 
                label="Total Pitches / Visits" 
                value={metrics.totalPitches} 
                subtitle={`${beats.length} beats covered`}
                icon={<Store className="w-5 h-5 text-primary" />}
                color="#ff385c"
              />
              <KpiCard 
                label="Conversion Strike Rate" 
                value={`${metrics.strikeRate.toFixed(1)}%`} 
                subtitle="Orders converted / Visited"
                icon={<TrendingUp className="w-5 h-5 text-[#10B981]" />}
                color="#10B981"
              />
              <KpiCard 
                label="Pieces Ordered" 
                value={metrics.piecesOrdered.toLocaleString()} 
                subtitle={`Avg ${metrics.avgPieces.toFixed(1)} pcs/order`}
                icon={<ShoppingBag className="w-5 h-5 text-[#f59e0b]" />}
                color="#f59e0b"
              />
              <KpiCard 
                label="Estimated Sales Value" 
                value={`₹${metrics.totalValue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`} 
                subtitle="Field revenue booked"
                icon={<DollarSign className="w-5 h-5 text-[#428bff]" />}
                color="#428bff"
              />
            </div>

            {/* Primary Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <DailyTrendChart data={metrics.dailyTrendData} />
              <ConversionBarChart 
                data={metrics.productConvData} 
                title="Top Converting Amul SKUs (%)"
                xKey="name" 
                yKey="rate" 
              />
            </div>

            {/* Objections & Key Observations */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
              <div className="lg:col-span-1">
                <GenericBarMetricChart 
                  data={metrics.objectionData} 
                  title="Top Retailer Objections Encountered" 
                  unit=" outlets"
                />
              </div>

              <div className="lg:col-span-2 bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-[16px] font-bold text-ink">Recent Daily Market Visit Logs</h3>
                  <span className="text-xs font-semibold text-muted bg-surface-soft px-2.5 py-1 rounded-full border border-hairline">
                    Latest Days
                  </span>
                </div>
                <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1">
                  {(dataset?.daily_reports || []).slice(-6).reverse().map((d, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl border border-hairline bg-surface-soft/40 hover:bg-surface-soft transition-colors">
                      <div className="flex items-center justify-between mb-1.5">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-ink text-sm">Day {d.day_no} · {d.beat}</span>
                          <span className="text-xs text-muted">({d.date})</span>
                        </div>
                        <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-primary/10 text-primary">
                          {d.converted}/{d.visited} Orders ({d.conversion_rate}%)
                        </span>
                      </div>
                      <p className="text-xs text-muted leading-relaxed line-clamp-2">
                        {d.observations}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: BEATS & ROUTES */}
      {currentTab === 'Beats' && (
        <div className="px-6 md:px-16 max-w-[1440px] mx-auto py-10 animate-fadeIn">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-ink mb-2">Beat & Route Productivity Ranking</h2>
            <p className="text-muted text-sm max-w-2xl">
              Performance breakdown across {beatMetrics.length} distinct beats in Silchar, analyzing total retailer visits, conversion strike rates, and distributor distribution.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-5 mb-8">
            <div className="bg-canvas border border-hairline rounded-[14px] p-5 shadow-airbnb">
              <div className="text-xs text-muted font-medium mb-1">Total Beats Mapped</div>
              <div className="text-2xl font-bold text-ink">{beatMetrics.length}</div>
            </div>
            <div className="bg-canvas border border-hairline rounded-[14px] p-5 shadow-airbnb">
              <div className="text-xs text-muted font-medium mb-1">Primary Distributors</div>
              <div className="text-2xl font-bold text-ink">3 Agencies</div>
            </div>
            <div className="bg-canvas border border-hairline rounded-[14px] p-5 shadow-airbnb">
              <div className="text-xs text-muted font-medium mb-1">Top Performing Beat</div>
              <div className="text-2xl font-bold text-primary">
                {beatMetrics.length > 0 ? beatMetrics[0].beat : 'Malugram'}
              </div>
            </div>
            <div className="bg-canvas border border-hairline rounded-[14px] p-5 shadow-airbnb">
              <div className="text-xs text-muted font-medium mb-1">Avg Outlets / Beat</div>
              <div className="text-2xl font-bold text-ink">
                {beatMetrics.length > 0 ? Math.round(beatMetrics.reduce((a, b) => a + b.visited, 0) / beatMetrics.length) : 20}
              </div>
            </div>
          </div>

          {/* Beat Performance Table */}
          <div className="bg-canvas border border-hairline rounded-[14px] shadow-airbnb overflow-hidden">
            <div className="p-5 border-b border-hairline">
              <h3 className="font-bold text-ink text-base">Beat Ranking Table</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-sm">
                <thead>
                  <tr className="bg-surface-soft text-muted text-xs uppercase font-bold border-b border-hairline">
                    <th className="py-3 px-5">Beat Name</th>
                    <th className="py-3 px-5">Distributor</th>
                    <th className="py-3 px-5 text-right">Days</th>
                    <th className="py-3 px-5 text-right">Visits</th>
                    <th className="py-3 px-5 text-right">Orders Converted</th>
                    <th className="py-3 px-5 text-right">Conversion Rate</th>
                    <th className="py-3 px-5 text-right">Total Value</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-hairline">
                  {beatMetrics.map((b, idx) => (
                    <tr key={idx} className="hover:bg-surface-soft/50 transition-colors">
                      <td className="py-3.5 px-5 font-semibold text-ink flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-primary shrink-0" />
                        {b.beat}
                      </td>
                      <td className="py-3.5 px-5 text-muted">{b.distributor}</td>
                      <td className="py-3.5 px-5 text-right text-muted">{b.days}</td>
                      <td className="py-3.5 px-5 text-right font-medium text-ink">{b.visited}</td>
                      <td className="py-3.5 px-5 text-right font-medium text-ink">{b.converted}</td>
                      <td className="py-3.5 px-5 text-right">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold ${
                          b.conversionRate >= 75 ? 'bg-emerald-50 text-emerald-700' :
                          b.conversionRate >= 60 ? 'bg-amber-50 text-amber-700' : 'bg-rose-50 text-rose-700'
                        }`}>
                          {b.conversionRate}%
                        </span>
                      </td>
                      <td className="py-3.5 px-5 text-right font-semibold text-ink">
                        ₹{b.totalValue > 0 ? b.totalValue.toLocaleString() : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: RETAILER VOICE & SURVEYS */}
      {currentTab === 'Surveys' && (
        <div className="px-6 md:px-16 max-w-[1440px] mx-auto py-10 animate-fadeIn">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-ink mb-2">Retailer Voice & Survey Intelligence</h2>
            <p className="text-muted text-sm max-w-2xl">
              119 verified retailer survey responses collected directly by Saurav Sinha across Silchar retail counters, analyzing margin satisfaction, stock-out bottlenecks, and competitor dominance.
            </p>
          </div>

          {/* Search & Beat Filters */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-muted absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={surveySearchQuery}
                onChange={(e) => setSurveySearchQuery(e.target.value)}
                placeholder="Search retailer, beat, challenges, or support needed..."
                className="w-full bg-canvas border border-hairline rounded-xl pl-10 pr-4 py-2.5 text-sm text-ink focus:outline-none focus:border-primary transition-colors shadow-sm"
              />
            </div>
            <select
              value={surveyBeatFilter}
              onChange={(e) => setSurveyBeatFilter(e.target.value)}
              className="bg-canvas border border-hairline rounded-xl px-4 py-2.5 text-sm text-ink focus:outline-none focus:border-primary transition-colors shadow-sm"
            >
              <option value="">All Beats ({surveyBeatOptions.length})</option>
              {surveyBeatOptions.map((beat, idx) => (
                <option key={idx} value={beat}>{beat}</option>
              ))}
            </select>
          </div>

          {/* Survey Cards / Table */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredSurveys.slice(0, 30).map((s, idx) => (
              <div key={idx} className="bg-canvas border border-hairline rounded-[14px] p-5 shadow-airbnb flex flex-col justify-between hover:shadow-md transition-shadow">
                <div>
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-bold text-ink text-base">{s.retailer_name}</h4>
                      <span className="text-xs text-muted font-medium flex items-center gap-1 mt-0.5">
                        <MapPin className="w-3 h-3 text-primary" /> {s.beat_name}
                      </span>
                    </div>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                      s.faces_stockouts.toLowerCase() === 'yes' ? 'bg-rose-50 text-rose-700' : 'bg-emerald-50 text-emerald-700'
                    }`}>
                      {s.faces_stockouts.toLowerCase() === 'yes' ? 'Stock-outs: Yes' : 'No Stock-outs'}
                    </span>
                  </div>

                  <div className="space-y-2.5 text-xs text-muted mt-4 border-t border-hairline pt-3">
                    <div>
                      <span className="font-semibold text-ink">Stocked:</span> {s.stocked_variants || 'Amul Kool / Lassi / Tru'}
                    </div>
                    <div>
                      <span className="font-semibold text-ink">Top Competitor:</span> {s.competitors_stocked || 'Coke / Sprite / Purabi'}
                    </div>
                    {s.challenges && (
                      <div className="bg-surface-soft p-2.5 rounded-lg text-ink font-medium">
                        <span className="font-bold text-primary">Challenge:</span> {s.challenges}
                      </div>
                    )}
                    {s.support_needed && (
                      <div className="text-xs text-muted">
                        <span className="font-semibold text-ink">Support Requested:</span> {s.support_needed}
                      </div>
                    )}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-hairline flex items-center justify-between text-[11px] text-muted">
                  <span>Margin: <strong className="text-ink">{s.margin_satisfied || 'Not Sure'}</strong></span>
                  <span>Brand Loyalty: <strong className="text-ink">{s.brand_loyalty || 'Moderate'}</strong></span>
                </div>
              </div>
            ))}
          </div>

          {filteredSurveys.length > 30 && (
            <div className="text-center py-6 text-xs text-muted">
              Showing 30 of {filteredSurveys.length} retailer records. Use the search filter above to narrow results.
            </div>
          )}
        </div>
      )}

      {/* TAB 4: SKU & PTR ECONOMICS */}
      {currentTab === 'Economics' && (
        <div className="px-6 md:px-16 max-w-[1440px] mx-auto py-10 animate-fadeIn">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-ink mb-2">Amul Product SKU & PTR Economics Catalog</h2>
            <p className="text-muted text-sm max-w-2xl">
              Authentic pricing master with MRP, Price to Retailer (PTR), Retailer Margin in ₹ and %, and standard carton packaging across 26 focus SKUs.
            </p>
          </div>

          <div className="bg-canvas border border-hairline rounded-[14px] shadow-airbnb overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-sm">
                <thead>
                  <tr className="bg-surface-soft text-muted text-xs uppercase font-bold border-b border-hairline">
                    <th className="py-3.5 px-5">Product Name</th>
                    <th className="py-3.5 px-5">Category</th>
                    <th className="py-3.5 px-5">Pack Size</th>
                    <th className="py-3.5 px-5 text-right">MRP (₹)</th>
                    <th className="py-3.5 px-5 text-right">PTR (₹)</th>
                    <th className="py-3.5 px-5 text-right">Margin (₹)</th>
                    <th className="py-3.5 px-5 text-right">Margin (%)</th>
                    <th className="py-3.5 px-5 text-right">Case Size</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-hairline">
                  {(dataset?.products_master || []).map((p, idx) => (
                    <tr key={idx} className="hover:bg-surface-soft/50 transition-colors">
                      <td className="py-3.5 px-5 font-semibold text-ink">{p.product_name}</td>
                      <td className="py-3.5 px-5 text-muted">
                        <span className="px-2 py-0.5 rounded-full bg-surface-soft text-ink text-xs font-medium border border-hairline">
                          {p.product_group}
                        </span>
                      </td>
                      <td className="py-3.5 px-5 text-muted">{p.pack_size}</td>
                      <td className="py-3.5 px-5 text-right font-bold text-ink">₹{p.mrp.toFixed(2)}</td>
                      <td className="py-3.5 px-5 text-right text-muted">₹{p.ptr.toFixed(2)}</td>
                      <td className="py-3.5 px-5 text-right font-medium text-emerald-600">₹{p.retailer_margin_rs.toFixed(2)}</td>
                      <td className="py-3.5 px-5 text-right">
                        <span className="font-bold text-ink bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full text-xs">
                          {p.margin_percent}%
                        </span>
                      </td>
                      <td className="py-3.5 px-5 text-right text-muted">{p.units_per_case} units</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
