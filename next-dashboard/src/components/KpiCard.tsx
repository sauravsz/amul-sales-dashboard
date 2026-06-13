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
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb flex flex-col justify-center min-h-[120px]">
      <div className="flex items-center justify-between mb-3">
        <div className="text-ink text-[16px] font-semibold">{label}</div>
        {icon && (
          <div className="text-ink">
            {icon}
          </div>
        )}
      </div>
      <div className="text-ink text-[28px] font-bold leading-tight mb-1">
        {value}
      </div>
      <div className="text-muted text-[14px] font-normal">
        {subtitle}
      </div>
    </div>
  );
}
