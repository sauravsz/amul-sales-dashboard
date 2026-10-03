'use client';
import React from 'react';
import { MapPin, BarChart3, Users, DollarSign } from 'lucide-react';

interface TopNavProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
}

export default function TopNav({ currentTab, onTabChange }: TopNavProps) {
  const navTabs = [
    { id: 'Dashboard', label: 'Dashboard', shortLabel: 'Overview', icon: BarChart3 },
    { id: 'Beats', label: 'Beats & Routes', shortLabel: 'Beats', icon: MapPin },
    { id: 'Surveys', label: 'Retailer Voice', shortLabel: 'Surveys (119)', icon: Users },
    { id: 'Economics', label: 'SKU Economics', shortLabel: 'SKU & PTR', icon: DollarSign },
  ];

  return (
    <>
      {/* Desktop & Mobile Header */}
      <header className="h-[64px] sm:h-[76px] bg-white/95 border-b border-[#dddddd] flex items-center justify-between px-4 sm:px-8 md:px-16 sticky top-0 z-50 shadow-xs backdrop-blur-md">
        <div className="flex items-center space-x-2.5 sm:space-x-3">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 sm:w-3.5 sm:h-3.5 rounded-full bg-[#ff385c] inline-block shadow-xs" />
            <span className="text-[#222222] text-[17px] sm:text-[21px] font-bold tracking-tight">
              Amul Field Intelligence
            </span>
          </div>
          <div className="hidden lg:flex items-center text-[11px] font-bold uppercase tracking-wider text-[#717171] bg-[#f7f7f7] px-2.5 py-1 rounded-full border border-[#dddddd]">
            Saurav Sinha · Silchar Beats
          </div>
        </div>
        
        {/* Desktop Navigation Tabs */}
        <div className="hidden md:flex items-center space-x-6">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = currentTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`flex items-center gap-2 text-[14px] font-semibold pb-4 pt-4 transition-all border-b-2 ${
                  isActive 
                    ? 'text-[#222222] border-[#222222]' 
                    : 'text-[#717171] border-transparent hover:text-[#222222]'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-[#ff385c]' : 'text-[#717171]'}`} />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* User / Market Badge */}
        <div className="flex items-center space-x-2.5">
          <div className="flex flex-col text-right">
            <span className="text-xs font-bold text-[#222222]">34 Days</span>
            <span className="text-[10px] text-[#717171]">Silchar</span>
          </div>
          <div className="w-8 h-8 rounded-full bg-[#ff385c]/10 border border-[#ff385c]/20 flex items-center justify-center text-[#ff385c] font-bold text-xs shadow-xs">
            SS
          </div>
        </div>
      </header>

      {/* Mobile Top Scrollable Sub-nav Strip */}
      <div className="flex md:hidden bg-white border-b border-[#dddddd] px-2 py-1.5 overflow-x-auto no-scrollbar sticky top-[64px] z-40 shadow-xs">
        <div className="flex items-center gap-1.5 min-w-max mx-auto">
          {navTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = currentTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all ${
                  isActive
                    ? 'bg-[#222222] text-white shadow-xs'
                    : 'bg-[#f7f7f7] text-[#555555] border border-[#dddddd] hover:bg-[#ebebeb]'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-[#ff385c]' : 'text-[#717171]'}`} />
                {tab.shortLabel}
              </button>
            );
          })}
        </div>
      </div>

      {/* Mobile Bottom Navigation Bar (Persistent 1-Thumb Switching) */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/95 border-t border-[#dddddd] backdrop-blur-md px-2 py-1.5 flex items-center justify-around shadow-lg">
        {navTabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all ${
                isActive ? 'text-[#ff385c]' : 'text-[#717171] hover:text-[#222222]'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'stroke-[2.5]' : 'stroke-2'}`} />
              <span className={`text-[10px] mt-0.5 ${isActive ? 'font-bold' : 'font-medium'}`}>
                {tab.shortLabel.split(' ')[0]}
              </span>
            </button>
          );
        })}
      </nav>
    </>
  );
}
