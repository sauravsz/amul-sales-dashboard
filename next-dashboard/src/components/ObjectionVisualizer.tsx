'use client';
import React, { useMemo } from 'react';
import { 
  PackageX, 
  DollarSign, 
  RotateCcw, 
  CloudRain, 
  Snowflake, 
  CheckCircle2, 
  AlertTriangle,
  Layers,
  Sparkles
} from 'lucide-react';

interface ObjectionItem {
  name: string;
  value: number;
  color?: string;
}

interface ObjectionVisualizerProps {
  data: ObjectionItem[];
  title?: string;
  subtitle?: string;
}

// Map objection categories to rich metadata, colors, icons, and field recommendations
const OBJECTION_METADATA: Record<string, {
  color: string;
  bgColor: string;
  borderColor: string;
  badgeBg: string;
  badgeText: string;
  category: string;
  icon: React.ComponentType<{ className?: string }>;
  recommendation: string;
}> = {
  "Existing Stock Sufficient": {
    color: "#64748b",
    bgColor: "bg-slate-50",
    borderColor: "border-slate-200",
    badgeBg: "bg-slate-100",
    badgeText: "text-slate-700",
    category: "Inventory",
    icon: Layers,
    recommendation: "Re-pitch on next scheduled cycle; focus on faster-moving pack sizes."
  },
  "Stock Already Available": {
    color: "#64748b",
    bgColor: "bg-slate-50",
    borderColor: "border-slate-200",
    badgeBg: "bg-slate-100",
    badgeText: "text-slate-700",
    category: "Inventory",
    icon: Layers,
    recommendation: "Verify retail sell-through rate and check shelf visibility."
  },
  "Damaged Stock / Slow Return": {
    color: "#e11d48",
    bgColor: "bg-rose-50/60",
    borderColor: "border-rose-200",
    badgeBg: "bg-rose-100",
    badgeText: "text-rose-700",
    category: "Logistics",
    icon: RotateCcw,
    recommendation: "Accelerate distributor credit note and physical pack replacement."
  },
  "Low Margin vs Competitor": {
    color: "#f59e0b",
    bgColor: "bg-amber-50/60",
    borderColor: "border-amber-200",
    badgeBg: "bg-amber-100",
    badgeText: "text-amber-800",
    category: "Commercial",
    icon: DollarSign,
    recommendation: "Introduce volume combo schemes against local drink brands."
  },
  "Stock Unavailable at Distributor": {
    color: "#8b5cf6",
    bgColor: "bg-purple-50/60",
    borderColor: "border-purple-200",
    badgeBg: "bg-purple-100",
    badgeText: "text-purple-700",
    category: "Supply Chain",
    icon: PackageX,
    recommendation: "Prioritize replenishment of high-velocity ₹35 Butter & beverage cans."
  },
  "Slow Seasonal Movement (Rain)": {
    color: "#0284c7",
    bgColor: "bg-sky-50/60",
    borderColor: "border-sky-200",
    badgeBg: "bg-sky-100",
    badgeText: "text-sky-700",
    category: "Weather",
    icon: CloudRain,
    recommendation: "Shift focus toward ambient staples, paneer, and long shelf-life dairy."
  },
  "No Refrigerator Space": {
    color: "#0d9488",
    bgColor: "bg-teal-50/60",
    borderColor: "border-teal-200",
    badgeBg: "bg-teal-100",
    badgeText: "text-teal-700",
    category: "Infrastructure",
    icon: Snowflake,
    recommendation: "Provide branded counter-top chillers or push ambient display racks."
  }
};

const DEFAULT_META = {
  color: "#ff385c",
  bgColor: "bg-gray-50",
  borderColor: "border-gray-200",
  badgeBg: "bg-gray-100",
  badgeText: "text-gray-700",
  category: "Field Feedback",
  icon: AlertTriangle,
  recommendation: "Follow up with retailer to address specific trade concern."
};

export default function ObjectionVisualizer({
  data,
  title = "Top Retailer Objections & Bottlenecks",
  subtitle = "Granular root-cause analysis of non-converted field pitches"
}: ObjectionVisualizerProps) {
  const totalCount = useMemo(() => {
    return data.reduce((sum, item) => sum + item.value, 0);
  }, [data]);

  if (!data || data.length === 0 || totalCount === 0) {
    return (
      <div className="bg-white border border-[#dddddd] rounded-[16px] p-6 shadow-sm flex items-center justify-center text-[#717171] h-full min-h-[380px]">
        No objection data recorded for current filter
      </div>
    );
  }

  return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-6 shadow-sm flex flex-col justify-between h-full">
      {/* Header */}
      <div>
        <div className="flex items-start justify-between gap-3 mb-2">
          <div>
            <h3 className="text-[17px] font-bold text-[#222222] tracking-tight">{title}</h3>
            <p className="text-xs text-[#717171] mt-0.5">{subtitle}</p>
          </div>
          <span className="shrink-0 text-xs font-bold text-[#222222] bg-[#f7f7f7] border border-[#dddddd] px-2.5 py-1 rounded-full">
            {totalCount.toLocaleString()} Pitches
          </span>
        </div>

        {/* Multi-segment Distribution Bar */}
        <div className="mt-4 mb-5">
          <div className="h-3 w-full rounded-full overflow-hidden flex bg-[#f0f0f0] gap-0.5 p-0.5 border border-[#e5e5e5]">
            {data.map((item, idx) => {
              const meta = OBJECTION_METADATA[item.name] || DEFAULT_META;
              const pct = (item.value / totalCount) * 100;
              if (pct < 1) return null;
              return (
                <div
                  key={idx}
                  style={{ width: `${pct}%`, backgroundColor: meta.color }}
                  className="h-full first:rounded-l-full last:rounded-r-full transition-all duration-500 hover:opacity-90"
                  title={`${item.name}: ${item.value} pitches (${pct.toFixed(1)}%)`}
                />
              );
            })}
          </div>
          <div className="flex items-center justify-between text-[11px] text-[#717171] mt-1.5 px-0.5">
            <span>Distribution Share</span>
            <span>100% Total Volume</span>
          </div>
        </div>
      </div>

      {/* Ranked Modern List */}
      <div className="space-y-3 flex-1 overflow-y-auto max-h-[320px] pr-1 custom-scrollbar">
        {data.map((item, idx) => {
          const meta = OBJECTION_METADATA[item.name] || DEFAULT_META;
          const Icon = meta.icon;
          const sharePct = ((item.value / totalCount) * 100).toFixed(1);

          return (
            <div
              key={idx}
              className={`p-3.5 rounded-[12px] border ${meta.borderColor} ${meta.bgColor} transition-all hover:shadow-sm`}
            >
              {/* Row Header */}
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2.5 min-w-0">
                  <div
                    className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0"
                    style={{ backgroundColor: `${meta.color}15`, color: meta.color }}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="font-bold text-[#222222] text-xs sm:text-sm truncate">
                    {item.name}
                  </span>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${meta.badgeBg} ${meta.badgeText}`}>
                    {meta.category}
                  </span>
                  <span className="text-xs font-bold text-[#222222]">
                    {item.value} <span className="text-[11px] font-normal text-[#717171]">({sharePct}%)</span>
                  </span>
                </div>
              </div>

              {/* Progress Track */}
              <div className="w-full bg-black/5 h-1.5 rounded-full overflow-hidden my-2">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{ width: `${sharePct}%`, backgroundColor: meta.color }}
                />
              </div>

              {/* Actionable Field Recommendation */}
              <p className="text-[11px] text-[#555555] leading-relaxed flex items-center gap-1.5 mt-1">
                <Sparkles className="w-3 h-3 text-[#ff385c] shrink-0" />
                <span>{meta.recommendation}</span>
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
