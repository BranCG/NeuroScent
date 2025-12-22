import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import './LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();

    const handleStartTest = () => {
        navigate('/test');
    };

    return (
        <div className="landing-page">
            <div className="container">
                <motion.div
                    className="hero"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <h1 className="hero-title">
                        <span className="gradient-text">NeuroScent</span>
                    </h1>
                    <p className="hero-subtitle">
                        Encuentra el perfume perfecto para ti
                    </p>
                    <p className="hero-description">
                        Nuestro sistema de inteligencia artificial analiza tus preferencias sensoriales
                        para recomendarte fragancias con alta afinidad a tu perfil olfativo.
                    </p>

                    <motion.button
                        className="cta-button"
                        onClick={handleStartTest}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        Comenzar Test
                        <span className="button-icon">→</span>
                    </motion.button>

                    <div className="info-cards">
                        <motion.div
                            className="info-card"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.3 }}
                        >
                            <div className="info-icon">⏱️</div>
                            <h3>2-3 minutos</h3>
                            <p>Test rápido y sencillo</p>
                        </motion.div>

                        <motion.div
                            className="info-card"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.4 }}
                        >
                            <div className="info-icon">🧠</div>
                            <h3>IA Avanzada</h3>
                            <p>Análisis de afinidad sensorial</p>
                        </motion.div>

                        <motion.div
                            className="info-card"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.5 }}
                        >
                            <div className="info-icon">✨</div>
                            <h3>Personalizado</h3>
                            <p>Recomendaciones únicas</p>
                        </motion.div>
                    </div>

                    <div className="disclaimer">
                        <p>
                            💡 <strong>Nota:</strong> Este análisis predice tu afinidad con perfumes basándose
                            en tus preferencias. La experiencia olfativa es única para cada persona.
                            Recomendamos solicitar una muestra antes de comprar.
                        </p>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default LandingPage;
