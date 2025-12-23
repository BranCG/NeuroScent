import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts';
import { motion } from 'framer-motion';
import './OlfactoryRadarChart.css';

interface OlfactoryProfile {
    citrus: number;
    floral: number;
    woody: number;
    sweet: number;
    spicy: number;
    green: number;
    aquatic: number;
}

interface OlfactoryRadarChartProps {
    profile: OlfactoryProfile;
}

const OlfactoryRadarChart = ({ profile }: OlfactoryRadarChartProps) => {
    // Transform profile data for Recharts
    const radarData = [
        { dimension: 'Cítrico', value: profile.citrus * 100, fullMark: 100 },
        { dimension: 'Floral', value: profile.floral * 100, fullMark: 100 },
        { dimension: 'Amaderado', value: profile.woody * 100, fullMark: 100 },
        { dimension: 'Dulce', value: profile.sweet * 100, fullMark: 100 },
        { dimension: 'Especiado', value: profile.spicy * 100, fullMark: 100 },
        { dimension: 'Verde', value: profile.green * 100, fullMark: 100 },
        { dimension: 'Acuático', value: profile.aquatic * 100, fullMark: 100 },
    ];

    return (
        <motion.div
            className="radar-chart-container"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
        >
            <h3 className="radar-title">🧬 Tu Perfil Olfativo</h3>
            <div className="radar-wrapper">
                <ResponsiveContainer width="100%" height={320}>
                    <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                        <defs>
                            <linearGradient id="radarGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stopColor="#a855f7" stopOpacity={0.9} />
                                <stop offset="50%" stopColor="#6366f1" stopOpacity={0.7} />
                                <stop offset="100%" stopColor="#06b6d4" stopOpacity={0.5} />
                            </linearGradient>
                            <linearGradient id="radarStroke" x1="0" y1="0" x2="1" y2="1">
                                <stop offset="0%" stopColor="#f472b6" />
                                <stop offset="50%" stopColor="#a855f7" />
                                <stop offset="100%" stopColor="#06b6d4" />
                            </linearGradient>
                        </defs>
                        <PolarGrid
                            stroke="rgba(255, 255, 255, 0.15)"
                            strokeDasharray="3 3"
                        />
                        <PolarAngleAxis
                            dataKey="dimension"
                            tick={{ fill: '#e2e8f0', fontSize: 12, fontWeight: 500 }}
                            tickLine={false}
                        />
                        <PolarRadiusAxis
                            angle={90}
                            domain={[0, 100]}
                            tick={{ fill: 'rgba(255,255,255,0.5)', fontSize: 10 }}
                            axisLine={false}
                            tickCount={5}
                        />
                        <Radar
                            name="Perfil"
                            dataKey="value"
                            stroke="url(#radarStroke)"
                            fill="url(#radarGradient)"
                            strokeWidth={2.5}
                            dot={{ fill: '#f472b6', strokeWidth: 0, r: 4 }}
                            activeDot={{ fill: '#fff', stroke: '#a855f7', strokeWidth: 2, r: 6 }}
                        />
                        <Tooltip
                            content={({ payload }) => {
                                if (payload && payload.length > 0) {
                                    const data = payload[0].payload;
                                    return (
                                        <div className="radar-tooltip">
                                            <span className="tooltip-label">{data.dimension}</span>
                                            <span className="tooltip-value">{Math.round(data.value)}%</span>
                                        </div>
                                    );
                                }
                                return null;
                            }}
                        />
                    </RadarChart>
                </ResponsiveContainer>
            </div>
            <p className="radar-description">
                Este gráfico muestra tus preferencias olfativas basadas en tus respuestas.
            </p>
        </motion.div>
    );
};

export default OlfactoryRadarChart;
