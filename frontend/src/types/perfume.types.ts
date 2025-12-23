// Perfume related types
export interface Perfume {
    id: string;
    name: string;
    brand: string;
    description?: string;
    image_url?: string;
    purchase_url?: string;
}

export interface AffinityResult {
    perfume: Perfume;
    affinity: {
        score: number;
        level: 'excellent' | 'good' | 'moderate' | 'low';
        description: string;
        recommendation: string;
    };
}

export interface OlfactoryProfile {
    id: string;
    intensity: number;
    citrus: number;
    floral: number;
    woody: number;
    sweet: number;
    spicy: number;
    green: number;
    aquatic: number;
    emotion?: string;
    season?: string;
}

export interface TestResult {
    test_id: string;
    user_id: string;
    profile_id: string;
    olfactory_profile?: OlfactoryProfile;
    results: AffinityResult[];
    metadata: {
        total_perfumes_analyzed: number;
        top_match_count: number;
        test_completed_at: string;
    };
}

