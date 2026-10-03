import React from 'react';
import { User, Menu, MapPin, BarChart3, Users, DollarSign } from 'lucide-react';

interface TopNavProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
}

export default function TopNav({ currentTab, onTabChange }: TopNavProps) {
  const navTabs = [
    { id: 'Dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'Beats', label: 'Beats & Routes', icon: MapPin },
    { id: 'Surveys', label: 'Retailer Voice (119)', icon: Users },
    { id: 'Economics', label: 'SKU & PTR Economics', icon: DollarSign },
  ];

  return (
    <header className="h-[80px] bg-canvas border-b border-hairline flex items-center justify-between px-6 md:px-16 sticky top-0 z-50 shadow-sm backdrop-blur-md bg-canvas/95">
      <div className="flex items-center space-x-3">
        <div className="flex items-center gap-2">
          <span className="w-3.5 h-3.5 rounded-full bg-primary inline-block" />
          <span className="text-ink text-[22px] font-bold tracking-tight">Amul Field Intelligence</span>
        </div>
        <div className="hidden sm:flex items-center text-xs font-semibold uppercase tracking-wider text-muted bg-surface-soft px-2.5 py-1 rounded-full border border-hairline">
          Saurav Sinha · Silchar Beats
        </div>
      </div>
      
      <div className="hidden md:flex items-center space-x-6">
        {navTabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex items-center gap-2 text-[15px] font-semibold pb-5 pt-5 transition-colors border-b-2 ${
                isActive 
                  ? 'text-ink border-ink' 
                  : 'text-muted border-transparent hover:text-ink'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-primary' : 'text-muted'}`} />
              {tab.label}
            </button>
          );
        })}
      </div>

      <div className="flex items-center space-x-3">
        <div className="hidden lg:flex flex-col text-right">
          <span className="text-xs font-bold text-ink">34 Market Days</span>
          <span className="text-[11px] text-muted">Silchar Division</span>
        </div>
        <div className="flex items-center space-x-2 border border-hairline rounded-full py-1.5 px-3 hover:shadow-airbnb transition-shadow bg-canvas">
          <Menu className="w-4 h-4 text-ink" />
          <div className="w-7 h-7 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-xs">
            SS
          </div>
        </div>
      </div>
    </header>
  );
}
