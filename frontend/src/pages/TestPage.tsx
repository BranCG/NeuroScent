import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { TEST_QUESTIONS } from '../utils/testQuestions';
import type { TestAnswers } from '../types/test.types';
import { testService } from '../services/testService';
import './TestPage.css';

const TestPage = () => {
    const navigate = useNavigate();
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [answers, setAnswers] = useState<Partial<TestAnswers>>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const question = TEST_QUESTIONS[currentQuestion];
    const progress = ((currentQuestion + 1) / TEST_QUESTIONS.length) * 100;

    const handleAnswer = (value: any) => {
        if (question.type === 'multiple') {
            const currentValues = (answers[question.id as keyof TestAnswers] as string[]) || [];
            const newValues = currentValues.includes(value)
                ? currentValues.filter(v => v !== value)
                : [...currentValues, value];

            setAnswers({ ...answers, [question.id]: newValues });
        } else {
            setAnswers({ ...answers, [question.id]: value });
        }
    };

    const handleNext = async () => {
        if (currentQuestion < TEST_QUESTIONS.length - 1) {
            setCurrentQuestion(currentQuestion + 1);
        } else {
            // Submit test
            await handleSubmit();
        }
    };

    const handleBack = () => {
        if (currentQuestion > 0) {
            setCurrentQuestion(currentQuestion - 1);
        }
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError(null);

        try {
            // Generate session ID
            const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

            const testData: TestAnswers = {
                ...answers,
                session_id: sessionId,
            } as TestAnswers;

            const result = await testService.calculateAffinity(testData);
            navigate(`/results/${result.test_id}`);
        } catch (err: any) {
            console.error('Error submitting test:', err);
            setError(err.response?.data?.detail?.message || 'Error al procesar el test. Por favor intenta de nuevo.');
            setLoading(false);
        }
    };

    const canProceed = () => {
        const answer = answers[question.id as keyof TestAnswers];

        if (!question.required) return true;
        if (!answer) return false;

        if (question.type === 'multiple') {
            return Array.isArray(answer) && answer.length > 0;
        }

        return true;
    };

    return (
        <div className="test-page">
            <div className="test-container">
                <div className="test-header">
                    <h2>Test Sensorial NeuroScent</h2>
                    <p>Pregunta {currentQuestion + 1} de {TEST_QUESTIONS.length}</p>
                </div>

                <div className="progress-bar">
                    <motion.div
                        className="progress-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.3 }}
                    />
                </div>

                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentQuestion}
                        className="question-container"
                        initial={{ opacity: 0, x: 50 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -50 }}
                        transition={{ duration: 0.3 }}
                    >
                        <h3 className="question-text">{question.text}</h3>

                        <div className="options-container">
                            {question.type === 'scale' && question.options && (
                                <div className="scale-options">
                                    {question.options.map((option) => (
                                        <button
                                            key={option.value as string}
                                            className={`scale-option ${answers[question.id as keyof TestAnswers] === option.value ? 'selected' : ''
                                                }`}
                                            onClick={() => handleAnswer(option.value)}
                                        >
                                            <span className="option-value">{option.value}</span>
                                            <span className="option-label">{option.label}</span>
                                        </button>
                                    ))}
                                </div>
                            )}

                            {(question.type === 'single' || question.type === 'multiple') && question.options && (
                                <div className="choice-options">
                                    {question.options.map((option) => {
                                        const currentAnswers = answers[question.id as keyof TestAnswers];
                                        const isSelected = question.type === 'multiple'
                                            ? Array.isArray(currentAnswers) && currentAnswers.includes(option.value as string)
                                            : currentAnswers === option.value;

                                        return (
                                            <button
                                                key={option.value as string}
                                                className={`choice-option ${isSelected ? 'selected' : ''}`}
                                                onClick={() => handleAnswer(option.value)}
                                            >
                                                {option.label}
                                                {isSelected && <span className="checkmark">✓</span>}
                                            </button>
                                        );
                                    })}
                                </div>
                            )}

                            {question.type === 'text' && (
                                <input
                                    type="text"
                                    className="text-input"
                                    placeholder="Escribe tu respuesta..."
                                    value={(answers[question.id as keyof TestAnswers] as string) || ''}
                                    onChange={(e) => handleAnswer(e.target.value)}
                                />
                            )}
                        </div>

                        {error && (
                            <div className="error-message">
                                {error}
                            </div>
                        )}
                    </motion.div>
                </AnimatePresence>

                <div className="navigation-buttons">
                    <button
                        className="btn-secondary"
                        onClick={handleBack}
                        disabled={currentQuestion === 0 || loading}
                    >
                        ← Anterior
                    </button>

                    <button
                        className="btn-primary"
                        onClick={handleNext}
                        disabled={!canProceed() || loading}
                    >
                        {loading ? (
                            'Procesando...'
                        ) : currentQuestion === TEST_QUESTIONS.length - 1 ? (
                            'Ver Resultados'
                        ) : (
                            'Siguiente →'
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default TestPage;
