'use client';
import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  Legend, Cell
} from 'recharts';
import type { DailyTrendItem, ConversionItem } from '@/types/sales';

interface DailyTrendChartProps {
  data: DailyTrendItem[];
}

export function DailyTrendChart({ data }: DailyTrendChartProps) {
  if (!data || data.length === 0) return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-6 shadow-xs h-[340px] sm:h-[420px] flex items-center justify-center text-[#717171]">
      No visit data available
    </div>
  );
  
  return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-4 sm:p-6 shadow-xs h-[340px] sm:h-[420px] flex flex-col justify-between">
      <div className="mb-2">
        <h3 className="text-[15px] sm:text-[17px] font-bold text-[#222222]">Daily Outlets Visited vs Orders Converted</h3>
        <p className="text-[11px] sm:text-xs text-[#717171] mt-0.5">Track field conversion velocity across market visit dates</p>
      </div>
      <div className="flex-1 w-full min-h-[220px] sm:min-h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 10, left: -25, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis 
              dataKey="date" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#717171', fontSize: 10 }} 
              dy={6}
              tickFormatter={(val: string) => {
                const parts = val.split('-');
                return parts.length === 3 ? `${parts[2]}/${parts[1]}` : val;
              }}
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#717171', fontSize: 11 }}
            />
            <RechartsTooltip 
              cursor={{ fill: '#f7f7f7' }}
              contentStyle={{ borderRadius: '12px', border: '1px solid #dddddd', boxShadow: 'rgba(0, 0, 0, 0.08) 0 4px 12px', padding: '10px 14px', background: '#ffffff' }}
              labelStyle={{ fontWeight: 700, color: '#222222', marginBottom: '2px', fontSize: '12px' }}
              itemStyle={{ fontSize: '12px', padding: '1px 0' }}
            />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '11px', color: '#717171', paddingTop: '8px' }} />
            <Bar dataKey="pitches" fill="#e5e5e5" name="Visited" radius={[3, 3, 0, 0]} maxBarSize={24} />
            <Bar dataKey="orders" fill="#ff385c" name="Orders Converted" radius={[3, 3, 0, 0]} maxBarSize={24} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

interface ConversionBarChartProps {
  data: ConversionItem[];
  title: string;
  xKey: string;
  yKey: string;
}

export function ConversionBarChart({ data, title, xKey, yKey }: ConversionBarChartProps) {
  if (!data || data.length === 0) return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-6 shadow-xs h-[340px] sm:h-[420px] flex items-center justify-center text-[#717171]">
      No product conversion data available
    </div>
  );
  
  return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-4 sm:p-6 shadow-xs h-[340px] sm:h-[420px] flex flex-col justify-between">
      <div className="mb-2">
        <h3 className="text-[15px] sm:text-[17px] font-bold text-[#222222]">{title}</h3>
        <p className="text-[11px] sm:text-xs text-[#717171] mt-0.5">Conversion strike rate across focus SKUs (≥5 pitches)</p>
      </div>
      <div className="flex-1 w-full min-h-[220px] sm:min-h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f0f0f0" />
            <XAxis 
              type="number"
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#717171', fontSize: 11 }}
              domain={[0, 100]}
              unit="%"
            />
            <YAxis 
              dataKey={xKey} 
              type="category" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#222222', fontSize: 11, fontWeight: 500 }}
              width={125}
            />
            <RechartsTooltip 
              cursor={{ fill: 'transparent' }}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const entry = payload[0].payload as ConversionItem;
                  return (
                    <div className="bg-white border border-[#dddddd] rounded-[12px] p-2.5 shadow-lg text-xs">
                      <div className="font-bold text-[#222222] mb-0.5">{entry.name}</div>
                      <div className="text-[#ff385c] font-bold text-xs sm:text-sm">{entry.rate}% Conversion</div>
                      <div className="text-[#717171] mt-0.5 text-[11px]">
                        {entry.orders} booked / {entry.pitches} pitched
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Bar 
              dataKey={yKey} 
              fill="#ff385c" 
              radius={[0, 4, 4, 0]} 
              barSize={18} 
              background={{ fill: '#f7f7f7', radius: 4 }}
            >
              {data.map((_, index) => (
                <Cell key={`cell-${index}`} fill={index === 0 ? '#ff385c' : index === 1 ? '#e00b41' : '#ff5a5f'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

interface GenericBarMetricChartProps {
  data: Array<{ name: string; value: number; color?: string }>;
  title: string;
  unit?: string;
  subtitle?: string;
}

export function GenericBarMetricChart({ data, title, unit = '', subtitle }: GenericBarMetricChartProps) {
  if (!data || data.length === 0) return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-6 shadow-xs h-[340px] flex items-center justify-center text-[#717171]">
      No data available
    </div>
  );

  return (
    <div className="bg-white border border-[#dddddd] rounded-[16px] p-4 sm:p-6 shadow-xs h-[340px] flex flex-col justify-between">
      <div>
        <h3 className="text-[15px] sm:text-[17px] font-bold text-[#222222]">{title}</h3>
        {subtitle && <p className="text-[11px] sm:text-xs text-[#717171] mt-0.5">{subtitle}</p>}
      </div>
      <div className="flex-1 w-full min-h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis 
              dataKey="name" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#717171', fontSize: 10 }}
              interval={0}
              angle={-20}
              textAnchor="end"
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#717171', fontSize: 11 }}
            />
            <RechartsTooltip 
              cursor={{ fill: '#f7f7f7' }}
              contentStyle={{ borderRadius: '12px', border: '1px solid #dddddd', boxShadow: 'rgba(0, 0, 0, 0.08) 0 4px 12px', padding: '10px 14px', background: '#ffffff' }}
              formatter={(val: unknown) => [`${val}${unit}`, title]}
            />
            <Bar dataKey="value" fill="#ff385c" radius={[4, 4, 0, 0]} maxBarSize={28}>
              {data.map((entry, index) => (
                <Cell key={`bar-${index}`} fill={entry.color || (index === 0 ? '#ff385c' : '#717171')} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
