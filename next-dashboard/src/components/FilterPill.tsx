import React from 'react';
import { Search } from 'lucide-react';

interface FilterPillProps {
  interns: string[];
  distributors: string[];
  beats: string[];
  products: string[];
  categories: string[];
  selectedIntern: string;
  selectedDistributor: string;
  selectedBeat: string;
  selectedProduct: string;
  selectedCategory: string;
  onInternChange: (v: string) => void;
  onDistributorChange: (v: string) => void;
  onBeatChange: (v: string) => void;
  onProductChange: (v: string) => void;
  onCategoryChange: (v: string) => void;
}

export default function FilterPill({
  interns, distributors, beats, products, categories,
  selectedIntern, selectedDistributor, selectedBeat, selectedProduct, selectedCategory,
  onInternChange, onDistributorChange, onBeatChange, onProductChange, onCategoryChange
}: FilterPillProps) {
  return (
    <div className="flex justify-center -mt-8 mb-12 relative z-40">
      <div className="bg-canvas border border-hairline rounded-[9999px] shadow-airbnb flex items-center h-[64px] pl-6 pr-2">
        
        {/* Intern */}
        <div className="flex flex-col justify-center border-r border-hairline pr-4 w-[140px]">
          <label className="text-[12px] font-bold text-ink mb-0.5">Who</label>
          <select 
            className="bg-transparent text-[14px] text-muted outline-none appearance-none cursor-pointer truncate"
            value={selectedIntern}
            onChange={(e) => onInternChange(e.target.value)}
          >
            <option value="">Any intern</option>
            {interns.map(i => <option key={i} value={i}>{i}</option>)}
          </select>
        </div>

        {/* Distributor */}
        <div className="flex flex-col justify-center border-r border-hairline px-4 w-[140px]">
          <label className="text-[12px] font-bold text-ink mb-0.5">Distributor</label>
          <select 
            className="bg-transparent text-[14px] text-muted outline-none appearance-none cursor-pointer truncate"
            value={selectedDistributor}
            onChange={(e) => onDistributorChange(e.target.value)}
          >
            <option value="">Any distributor</option>
            {distributors.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>

        {/* Route/Beat */}
        <div className="flex flex-col justify-center border-r border-hairline px-4 w-[140px]">
          <label className="text-[12px] font-bold text-ink mb-0.5">Where</label>
          <select 
            className="bg-transparent text-[14px] text-muted outline-none appearance-none cursor-pointer truncate"
            value={selectedBeat}
            onChange={(e) => onBeatChange(e.target.value)}
          >
            <option value="">Any route</option>
            {beats.map(b => <option key={b} value={b}>{b}</option>)}
          </select>
        </div>

        {/* Product */}
        <div className="flex flex-col justify-center border-r border-hairline px-4 w-[140px]">
          <label className="text-[12px] font-bold text-ink mb-0.5">What</label>
          <select 
            className="bg-transparent text-[14px] text-muted outline-none appearance-none cursor-pointer truncate"
            value={selectedProduct}
            onChange={(e) => onProductChange(e.target.value)}
          >
            <option value="">Any product</option>
            {products.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>

        {/* Category */}
        <div className="flex flex-col justify-center px-4 w-[140px]">
          <label className="text-[12px] font-bold text-ink mb-0.5">Category</label>
          <select 
            className="bg-transparent text-[14px] text-muted outline-none appearance-none cursor-pointer truncate"
            value={selectedCategory}
            onChange={(e) => onCategoryChange(e.target.value)}
          >
            <option value="">Any category</option>
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        {/* Search Orb */}
        <button className="w-[48px] h-[48px] rounded-full bg-primary flex items-center justify-center hover:bg-[#e00b41] transition-colors ml-2 flex-shrink-0">
          <Search className="w-5 h-5 text-canvas" strokeWidth={3} />
        </button>

      </div>
    </div>
  );
}
