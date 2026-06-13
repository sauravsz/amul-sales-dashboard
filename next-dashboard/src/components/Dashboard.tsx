'use client';
import React, { useState, useMemo } from 'react';
import TopNav from './TopNav';
import FilterPill from './FilterPill';
import KpiCard from './KpiCard';
import { DailyTrendChart, ConversionBarChart } from './Charts';

export default function Dashboard({ rawData }: { rawData: any[] }) {
  const [selectedIntern, setSelectedIntern] = useState('');
  const [selectedDistributor, setSelectedDistributor] = useState('');
  const [selectedBeat, setSelectedBeat] = useState('');
  const [selectedProduct, setSelectedProduct] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  // 1. Extract cascaded filter options
  const interns = useMemo(() => Array.from(new Set(rawData.map(d => d.intern_name).filter(Boolean))).sort() as string[], [rawData]);
  
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

  // 2. Filter the data based on selected filters
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

  // 3. Compute Metrics
  const metrics = useMemo(() => {
    let totalPitches = 0;
    let successfulPitches = 0;
    let piecesOrdered = 0;
    let totalValue = 0;
    const dateMap = new Map<string, { pitches: number, orders: number }>();
    const productMap = new Map<string, { pitches: number, orders: number }>();

    filteredData.forEach(row => {
      totalPitches++;
      const isSuccessful = String(row.order_booked).toLowerCase() === 'yes' || String(row.sales_successful).toLowerCase() === 'true';
      if (isSuccessful) successfulPitches++;
      
      const qty = parseInt(row.pieces_ordered) || parseInt(row.quantity_ordered) || 0;
      piecesOrdered += qty;
      totalValue += parseFloat(row.estimated_value) || 0;

      // Daily Trend
      const d = row.date;
      if (d) {
        if (!dateMap.has(d)) dateMap.set(d, { pitches: 0, orders: 0 });
        const dayData = dateMap.get(d)!;
        dayData.pitches++;
        if (isSuccessful) dayData.orders++;
      }

      // Product Conv
      const p = row.product_name;
      if (p) {
        if (!productMap.has(p)) productMap.set(p, { pitches: 0, orders: 0 });
        const pData = productMap.get(p)!;
        pData.pitches++;
        if (isSuccessful) pData.orders++;
      }
    });

    const strikeRate = totalPitches > 0 ? (successfulPitches / totalPitches) * 100 : 0;
    const avgPieces = successfulPitches > 0 ? piecesOrdered / successfulPitches : 0;

    const dailyTrendData = Array.from(dateMap.entries())
      .map(([date, data]) => ({ date, pitches: data.pitches, orders: data.orders }))
      .sort((a, b) => a.date.localeCompare(b.date));

    const productConvData = Array.from(productMap.entries())
      .map(([name, data]) => ({
        product: name,
        conversion: data.pitches > 0 ? (data.orders / data.pitches) * 100 : 0
      }))
      .filter(p => p.pitches !== 0) // Hide zero pitch prods
      .sort((a, b) => b.conversion - a.conversion)
      .slice(0, 5); // top 5

    return { totalPitches, strikeRate, piecesOrdered, avgPieces, totalValue, dailyTrendData, productConvData };
  }, [filteredData]);

  const [currentTab, setCurrentTab] = useState('Dashboard');

  return (
    <>
      <TopNav currentTab={currentTab} onTabChange={setCurrentTab} />
      
      {currentTab === 'Dashboard' ? (
        <>
          {/* Hero Banner Section (Clean white, photography/text led) */}
          <div className="pt-16 pb-24 px-6 md:px-20 text-center">
            <h1 className="text-ink text-[48px] md:text-[64px] font-bold tracking-tighter leading-tight mb-4">
              Internship Sales Performance
            </h1>
            <p className="text-muted text-[18px] max-w-2xl mx-auto">
              Analyze your daily field visits, monitor distributor engagement, and track product conversion rates across all your assigned routes.
            </p>
          </div>

          <FilterPill 
            interns={interns} distributors={distributors} beats={beats} products={products} categories={categories}
            selectedIntern={selectedIntern} selectedDistributor={selectedDistributor} selectedBeat={selectedBeat} selectedProduct={selectedProduct} selectedCategory={selectedCategory}
            onInternChange={(val) => {
              setSelectedIntern(val);
              setSelectedDistributor('');
              setSelectedBeat('');
              setSelectedProduct('');
              setSelectedCategory('');
            }} 
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

          <div className="px-6 md:px-20 max-w-[1440px] mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              <KpiCard 
                label="Total Pitches" 
                value={metrics.totalPitches} 
                subtitle="Overall reach"
                color="#ff385c"
              />
              <KpiCard 
                label="Strike Rate" 
                value={`${metrics.strikeRate.toFixed(1)}%`} 
                subtitle="Orders / Pitches"
                color="#10B981"
              />
              <KpiCard 
                label="Pieces Ordered" 
                value={metrics.piecesOrdered} 
                subtitle={`Avg ${metrics.avgPieces.toFixed(1)}/order`}
                color="#f59e0b"
              />
              <KpiCard 
                label="Estimated Value" 
                value={`₹${metrics.totalValue.toLocaleString()}`} 
                subtitle="Potential revenue"
                color="#428bff"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-20">
              <DailyTrendChart data={metrics.dailyTrendData} />
              <ConversionBarChart 
                data={metrics.productConvData} 
                title="Top Converting Products (%)"
                xKey="product" 
                yKey="conversion" 
              />
            </div>
          </div>
        </>
      ) : (
        <div className="py-32 px-6 text-center">
          <div className="max-w-md mx-auto bg-canvas border border-hairline rounded-2xl p-12 shadow-airbnb">
            <h2 className="text-2xl font-bold text-ink mb-4">{currentTab}</h2>
            <p className="text-muted">The {currentTab} page is currently under construction. Check back soon for deeper insights and automated reporting.</p>
          </div>
        </div>
      )}
    </>
  );
}
