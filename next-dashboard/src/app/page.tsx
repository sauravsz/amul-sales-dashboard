import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';
import Dashboard from '@/components/Dashboard';
import type { SalesRecord, SauravDataset } from '@/types/sales';

export default async function Home() {
  const possibleCsvPaths = [
    path.join(process.cwd(), 'data', 'raw', 'field_sales_log.csv'),
    path.join(process.cwd(), '..', 'data', 'raw', 'field_sales_log.csv'),
  ];
  
  const possibleJsonPaths = [
    path.join(process.cwd(), 'public', 'data', 'saurav_data.json'),
    path.join(process.cwd(), 'data', 'raw', 'saurav_daily_reports.json'),
  ];
  
  let data: SalesRecord[] = [];
  let dataset: SauravDataset | null = null;
  
  for (const p of possibleCsvPaths) {
    if (fs.existsSync(p)) {
      try {
        const fileContent = fs.readFileSync(p, 'utf-8');
        const parsed = Papa.parse<SalesRecord>(fileContent, { header: true, skipEmptyLines: true });
        data = parsed.data;
        break;
      } catch (error) {
        console.error("Failed to load CSV from", p, error);
      }
    }
  }

  for (const p of possibleJsonPaths) {
    if (fs.existsSync(p)) {
      try {
        const jsonContent = fs.readFileSync(p, 'utf-8');
        dataset = JSON.parse(jsonContent) as SauravDataset;
        break;
      } catch (error) {
        console.error("Failed to load JSON dataset from", p, error);
      }
    }
  }

  return (
    <main className="min-h-screen bg-canvas pb-24">
      <Dashboard rawData={data} dataset={dataset} />
    </main>
  );
}
