import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { testService } from '../services/testService';
import type { TestResult } from '../types/perfume.types';
import OlfactoryRadarChart from '../components/OlfactoryRadarChart';
import ShareButton from '../components/ShareButton';
import './ResultsPage.css';

const ResultsPage = () => {
    const { testId } = useParams<{ testId: string }>();
    const navigate = useNavigate();
    const [result, setResult] = useState<TestResult | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchResults = async () => {
            if (!testId) {
                setError('ID de test no válido');
                setLoading(false);
                return;
            }

            try {
                const data = await testService.getTestResult(testId);
                setResult(data);
            } catch (err: any) {
                console.error('Error fetching results:', err);
                setError('Error al cargar los resultados');
            } finally {
                setLoading(false);
            }
        };

        fetchResults();
    }, [testId]);

    const getAffinityColor = (score: number) => {
        if (score >= 80) return '#10b981';
        if (score >= 60) return '#6366f1';
        if (score >= 40) return '#f59e0b';
        return '#94a3b8';
    };

    if (loading) {
        return (
            <div className="results-page loading">
                <div className="loader">Cargando resultados...</div>
            </div>
        );
    }

    if (error || !result) {
        return (
            <div className="results-page error">
                <div className="error-container">
                    <h2>😕 Error</h2>
                    <p>{error || 'No se encontraron resultados'}</p>
                    <button className="btn-primary" onClick={() => navigate('/')}>
                        Volver al inicio
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="results-page">
            <div className="container">
                <motion.div
                    className="results-header"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <h1>✨ Tus Resultados</h1>
                    <p>Basado en tus preferencias, estos son los perfumes con mayor afinidad:</p>
                    <div className="share-button-wrapper">
                        <ShareButton
                            testId={result.test_id}
                            topPerfumeName={result.results[0]?.perfume.name}
                        />
                    </div>
                </motion.div>

                {/* Radar Chart - Olfactory Profile */}
                {result.olfactory_profile && (
                    <OlfactoryRadarChart profile={result.olfactory_profile} />
                )}

                <div className="results-grid">
                    {result.results.map((item, index) => (
                        <motion.div
                            key={item.perfume.id}
                            className="perfume-card"
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.2 }}
                        >
                            {index === 0 && <div className="best-match-badge">🏆 Mejor Match</div>}

                            {item.perfume.image_url && (
                                <div className="perfume-image">
                                    <img src={item.perfume.image_url} alt={item.perfume.name} />
                                </div>
                            )}

                            <div className="perfume-info">
                                <h3 className="perfume-name">{item.perfume.name}</h3>
                                <p className="perfume-brand">{item.perfume.brand}</p>

                                <div className="affinity-score-container">
                                    <div className="affinity-score">
                                        <span
                                            className="score-number"
                                            style={{ color: getAffinityColor(item.affinity.score) }}
                                        >
                                            {item.affinity.score.toFixed(0)}%
                                        </span>
                                        <span className="score-label">Afinidad</span>
                                    </div>
                                    <div className="affinity-bar">
                                        <motion.div
                                            className="affinity-fill"
                                            initial={{ width: 0 }}
                                            animate={{ width: `${item.affinity.score}%` }}
                                            transition={{ duration: 1, delay: index * 0.2 + 0.3 }}
                                            style={{ backgroundColor: getAffinityColor(item.affinity.score) }}
                                        />
                                    </div>
                                </div>

                                <div className="description-section">
                                    <h4>📝 Descripción</h4>
                                    <p>{item.affinity.description}</p>
                                </div>

                                <div className="recommendation-section">
                                    <h4>💡 Cuándo usarlo</h4>
                                    <p>{item.affinity.recommendation}</p>
                                </div>

                                {item.perfume.purchase_url && (
                                    <a
                                        href={item.perfume.purchase_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="btn-purchase"
                                    >
                                        Ver en tienda →
                                    </a>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>

                <motion.div
                    className="footer-actions"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8 }}
                >
                    <button className="btn-secondary" onClick={() => navigate('/')}>
                        ← Volver al inicio
                    </button>
                    <button className="btn-primary" onClick={() => navigate('/test')}>
                        Hacer otro test
                    </button>
                </motion.div>

                <div className="disclaimer-box">
                    <p>
                        <strong>Recuerda:</strong> Estos resultados son predicciones basadas en IA.
                        La experiencia olfativa es única para cada persona. Te recomendamos solicitar
                        una muestra antes de realizar la compra.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ResultsPage;
