import React from 'react';
import { User, Menu, Globe } from 'lucide-react';

interface TopNavProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
}

export default function TopNav({ currentTab, onTabChange }: TopNavProps) {
  return (
    <header className="h-[80px] bg-canvas border-b border-hairline flex items-center justify-between px-6 md:px-20 sticky top-0 z-50">
      <div className="flex items-center space-x-2">
        <div className="text-primary text-[24px] font-bold tracking-tighter leading-none mt-1">Summer Internship</div>
        <div className="text-ink text-[14px] font-semibold ml-2 border-l border-hairline pl-4 mt-2">Field Sales</div>
      </div>
      
      <div className="hidden md:flex items-center space-x-8">
        <div 
          onClick={() => onTabChange('Dashboard')}
          className={`font-semibold text-[16px] cursor-pointer pb-6 mt-6 transition-colors ${currentTab === 'Dashboard' ? 'text-ink border-b-2 border-ink' : 'text-muted hover:text-ink'}`}
        >
          Dashboard
        </div>
        <div 
          onClick={() => onTabChange('Analytics')}
          className={`font-semibold text-[16px] cursor-pointer pb-6 mt-6 transition-colors ${currentTab === 'Analytics' ? 'text-ink border-b-2 border-ink' : 'text-muted hover:text-ink'}`}
        >
          Analytics
        </div>
        <div 
          onClick={() => onTabChange('Reports')}
          className={`font-semibold text-[16px] cursor-pointer pb-6 mt-6 transition-colors ${currentTab === 'Reports' ? 'text-ink border-b-2 border-ink' : 'text-muted hover:text-ink'}`}
        >
          Reports
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button className="hidden md:flex items-center space-x-2 text-[14px] font-semibold text-ink hover:bg-surface px-4 py-2 rounded-full transition-colors">
          <span>Host portal</span>
        </button>
        <button className="hidden md:flex items-center justify-center w-8 h-8 rounded-full hover:bg-surface transition-colors">
          <Globe className="w-4 h-4 text-ink" />
        </button>
        <button className="flex items-center space-x-3 border border-hairline rounded-full p-2 pl-4 hover:shadow-airbnb transition-shadow bg-canvas">
          <Menu className="w-4 h-4 text-ink" />
          <div className="w-8 h-8 rounded-full bg-surface flex items-center justify-center text-ink">
            <User className="w-5 h-5 text-ink" />
          </div>
        </button>
      </div>
    </header>
  );
}
