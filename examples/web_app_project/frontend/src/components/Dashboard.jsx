import React, { useState, useEffect } from 'react';
import { fetchUserData, fetchMetrics } from '../services/api';
import MetricsCard from './MetricsCard';
import './Dashboard.css';

const Dashboard = ({ userId }) => {
  const [userData, setUserData] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        const [user, metricsData] = await Promise.all([
          fetchUserData(userId),
          fetchMetrics(userId)
        ]);
        setUserData(user);
        setMetrics(metricsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      loadDashboardData();
    }
  }, [userId]);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <p>Welcome back, {userData?.name}!</p>
      </div>
      
      <div className="metrics-grid">
        {metrics.map((metric) => (
          <MetricsCard key={metric.id} metric={metric} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
