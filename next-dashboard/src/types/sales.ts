export interface SalesRecord {
  date: string;
  day?: string;
  week_no?: string;
  month?: string;
  distributor_name?: string;
  salesman_name?: string;
  intern_name?: string;
  beat_name?: string;
  area?: string;
  outlet_id?: string;
  outlet_name?: string;
  outlet_type?: string;
  outlet_size?: string;
  locality_type?: string;
  cold_storage_available?: string;
  high_footfall?: string;
  visited?: string;
  product_name?: string;
  product_group?: string;
  product_subgroup?: string;
  pitched?: string;
  availability_before_pitch?: string;
  display_visibility?: string;
  scheme_explained?: string;
  retailer_interest_level?: string;
  order_booked?: string;
  bill_cut?: string;
  pieces_ordered?: string | number;
  pieces_sold_if_known?: string | number;
  order_value_if_known?: string | number;
  competitor_present?: string;
  competitor_brand?: string;
  retailer_objection_raw?: string;
  retailer_objection_category?: string;
  follow_up_needed?: string;
  follow_up_priority?: string;
  follow_up_reason?: string;
  my_observation?: string;
}

export interface DailyReportItem {
  day_no: number;
  date: string;
  day_name: string;
  distributor: string;
  beat: string;
  salesman: string;
  visited: number;
  converted: number;
  conversion_rate: number;
  total_value: number;
  total_pieces: number;
  observations: string;
}

export interface SurveyResponseItem {
  survey_id: string;
  intern_name: string;
  beat_name: string;
  retailer_name: string;
  stocked_variants: string;
  top_demanded_product: string;
  weekly_sales_value: string;
  faces_stockouts: string;
  margin_satisfied: string;
  promotional_schemes_received: string;
  fastest_and_slowest_skus: string;
  competitors_stocked: string;
  highest_volume_brand: string;
  better_margin_brand: string;
  brand_loyalty: string;
  challenges: string;
  support_needed: string;
  remarks: string;
}

export interface ProductMasterItem {
  product_name: string;
  product_group: string;
  product_subgroup: string;
  mrp: number;
  ptr: number;
  retailer_margin_rs: number;
  margin_percent: number;
  pack_size: string;
  units_per_case: number;
}

export interface SauravDataset {
  intern: string;
  market: string;
  total_days: number;
  total_visits: number;
  total_converted: number;
  overall_strike_rate: number;
  daily_reports: DailyReportItem[];
  survey_responses: SurveyResponseItem[];
  products_master: ProductMasterItem[];
}

export interface DailyTrendItem {
  date: string;
  pitches: number;
  orders: number;
}

export interface ConversionItem {
  name: string;
  rate: number;
  pitches: number;
  orders: number;
  [key: string]: string | number;
}

export interface ObjectionItem {
  objection: string;
  count: number;
}

export interface BeatMetricItem {
  beat: string;
  distributor: string;
  days: number;
  visited: number;
  converted: number;
  conversionRate: number;
  totalValue: number;
}
