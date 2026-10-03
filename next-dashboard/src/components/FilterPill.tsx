'use client';
import React from 'react';
import { Search, SlidersHorizontal, RotateCcw } from 'lucide-react';

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
  const hasActiveFilters = Boolean(selectedDistributor || selectedBeat || selectedProduct || selectedCategory);

  const resetFilters = () => {
    onDistributorChange('');
    onBeatChange('');
    onProductChange('');
    onCategoryChange('');
  };

  return (
    <div className="relative z-30 mb-8 px-4 sm:px-8">
      {/* 1. Desktop Floating Airbnb Pill (lg and above) */}
      <div className="hidden lg:flex justify-center -mt-6">
        <div className="bg-white border border-[#dddddd] rounded-full shadow-md flex items-center h-[66px] pl-6 pr-2 hover:shadow-lg transition-shadow">
          {/* Intern */}
          <div className="flex flex-col justify-center border-r border-[#ebebeb] pr-4 w-[130px]">
            <span className="text-[11px] font-bold text-[#222222] tracking-wider uppercase">Intern</span>
            <select
              value={selectedIntern}
              onChange={(e) => onInternChange(e.target.value)}
              className="bg-transparent text-[13px] text-[#222222] font-semibold focus:outline-none cursor-pointer truncate"
            >
              {interns.map((i, idx) => (
                <option key={idx} value={i}>{i}</option>
              ))}
            </select>
          </div>

          {/* Distributor */}
          <div className="flex flex-col justify-center border-r border-[#ebebeb] px-4 w-[145px]">
            <span className="text-[11px] font-bold text-[#222222] tracking-wider uppercase">Distributor</span>
            <select
              value={selectedDistributor}
              onChange={(e) => onDistributorChange(e.target.value)}
              className="bg-transparent text-[13px] text-[#222222] font-medium focus:outline-none cursor-pointer truncate"
            >
              <option value="">All Distributors</option>
              {distributors.map((d, idx) => (
                <option key={idx} value={d}>{d}</option>
              ))}
            </select>
          </div>

          {/* Beat */}
          <div className="flex flex-col justify-center border-r border-[#ebebeb] px-4 w-[145px]">
            <span className="text-[11px] font-bold text-[#222222] tracking-wider uppercase">Route Beat</span>
            <select
              value={selectedBeat}
              onChange={(e) => onBeatChange(e.target.value)}
              className="bg-transparent text-[13px] text-[#222222] font-medium focus:outline-none cursor-pointer truncate"
            >
              <option value="">All Beats ({beats.length})</option>
              {beats.map((b, idx) => (
                <option key={idx} value={b}>{b}</option>
              ))}
            </select>
          </div>

          {/* Product */}
          <div className="flex flex-col justify-center border-r border-[#ebebeb] px-4 w-[155px]">
            <span className="text-[11px] font-bold text-[#222222] tracking-wider uppercase">Focus SKU</span>
            <select
              value={selectedProduct}
              onChange={(e) => onProductChange(e.target.value)}
              className="bg-transparent text-[13px] text-[#222222] font-medium focus:outline-none cursor-pointer truncate"
            >
              <option value="">All Products</option>
              {products.map((p, idx) => (
                <option key={idx} value={p}>{p.replace('Amul ', '')}</option>
              ))}
            </select>
          </div>

          {/* Category */}
          <div className="flex flex-col justify-center px-4 w-[130px]">
            <span className="text-[11px] font-bold text-[#222222] tracking-wider uppercase">Category</span>
            <select
              value={selectedCategory}
              onChange={(e) => onCategoryChange(e.target.value)}
              className="bg-transparent text-[13px] text-[#222222] font-medium focus:outline-none cursor-pointer truncate"
            >
              <option value="">All Categories</option>
              {categories.map((c, idx) => (
                <option key={idx} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Action Orb */}
          {hasActiveFilters ? (
            <button
              onClick={resetFilters}
              title="Reset all filters"
              className="w-[46px] h-[46px] rounded-full bg-[#f7f7f7] border border-[#dddddd] text-[#717171] hover:text-[#222222] flex items-center justify-center transition-colors ml-2 shrink-0"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          ) : (
            <div className="w-[46px] h-[46px] rounded-full bg-[#ff385c] flex items-center justify-center text-white ml-2 shrink-0 shadow-xs">
              <Search className="w-4 h-4" strokeWidth={2.5} />
            </div>
          )}
        </div>
      </div>

      {/* 2. Mobile / Tablet Responsive Filter Carousel (< lg) */}
      <div className="lg:hidden bg-white border border-[#dddddd] rounded-2xl p-3 shadow-xs">
        <div className="flex items-center justify-between mb-2 px-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#222222]">
            <SlidersHorizontal className="w-3.5 h-3.5 text-[#ff385c]" />
            <span>Filter Route Data</span>
          </div>
          {hasActiveFilters && (
            <button
              onClick={resetFilters}
              className="text-[11px] font-semibold text-[#ff385c] flex items-center gap-1 hover:underline"
            >
              <RotateCcw className="w-3 h-3" /> Reset
            </button>
          )}
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {/* Distributor */}
          <div className="bg-[#f7f7f7] border border-[#ebebeb] rounded-xl px-2.5 py-1.5 flex flex-col">
            <span className="text-[10px] font-bold text-[#717171] uppercase">Distributor</span>
            <select
              value={selectedDistributor}
              onChange={(e) => onDistributorChange(e.target.value)}
              className="bg-transparent text-xs text-[#222222] font-semibold focus:outline-none cursor-pointer truncate mt-0.5"
            >
              <option value="">All ({distributors.length})</option>
              {distributors.map((d, idx) => (
                <option key={idx} value={d}>{d}</option>
              ))}
            </select>
          </div>

          {/* Beat */}
          <div className="bg-[#f7f7f7] border border-[#ebebeb] rounded-xl px-2.5 py-1.5 flex flex-col">
            <span className="text-[10px] font-bold text-[#717171] uppercase">Beat Route</span>
            <select
              value={selectedBeat}
              onChange={(e) => onBeatChange(e.target.value)}
              className="bg-transparent text-xs text-[#222222] font-semibold focus:outline-none cursor-pointer truncate mt-0.5"
            >
              <option value="">All Beats ({beats.length})</option>
              {beats.map((b, idx) => (
                <option key={idx} value={b}>{b}</option>
              ))}
            </select>
          </div>

          {/* Focus SKU */}
          <div className="bg-[#f7f7f7] border border-[#ebebeb] rounded-xl px-2.5 py-1.5 flex flex-col">
            <span className="text-[10px] font-bold text-[#717171] uppercase">Focus SKU</span>
            <select
              value={selectedProduct}
              onChange={(e) => onProductChange(e.target.value)}
              className="bg-transparent text-xs text-[#222222] font-semibold focus:outline-none cursor-pointer truncate mt-0.5"
            >
              <option value="">All Products</option>
              {products.map((p, idx) => (
                <option key={idx} value={p}>{p.replace('Amul ', '')}</option>
              ))}
            </select>
          </div>

          {/* Category */}
          <div className="bg-[#f7f7f7] border border-[#ebebeb] rounded-xl px-2.5 py-1.5 flex flex-col">
            <span className="text-[10px] font-bold text-[#717171] uppercase">Category</span>
            <select
              value={selectedCategory}
              onChange={(e) => onCategoryChange(e.target.value)}
              className="bg-transparent text-xs text-[#222222] font-semibold focus:outline-none cursor-pointer truncate mt-0.5"
            >
              <option value="">All Categories</option>
              {categories.map((c, idx) => (
                <option key={idx} value={c}>{c}</option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
