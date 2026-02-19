export interface SensrClientOptions {
  apiKey: string;
  baseUrl?: string;
  /** Additional headers for integration contexts (e.g., OAuth tokens). */
  headers?: Record<string, string>;
}

export interface SensrPagination {
  next_cursor?: string | null;
}

export interface SensrPaginatedResponse<T> {
  data: T[];
  pagination?: SensrPagination;
}

// --- Sensr domain models (best-effort based on typical wearable APIs) ---

export interface SensrBiometric {
  id: string;
  user_id: string;
  type:
    | 'heart_rate'
    | 'hrv'
    | 'spo2'
    | 'respiration_rate'
    | 'blood_pressure'
    | 'temperature'
    | string;
  timestamp_ms: number;
  // common numeric value
  value?: number;
  unit?: string;
  // HRV specifics
  hrv?: {
    rmssd_ms?: number;
    sdnn_ms?: number;
    pnn50?: number;
  };
  // BP specifics
  blood_pressure?: {
    systolic_mmhg: number;
    diastolic_mmhg: number;
  };
}

export interface SensrSleepSummary {
  user_id: string;
  date: string; // ISO date (YYYY-MM-DD)
  start_time_ms?: number;
  end_time_ms?: number;
  total_sleep_minutes?: number;
  time_in_bed_minutes?: number;
  awake_minutes?: number;
  light_sleep_minutes?: number;
  deep_sleep_minutes?: number;
  rem_sleep_minutes?: number;
}

export interface SensrSleepEpisodeSegment {
  start_time_ms: number;
  end_time_ms: number;
  stage: 'awake' | 'light' | 'deep' | 'rem' | 'in_bed' | string;
}

export interface SensrSleepDetailsDay {
  user_id: string;
  date: string;
  start_time_ms: number;
  end_time_ms: number;
  segments: SensrSleepEpisodeSegment[];
}

export interface SensrActivity {
  id: string;
  user_id: string;
  start_time_ms: number;
  end_time_ms: number;
  type: string;
  name?: string;
  steps?: number;
  distance_m?: number;
  calories_kcal?: number;
}

export interface SensrCalorieDetailsBucket {
  start_time_ms: number;
  end_time_ms: number;
  calories_kcal: number;
}

export interface SensrCalorieDetailsResponse {
  user_id: string;
  granularity: 'day' | 'week' | 'month' | 'year' | string;
  buckets: SensrCalorieDetailsBucket[];
}

export interface SensrVitals {
  user_id: string;
  timestamp_ms: number;
  resting_heart_rate?: number;
  respiration_rate?: number;
  spo2?: number;
  temperature_c?: number;
}

export class SensrClient {
  private readonly baseUrl: string;
  private readonly apiKey: string;
  private readonly headers: Record<string, string>;

  constructor(opts: SensrClientOptions) {
    this.apiKey = opts.apiKey;
    this.baseUrl = (opts.baseUrl ?? 'https://api.getsensr.io').replace(/\/$/, '');
    this.headers = opts.headers ?? {};
  }

  private async request<T>(path: string, query?: Record<string, string | number | boolean | undefined>): Promise<T> {
    const url = new URL(this.baseUrl + path);
    if (query) {
      for (const [k, v] of Object.entries(query)) {
        if (v === undefined) continue;
        url.searchParams.set(k, String(v));
      }
    }

    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'X-API-KEY': this.apiKey,
        ...this.headers
      }
    });

    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(`Sensr API error ${res.status} ${res.statusText} for ${url.toString()} ${text ? `: ${text}` : ''}`);
    }

    return (await res.json()) as T;
  }

  private async *paginate<T>(path: string, query: Record<string, string | number | boolean | undefined>): AsyncGenerator<T> {
    let cursor: string | undefined = undefined;
    // common cursor key names used by APIs
    while (true) {
      const page: SensrPaginatedResponse<T> = await this.request<SensrPaginatedResponse<T>>(path, { ...query, cursor });
      for (const item of page.data) yield item;
      const next: string | null = page.pagination?.next_cursor ?? null;
      if (!next) break;
      cursor = next;
    }
  }

  async getBiometrics(params: {
    userId: string;
    startTimeMs?: number;
    endTimeMs?: number;
    limit?: number;
  }): Promise<SensrBiometric[]> {
    const out: SensrBiometric[] = [];
    for await (const item of this.paginate<SensrBiometric>('/v1/biometrics', {
      user_id: params.userId,
      start_time_ms: params.startTimeMs,
      end_time_ms: params.endTimeMs,
      limit: params.limit ?? 200
    })) {
      out.push(item);
    }
    return out;
  }

  async getActivities(params: {
    userId: string;
    startTimeMs?: number;
    endTimeMs?: number;
    limit?: number;
  }): Promise<SensrActivity[]> {
    const out: SensrActivity[] = [];
    for await (const item of this.paginate<SensrActivity>('/v1/activities', {
      user_id: params.userId,
      start_time_ms: params.startTimeMs,
      end_time_ms: params.endTimeMs,
      limit: params.limit ?? 200
    })) {
      out.push(item);
    }
    return out;
  }

  async getSleep(params: { userId: string; date: string }): Promise<SensrSleepSummary> {
    return this.request<SensrSleepSummary>('/v1/sleep', { user_id: params.userId, date: params.date });
  }

  async getSleepDetailsDay(params: { userId: string; date: string }): Promise<SensrSleepDetailsDay> {
    return this.request<SensrSleepDetailsDay>('/v1/sleep/details/day', {
      user_id: params.userId,
      date: params.date
    });
  }

  async getSleepDetailsGranular(params: {
    userId: string;
    granularity: 'week' | 'month' | 'year';
    startDate: string;
    endDate: string;
  }): Promise<unknown> {
    return this.request('/v1/sleep/details/granular', {
      user_id: params.userId,
      granularity: params.granularity,
      start_date: params.startDate,
      end_date: params.endDate
    });
  }

  async getCalorieDetails(params: {
    userId: string;
    granularity: 'day' | 'week' | 'month' | 'year';
    startDate: string;
    endDate: string;
  }): Promise<SensrCalorieDetailsResponse> {
    return this.request<SensrCalorieDetailsResponse>('/v1/calorie/details', {
      user_id: params.userId,
      granularity: params.granularity,
      start_date: params.startDate,
      end_date: params.endDate
    });
  }

  async getScores(params: { userId: string; date: string }): Promise<unknown> {
    return this.request('/v1/scores', { user_id: params.userId, date: params.date });
  }

  async getRecoveryScoreDetails(params: {
    userId: string;
    granularity: 'week' | 'month' | 'year';
    startDate: string;
    endDate: string;
  }): Promise<unknown> {
    return this.request('/v1/scores/recovery/details', {
      user_id: params.userId,
      granularity: params.granularity,
      start_date: params.startDate,
      end_date: params.endDate
    });
  }

  async getInsights(params: { userId: string; date: string }): Promise<unknown> {
    return this.request('/v1/insights', { user_id: params.userId, date: params.date });
  }

  async getVitals(params: {
    userId: string;
    startTimeMs?: number;
    endTimeMs?: number;
    limit?: number;
  }): Promise<SensrVitals[]> {
    const out: SensrVitals[] = [];
    for await (const item of this.paginate<SensrVitals>('/v1/vitals', {
      user_id: params.userId,
      start_time_ms: params.startTimeMs,
      end_time_ms: params.endTimeMs,
      limit: params.limit ?? 200
    })) {
      out.push(item);
    }
    return out;
  }

  async getVitalsDetailsGranular(params: {
    userId: string;
    granularity: 'week' | 'month' | 'year';
    startDate: string;
    endDate: string;
  }): Promise<unknown> {
    return this.request('/v1/vitals/details/granular', {
      user_id: params.userId,
      granularity: params.granularity,
      start_date: params.startDate,
      end_date: params.endDate
    });
  }
}
