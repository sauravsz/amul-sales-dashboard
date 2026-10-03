'use client';
import React, { useState, useMemo } from 'react';
import TopNav from './TopNav';
import FilterPill from './FilterPill';
import KpiCard from './KpiCard';
import { DailyTrendChart, ConversionBarChart } from './Charts';
import ObjectionVisualizer from './ObjectionVisualizer';
import type { SalesRecord, SauravDataset, DailyTrendItem, ConversionItem, BeatMetricItem } from '@/types/sales';
import { 
  ShoppingBag, 
  TrendingUp, 
  MapPin, 
  Store, 
  Search,
  DollarSign,
  CheckCircle2,
  AlertTriangle,
  Flame,
  Sparkles,
  Award,
  Percent,
  TrendingDown
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
  const [skuCategoryFilter, setSkuCategoryFilter] = useState('All');

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

  // Filtered field logs
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

    // Top converting products filtered by statistical significance (pitches >= 5)
    const productConvData: ConversionItem[] = Array.from(productMap.entries())
      .filter(([, data]) => data.pitches >= 5)
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
      .slice(0, 6);

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
      const q = surveySearchQuery.toLowerCase();
      const matchesSearch = surveySearchQuery === '' || 
        s.retailer_name.toLowerCase().includes(q) ||
        s.beat_name.toLowerCase().includes(q) ||
        s.challenges.toLowerCase().includes(q) ||
        s.support_needed.toLowerCase().includes(q) ||
        s.competitors_stocked.toLowerCase().includes(q);
      const matchesBeat = surveyBeatFilter === '' || s.beat_name === surveyBeatFilter;
      return matchesSearch && matchesBeat;
    });
  }, [dataset, surveySearchQuery, surveyBeatFilter]);

  const surveyBeatOptions = useMemo(() => {
    if (!dataset?.survey_responses) return [];
    return Array.from(new Set(dataset.survey_responses.map(s => s.beat_name).filter(Boolean))).sort() as string[];
  }, [dataset]);

  // Filtered Products for Economics Tab
  const filteredProductsMaster = useMemo(() => {
    if (!dataset?.products_master) return [];
    return dataset.products_master.filter(p => {
      if (skuCategoryFilter === 'All') return true;
      return p.product_group === skuCategoryFilter;
    });
  }, [dataset, skuCategoryFilter]);

  const productCategories = useMemo(() => {
    if (!dataset?.products_master) return ['All'];
    return ['All', ...Array.from(new Set(dataset.products_master.map(p => p.product_group)))];
  }, [dataset]);

  return (
    <div className="min-h-screen bg-[#fafafa] text-[#222222] pb-24 md:pb-16">
      <TopNav currentTab={currentTab} onTabChange={setCurrentTab} />
      
      {/* TAB 1: DASHBOARD OVERVIEW */}
      {currentTab === 'Dashboard' && (
        <div className="animate-fadeIn">
          {/* Hero Banner Section */}
          <div className="pt-8 sm:pt-12 pb-10 sm:pb-14 px-4 sm:px-8 text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-1.5 sm:gap-2 px-3 py-1 sm:px-3.5 sm:py-1.5 rounded-full bg-[#ff385c]/10 text-[#ff385c] text-[11px] sm:text-xs font-bold tracking-wide uppercase mb-3 border border-[#ff385c]/20 shadow-xs">
              <Sparkles className="w-3.5 h-3.5 shrink-0" /> Silchar Field Study · Summer Internship · Saurav Sinha
            </div>
            <h1 className="text-[#222222] text-[26px] sm:text-[36px] md:text-[48px] font-bold tracking-tight leading-tight mb-2.5">
              Amul Field Sales & Route Intelligence
            </h1>
            <p className="text-[#717171] text-xs sm:text-[15px] leading-relaxed max-w-2xl mx-auto">
              Real-time analytics across {dataset?.total_visits || 695} retailer visits, 22 beat routes, and 119 surveyed retail counters in the Silchar market.
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

          <div className="px-4 sm:px-8 md:px-16 max-w-[1440px] mx-auto">
            {/* KPI Cards Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-5 mb-6 sm:mb-8">
              <KpiCard 
                label="Total Pitches" 
                value={metrics.totalPitches.toLocaleString()} 
                subtitle={`${beats.length} beats covered`}
                icon={<Store className="w-4 h-4 sm:w-5 sm:h-5 text-[#ff385c]" />}
                color="#ff385c"
              />
              <KpiCard 
                label="Conversion Rate" 
                value={`${metrics.strikeRate.toFixed(1)}%`} 
                subtitle="Booked / Pitches"
                icon={<TrendingUp className="w-4 h-4 sm:w-5 sm:h-5 text-[#10B981]" />}
                color="#10B981"
              />
              <KpiCard 
                label="Pieces Ordered" 
                value={metrics.piecesOrdered.toLocaleString()} 
                subtitle={`Avg ${metrics.avgPieces.toFixed(1)}/order`}
                icon={<ShoppingBag className="w-4 h-4 sm:w-5 sm:h-5 text-[#f59e0b]" />}
                color="#f59e0b"
              />
              <KpiCard 
                label="Estimated Value" 
                value={`₹${metrics.totalValue.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`} 
                subtitle="Field revenue"
                icon={<DollarSign className="w-4 h-4 sm:w-5 sm:h-5 text-[#428bff]" />}
                color="#428bff"
              />
            </div>

            {/* Strategic Empirical Findings (from Thesis & 119 Surveys) */}
            <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4 mb-6 sm:mb-8">
              <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-3.5 sm:p-5 shadow-xs">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] sm:text-xs font-bold text-[#717171] uppercase">Margin Gap</span>
                  <TrendingDown className="w-3.5 h-3.5 text-rose-500 shrink-0" />
                </div>
                <div className="text-xl sm:text-2xl font-bold text-rose-600">89.8%</div>
                <p className="text-[10px] sm:text-xs text-[#717171] mt-0.5 leading-snug">Retailers citing low margin vs local drinks</p>
              </div>

              <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-3.5 sm:p-5 shadow-xs">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] sm:text-xs font-bold text-[#717171] uppercase">Trade Schemes</span>
                  <Percent className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                </div>
                <div className="text-xl sm:text-2xl font-bold text-amber-600">0.0%</div>
                <p className="text-[10px] sm:text-xs text-[#717171] mt-0.5 leading-snug">Outlets receiving trade combos or discounts</p>
              </div>

              <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-3.5 sm:p-5 shadow-xs">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] sm:text-xs font-bold text-[#717171] uppercase">Stock Delivery</span>
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                </div>
                <div className="text-xl sm:text-2xl font-bold text-emerald-600">93.8%</div>
                <p className="text-[10px] sm:text-xs text-[#717171] mt-0.5 leading-snug">Consistent supply on Amul Kool & Lassi</p>
              </div>

              <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-3.5 sm:p-5 shadow-xs">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] sm:text-xs font-bold text-[#717171] uppercase">Hero SKU</span>
                  <Award className="w-3.5 h-3.5 text-[#ff385c] shrink-0" />
                </div>
                <div className="text-lg sm:text-2xl font-bold text-[#ff385c] truncate">Amul Lassi</div>
                <p className="text-[10px] sm:text-xs text-[#717171] mt-0.5 leading-snug">Highest consumer pull & daily turnover</p>
              </div>
            </div>

            {/* Primary Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
              <DailyTrendChart data={metrics.dailyTrendData} />
              <ConversionBarChart 
                data={metrics.productConvData} 
                title="Top Converting Amul Focus SKUs (%)"
                xKey="name" 
                yKey="rate" 
              />
            </div>

            {/* Objections Visualizer & Key Observations */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 mb-8 sm:mb-12">
              <div className="lg:col-span-1">
                <ObjectionVisualizer 
                  data={metrics.objectionData} 
                  title="Top Retailer Objections & Bottlenecks" 
                  subtitle="Granular root-cause analysis of non-converted field pitches"
                />
              </div>

              <div className="lg:col-span-2 bg-white border border-[#dddddd] rounded-[16px] p-4 sm:p-6 shadow-xs flex flex-col justify-between">
                <div className="flex items-center justify-between mb-3 sm:mb-4">
                  <div>
                    <h3 className="text-[15px] sm:text-[17px] font-bold text-[#222222]">Verified Daily Market Visit Notes</h3>
                    <p className="text-[11px] sm:text-xs text-[#717171] mt-0.5">Chronological field notes from Saurav Sinha across Silchar routes</p>
                  </div>
                  <span className="text-[11px] sm:text-xs font-semibold text-[#717171] bg-[#f7f7f7] px-2.5 py-1 rounded-full border border-[#dddddd] shrink-0">
                    Market Logs
                  </span>
                </div>
                <div className="space-y-2.5 max-h-[300px] overflow-y-auto pr-1 custom-scrollbar">
                  {(dataset?.daily_reports || []).slice(-8).reverse().map((d, idx) => (
                    <div key={idx} className="p-3 rounded-xl border border-[#ebebeb] bg-[#fafafa] hover:bg-white hover:border-[#dddddd] transition-all">
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-1.5 min-w-0">
                          <span className="font-bold text-[#222222] text-xs sm:text-sm truncate">Day {d.day_no} · {d.beat}</span>
                          <span className="text-[11px] text-[#717171] shrink-0">({d.date.slice(5)})</span>
                        </div>
                        <span className="text-[10px] sm:text-xs font-bold px-2 py-0.5 rounded-full bg-[#ff385c]/10 text-[#ff385c] shrink-0">
                          {d.converted}/{d.visited} ({d.conversion_rate}%)
                        </span>
                      </div>
                      <p className="text-[11px] sm:text-xs text-[#555555] leading-relaxed line-clamp-2">
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
        <div className="px-4 sm:px-8 md:px-16 max-w-[1440px] mx-auto py-6 sm:py-10 animate-fadeIn">
          <div className="mb-6 sm:mb-8">
            <h2 className="text-xl sm:text-2xl font-bold text-[#222222] mb-1">Beat & Route Productivity Ranking</h2>
            <p className="text-[#717171] text-xs sm:text-sm max-w-2xl">
              Performance breakdown across {beatMetrics.length} distinct beats in Silchar, analyzing total retailer visits, conversion strike rates, and distributor distribution.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-5 mb-6 sm:mb-8">
            <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-4 sm:p-5 shadow-xs">
              <div className="text-[11px] text-[#717171] font-medium mb-0.5">Total Beats</div>
              <div className="text-xl sm:text-2xl font-bold text-[#222222]">{beatMetrics.length} Beats</div>
            </div>
            <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-4 sm:p-5 shadow-xs">
              <div className="text-[11px] text-[#717171] font-medium mb-0.5">Distributors</div>
              <div className="text-xl sm:text-2xl font-bold text-[#222222]">3 Agencies</div>
            </div>
            <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-4 sm:p-5 shadow-xs">
              <div className="text-[11px] text-[#717171] font-medium mb-0.5">Top Visited Beat</div>
              <div className="text-lg sm:text-2xl font-bold text-[#ff385c] truncate">
                {beatMetrics.length > 0 ? beatMetrics[0].beat : 'Malugram'}
              </div>
            </div>
            <div className="bg-white border border-[#dddddd] rounded-[14px] sm:rounded-[16px] p-4 sm:p-5 shadow-xs">
              <div className="text-[11px] text-[#717171] font-medium mb-0.5">Avg Strike Rate</div>
              <div className="text-xl sm:text-2xl font-bold text-emerald-600">
                {beatMetrics.length > 0 ? (beatMetrics.reduce((a, b) => a + b.conversionRate, 0) / beatMetrics.length).toFixed(1) : 65}%
              </div>
            </div>
          </div>

          {/* Beat Performance Table */}
          <div className="bg-white border border-[#dddddd] rounded-[16px] shadow-xs overflow-hidden">
            <div className="p-4 sm:p-5 border-b border-[#dddddd] flex items-center justify-between">
              <h3 className="font-bold text-[#222222] text-sm sm:text-base">Silchar Beat Performance Table</h3>
              <span className="text-[11px] text-[#717171]">Scroll horizontally on mobile</span>
            </div>
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left border-collapse text-xs sm:text-sm min-w-[620px]">
                <thead>
                  <tr className="bg-[#f7f7f7] text-[#717171] text-[11px] uppercase font-bold border-b border-[#dddddd]">
                    <th className="py-3 px-4">Beat Name</th>
                    <th className="py-3 px-4">Distributor</th>
                    <th className="py-3 px-4 text-right">Days</th>
                    <th className="py-3 px-4 text-right">Visits</th>
                    <th className="py-3 px-4 text-right">Orders</th>
                    <th className="py-3 px-4 text-right">Strike Rate</th>
                    <th className="py-3 px-4 text-right">Value (₹)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#ebebeb]">
                  {beatMetrics.map((b, idx) => (
                    <tr key={idx} className="hover:bg-[#fbfbfb] transition-colors">
                      <td className="py-3 px-4 font-semibold text-[#222222] flex items-center gap-1.5">
                        <MapPin className="w-3.5 h-3.5 text-[#ff385c] shrink-0" />
                        <span className="truncate">{b.beat}</span>
                      </td>
                      <td className="py-3 px-4 text-[#555555]">{b.distributor}</td>
                      <td className="py-3 px-4 text-right text-[#717171]">{b.days}</td>
                      <td className="py-3 px-4 text-right font-medium text-[#222222]">{b.visited}</td>
                      <td className="py-3 px-4 text-right font-medium text-[#222222]">{b.converted}</td>
                      <td className="py-3 px-4 text-right">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-bold ${
                          b.conversionRate >= 70 ? 'bg-emerald-50 text-emerald-700' :
                          b.conversionRate >= 55 ? 'bg-amber-50 text-amber-700' : 'bg-rose-50 text-rose-700'
                        }`}>
                          {b.conversionRate}%
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right font-semibold text-[#222222]">
                        ₹{b.totalValue > 0 ? b.totalValue.toLocaleString('en-IN', { maximumFractionDigits: 0 }) : '—'}
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
        <div className="px-4 sm:px-8 md:px-16 max-w-[1440px] mx-auto py-6 sm:py-10 animate-fadeIn">
          <div className="mb-6 sm:mb-8">
            <h2 className="text-xl sm:text-2xl font-bold text-[#222222] mb-1">Retailer Voice & Survey Intelligence</h2>
            <p className="text-[#717171] text-xs sm:text-sm max-w-2xl">
              119 verified retailer survey responses collected directly by Saurav Sinha across Silchar retail counters, analyzing margin satisfaction, stock-out bottlenecks, and competitor dominance.
            </p>
          </div>

          {/* Search & Beat Filters */}
          <div className="flex flex-col sm:flex-row gap-2.5 sm:gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-[#717171] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={surveySearchQuery}
                onChange={(e) => setSurveySearchQuery(e.target.value)}
                placeholder="Search retailer, beat, competitor, or challenge..."
                className="w-full bg-white border border-[#dddddd] rounded-xl pl-10 pr-4 py-2 text-xs sm:text-sm text-[#222222] focus:outline-none focus:border-[#ff385c] transition-colors shadow-xs"
              />
            </div>
            <select
              value={surveyBeatFilter}
              onChange={(e) => setSurveyBeatFilter(e.target.value)}
              className="bg-white border border-[#dddddd] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#222222] focus:outline-none focus:border-[#ff385c] transition-colors shadow-xs"
            >
              <option value="">All Beats ({surveyBeatOptions.length})</option>
              {surveyBeatOptions.map((beat, idx) => (
                <option key={idx} value={beat}>{beat}</option>
              ))}
            </select>
          </div>

          {/* Survey Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 sm:gap-5">
            {filteredSurveys.slice(0, 30).map((s, idx) => (
              <div key={idx} className="bg-white border border-[#dddddd] rounded-[16px] p-4 sm:p-5 shadow-xs flex flex-col justify-between hover:shadow-sm transition-all">
                <div>
                  <div className="flex items-start justify-between mb-2">
                    <div className="min-w-0 pr-2">
                      <h4 className="font-bold text-[#222222] text-sm sm:text-base truncate">{s.retailer_name}</h4>
                      <span className="text-[11px] text-[#717171] font-medium flex items-center gap-1 mt-0.5">
                        <MapPin className="w-3 h-3 text-[#ff385c] shrink-0" /> {s.beat_name}
                      </span>
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0 ${
                      s.faces_stockouts === 'Yes' ? 'bg-rose-50 text-rose-700' : 'bg-emerald-50 text-emerald-700'
                    }`}>
                      {s.faces_stockouts === 'Yes' ? 'Stockouts: Yes' : 'No Stockouts'}
                    </span>
                  </div>

                  <div className="space-y-2 text-xs text-[#555555] mt-3 border-t border-[#ebebeb] pt-2.5">
                    <div>
                      <span className="font-semibold text-[#222222]">Top Demand:</span> {s.top_demanded_product || 'Amul Lassi'}
                    </div>
                    <div>
                      <span className="font-semibold text-[#222222]">Competitors:</span> {s.competitors_stocked}
                    </div>
                    {s.challenges && (
                      <div className="bg-[#f7f7f7] p-2 rounded-lg text-[#222222] font-medium border border-[#ebebeb] text-[11px]">
                        <span className="font-bold text-[#ff385c]">Challenge:</span> {s.challenges}
                      </div>
                    )}
                  </div>
                </div>

                <div className="mt-3 pt-2.5 border-t border-[#ebebeb] flex items-center justify-between text-[11px] text-[#717171]">
                  <span>Margin: <strong className="text-[#222222]">{s.margin_satisfied}</strong></span>
                  <span>Loyalty: <strong className="text-[#222222]">{s.brand_loyalty}</strong></span>
                </div>
              </div>
            ))}
          </div>

          {filteredSurveys.length > 30 && (
            <div className="text-center py-5 text-xs text-[#717171]">
              Showing 30 of {filteredSurveys.length} survey responses. Use search to filter specific counters.
            </div>
          )}
        </div>
      )}

      {/* TAB 4: SKU & PTR ECONOMICS */}
      {currentTab === 'Economics' && (
        <div className="px-4 sm:px-8 md:px-16 max-w-[1440px] mx-auto py-6 sm:py-10 animate-fadeIn">
          <div className="mb-6 sm:mb-8">
            <h2 className="text-xl sm:text-2xl font-bold text-[#222222] mb-1">Amul Product SKU & PTR Economics Catalog</h2>
            <p className="text-[#717171] text-xs sm:text-sm max-w-2xl">
              Authentic pricing master with MRP, Price to Retailer (PTR), Retailer Margin in ₹ and %, and standard carton packaging across 35 focus SKUs.
            </p>
          </div>

          {/* Category Filter Pills */}
          <div className="flex flex-wrap gap-1.5 sm:gap-2 mb-5">
            {productCategories.map((cat, idx) => (
              <button
                key={idx}
                onClick={() => setSkuCategoryFilter(cat)}
                className={`px-3 py-1.5 rounded-full text-xs font-bold transition-all ${
                  skuCategoryFilter === cat 
                    ? 'bg-[#222222] text-white shadow-xs' 
                    : 'bg-white text-[#555555] border border-[#dddddd] hover:bg-[#f7f7f7]'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          <div className="bg-white border border-[#dddddd] rounded-[16px] shadow-xs overflow-hidden">
            <div className="p-4 border-b border-[#dddddd] flex items-center justify-between">
              <h3 className="font-bold text-[#222222] text-sm sm:text-base">Product Pricing & Trade Margins</h3>
              <span className="text-[11px] text-[#717171]">Scroll horizontally on mobile</span>
            </div>
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left border-collapse text-xs sm:text-sm min-w-[650px]">
                <thead>
                  <tr className="bg-[#f7f7f7] text-[#717171] text-[11px] uppercase font-bold border-b border-[#dddddd]">
                    <th className="py-3 px-4">Product Name</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4">Pack Size</th>
                    <th className="py-3 px-4 text-right">MRP (₹)</th>
                    <th className="py-3 px-4 text-right">PTR (₹)</th>
                    <th className="py-3 px-4 text-right">Margin (₹)</th>
                    <th className="py-3 px-4 text-right">Margin (%)</th>
                    <th className="py-3 px-4 text-right">Case Size</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#ebebeb]">
                  {filteredProductsMaster.map((p, idx) => (
                    <tr key={idx} className="hover:bg-[#fbfbfb] transition-colors">
                      <td className="py-3 px-4 font-semibold text-[#222222]">{p.product_name}</td>
                      <td className="py-3 px-4 text-[#717171]">
                        <span className="px-2 py-0.5 rounded-full bg-[#f7f7f7] text-[#222222] text-[11px] font-medium border border-[#dddddd]">
                          {p.product_group}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-[#717171]">{p.pack_size}</td>
                      <td className="py-3 px-4 text-right font-bold text-[#222222]">₹{p.mrp.toFixed(2)}</td>
                      <td className="py-3 px-4 text-right text-[#717171]">₹{p.ptr.toFixed(2)}</td>
                      <td className="py-3 px-4 text-right font-semibold text-emerald-600">₹{p.retailer_margin_rs.toFixed(2)}</td>
                      <td className="py-3 px-4 text-right">
                        <span className="font-bold text-[#222222] bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full text-[10px] sm:text-xs">
                          {p.margin_percent}%
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right text-[#717171]">{p.units_per_case} units</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
