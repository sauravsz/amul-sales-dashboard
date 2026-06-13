import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  Legend
} from 'recharts';

export function DailyTrendChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px] flex items-center justify-center text-muted">
      No data available
    </div>
  );
  
  return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px]">
      <h3 className="text-[16px] font-bold text-ink mb-4">Daily Pitches vs Orders</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ebebeb" />
          <XAxis 
            dataKey="date" 
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6a6a6a', fontSize: 12 }} 
            dy={10}
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
          <Bar dataKey="pitches" fill="#dddddd" name="Pitches" radius={[4, 4, 0, 0]} maxBarSize={40} />
          <Bar dataKey="orders" fill="#10B981" name="Orders" radius={[4, 4, 0, 0]} maxBarSize={40} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function ConversionBarChart({ data, title, xKey, yKey }: { data: any[], title: string, xKey: string, yKey: string }) {
  if (!data || data.length === 0) return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px] flex items-center justify-center text-muted">
      No data available
    </div>
  );
  
  return (
    <div className="bg-canvas border border-hairline rounded-[14px] p-6 shadow-airbnb h-[400px]">
      <h3 className="text-[16px] font-bold text-ink mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
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
            tick={{ fill: '#6a6a6a', fontSize: 12 }}
            width={120}
          />
          <RechartsTooltip 
            cursor={{ fill: 'transparent' }}
            contentStyle={{ borderRadius: '8px', border: '1px solid #dddddd', boxShadow: 'rgba(0, 0, 0, 0.04) 0 2px 6px 0', padding: '12px' }}
            itemStyle={{ color: '#222222', fontSize: '14px', fontWeight: 600 }}
            formatter={(val: number) => [`${val.toFixed(1)}%`, 'Conversion Rate']}
          />
          <Bar 
            dataKey={yKey} 
            fill="#ff385c" 
            radius={[0, 4, 4, 0]} 
            barSize={24} 
            background={{ fill: '#f7f7f7', radius: [0, 4, 4, 0] }}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
