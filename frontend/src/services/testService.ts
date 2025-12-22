import api from './api';
import type { TestResult } from '../types/perfume.types';
import type { TestAnswers } from '../types/test.types';

export const testService = {
    /**
     * Submit test answers and calculate affinity
     */
    async calculateAffinity(answers: TestAnswers): Promise<TestResult> {
        const response = await api.post('/test/calculate', answers);
        return response.data.data;
    },

    /**
     * Get test result by ID
     */
    async getTestResult(testId: string): Promise<TestResult> {
        const response = await api.get(`/test/${testId}`);
        return response.data.data;
    },
};
