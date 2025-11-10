import React, { useState, useEffect } from 'react';

const Home = () => {
    const [currentTime, setCurrentTime] = useState(new Date());
    const [userName, setUserName] = useState('');

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        // Buscar nome do usuário
        const userData = localStorage.getItem('userData');
        if (userData) {
            try {
                const user = JSON.parse(userData);
                setUserName(user.nome || '');
            } catch (error) {
                console.error('Erro ao carregar dados do usuário:', error);
            }
        }

        return () => clearInterval(timer);
    }, []);

    const getGreeting = () => {
        const hour = currentTime.getHours();
        if (hour >= 5 && hour < 12) return 'Bom dia';
        if (hour >= 12 && hour < 18) return 'Boa tarde';
        return 'Boa noite';
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <div style={styles.header}>
                    <h1 style={styles.title}>
                        {getGreeting()}{userName ? `, ${userName}` : ''}! 👋
                    </h1>
                    <p style={styles.subtitle}>Seja bem-vindo ao sistema</p>
                </div>

                <div style={styles.timeContainer}>
                    <div style={styles.timeBox}>
                        <h3 style={styles.timeLabel}>Data</h3>
                        <p style={styles.timeValue}>
                            {currentTime.toLocaleDateString('pt-BR', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                            })}
                        </p>
                    </div>
                    
                    <div style={styles.timeBox}>
                        <h3 style={styles.timeLabel}>Hora</h3>
                        <p style={styles.timeValue}>
                            {currentTime.toLocaleTimeString('pt-BR', {
                                hour: '2-digit',
                                minute: '2-digit',
                                second: '2-digit'
                            })}
                        </p>
                    </div>
                </div>

                <div style={styles.welcomeMessage}>
                    <p style={styles.messageText}>
                        🎉 Estamos felizes em tê-lo aqui! Utilize o menu para acessar as funcionalidades do sistema.
                    </p>
                </div>
            </div>
        </div>
    );
};

const styles = {
    container: {
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
    },
    card: {
        background: 'white',
        borderRadius: '20px',
        padding: '40px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        maxWidth: '600px',
        width: '100%',
        textAlign: 'center'
    },
    header: {
        marginBottom: '30px'
    },
    title: {
        fontSize: '2.5rem',
        fontWeight: 'bold',
        color: '#2d3748',
        margin: '0 0 10px 0'
    },
    subtitle: {
        fontSize: '1.2rem',
        color: '#718096',
        margin: 0
    },
    timeContainer: {
        display: 'flex',
        gap: '20px',
        marginBottom: '30px',
        flexWrap: 'wrap',
        justifyContent: 'center'
    },
    timeBox: {
        background: '#f7fafc',
        padding: '20px',
        borderRadius: '12px',
        minWidth: '200px'
    },
    timeLabel: {
        fontSize: '1rem',
        color: '#4a5568',
        margin: '0 0 10px 0',
        fontWeight: '600'
    },
    timeValue: {
        fontSize: '1.3rem',
        color: '#2d3748',
        margin: 0,
        fontWeight: 'bold'
    },
    welcomeMessage: {
        background: '#edf2f7',
        padding: '20px',
        borderRadius: '12px'
    },
    messageText: {
        fontSize: '1.1rem',
        color: '#4a5568',
        margin: 0,
        lineHeight: '1.5'
    }
};

export default Home;