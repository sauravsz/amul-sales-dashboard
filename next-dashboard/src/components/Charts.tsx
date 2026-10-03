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
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px] flex items-center justify-center text-muted">
      No data available
    </div>
  );
  
  return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px]">
      <h3 className="text-[16px] font-bold text-ink mb-4">Daily Outlets Visited vs Converted</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ebebeb" />
          <XAxis 
            dataKey="date" 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6a6a6a', fontSize: 11 }} 
            dy={10}
            tickFormatter={(val: string) => val.slice(5)}
          />
          <YAxis 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6a6a6a', fontSize: 12 }}
          />
          <RechartsTooltip 
            cursor={{ fill: '#f7f7f7' }}
            contentStyle={{ borderRadius: '8px', border: '1px solid #dddddd', boxShadow: 'rgba(0, 0, 0, 0.04) 0 2px 6px 0', padding: '12px' }}
            itemStyle={{ color: '#222222', fontSize: '14px', fontWeight: 600 }}
          />
          <Legend iconType="circle" wrapperStyle={{ fontSize: '12px', color: '#6a6a6a', paddingTop: '10px' }} />
          <Bar dataKey="pitches" fill="#dddddd" name="Visited" radius={[4, 4, 0, 0]} maxBarSize={30} />
          <Bar dataKey="orders" fill="#ff385c" name="Orders Converted" radius={[4, 4, 0, 0]} maxBarSize={30} />
        </BarChart>
      </ResponsiveContainer>
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
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px] flex items-center justify-center text-muted">
      No data available
    </div>
  );
  
  return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px]">
      <h3 className="text-[16px] font-bold text-ink mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#ebebeb" />
          <XAxis 
            type="number"
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6a6a6a', fontSize: 12 }}
            domain={[0, 100]}
          />
          <YAxis 
            dataKey={xKey} 
            type="category" 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#222222', fontSize: 12, fontWeight: 500 }}
            width={140}
          />
          <RechartsTooltip 
            cursor={{ fill: 'transparent' }}
            contentStyle={{ borderRadius: '8px', border: '1px solid #dddddd', boxShadow: 'rgba(0, 0, 0, 0.04) 0 2px 6px 0', padding: '12px' }}
            itemStyle={{ color: '#222222', fontSize: '14px', fontWeight: 600 }}
            formatter={(val: unknown) => [`${typeof val === 'number' ? val.toFixed(1) : Number(val || 0).toFixed(1)}%`, 'Conversion Rate']}
          />
          <Bar 
            dataKey={yKey} 
            fill="#ff385c" 
            radius={[0, 4, 4, 0]} 
            barSize={20} 
            background={{ fill: '#f7f7f7', radius: 4 }}
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={index === 0 ? '#ff385c' : '#e00b41'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface GenericBarMetricChartProps {
  data: Array<{ name: string; value: number; color?: string }>;
  title: string;
  unit?: string;
}

export function GenericBarMetricChart({ data, title, unit = '' }: GenericBarMetricChartProps) {
  if (!data || data.length === 0) return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[360px] flex items-center justify-center text-muted">
      No data available
    </div>
  );

  return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[360px]">
      <h3 className="text-[16px] font-bold text-ink mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 20, left: -10, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ebebeb" />
          <XAxis 
            dataKey="name" 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6a6a6a', fontSize: 11 }}
            interval={0}
            angle={-25}
            textAnchor="end"
          />
          <YAxis 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6a6a6a', fontSize: 12 }}
          />
          <RechartsTooltip 
            cursor={{ fill: '#f7f7f7' }}
            contentStyle={{ borderRadius: '8px', border: '1px solid #dddddd', boxShadow: 'rgba(0, 0, 0, 0.04) 0 2px 6px 0', padding: '12px' }}
            itemStyle={{ color: '#222222', fontSize: '14px', fontWeight: 600 }}
            formatter={(val: unknown) => [`${val}${unit}`, title]}
          />
          <Bar dataKey="value" fill="#ff385c" radius={[4, 4, 0, 0]} maxBarSize={36}>
            {data.map((entry, index) => (
              <Cell key={`bar-${index}`} fill={entry.color || '#ff385c'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
