'use client';
import React from 'react';

interface KpiCardProps {
  label: string;
  value: string | number;
  subtitle: string;
  icon?: React.ReactNode;
  color?: string;
}

export default function KpiCard({ label, value, subtitle, icon, color = "#ff385c" }: KpiCardProps) {
  return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-4 sm:p-5 shadow-xs flex flex-col justify-between min-h-[105px] sm:min-h-[120px] transition-all hover:shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <div className="text-[#222222] text-[13px] sm:text-[15px] font-semibold tracking-tight">{label}</div>
        {icon && (
          <div className="p-1.5 rounded-lg bg-[#f7f7f7] border border-[#ebebeb] shrink-0">
            {icon}
          </div>
        )}
      </div>
      <div>
        <div className="text-[#222222] text-[22px] sm:text-[28px] font-bold leading-tight mb-0.5">
          {value}
        </div>
        <div className="text-[#717171] text-[11px] sm:text-[13px] font-normal truncate">
          {subtitle}
        </div>
      </div>
    </div>
  );
}
