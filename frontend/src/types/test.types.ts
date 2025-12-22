// Test related types
export interface TestAnswers {
  q1_intensity: number;
  q2_preferred_families: string[];
  q3_rejected_families: string[];
  q4_emotion: string;
  q5_time_of_day: string[];
  q6_occasions: string[];
  q7_season: string;
  q8_longevity: number;
  q9_concentration?: string;
  q10_reference?: string;
  session_id: string;
}

export interface Question {
  id: string;
  type: 'scale' | 'multiple' | 'single' | 'text';
  text: string;
  options?: Array<{
    value: string | number;
    label: string;
  }>;
  multiple?: boolean;
  min?: number;
  max?: number;
  required: boolean;
}
