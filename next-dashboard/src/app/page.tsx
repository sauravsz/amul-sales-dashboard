import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';
import Dashboard from '@/components/Dashboard';

export default async function Home() {
  // Read CSV from the parent directory
  const csvPath = path.join(process.cwd(), '..', 'data', 'raw', 'field_sales_log.csv');
  let data = [];
  
  try {
    const fileContent = fs.readFileSync(csvPath, 'utf-8');
    const parsed = Papa.parse(fileContent, { header: true, skipEmptyLines: true });
    data = parsed.data;
  } catch (error) {
    console.error("Failed to load CSV", error);
  }

  return (
    <main className="min-h-screen bg-canvas pb-24">
      <Dashboard rawData={data} />
    </main>
  );
}
