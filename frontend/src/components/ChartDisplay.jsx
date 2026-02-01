import React from 'react';
import { Bar, Line, Pie, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Paper, Typography } from '@mui/material';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const ChartDisplay = ({ chartData }) => {
  if (!chartData || !chartData.chartType) {
    return null;
  }

  const { chartType, data, options } = chartData;

  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      title: {
        display: true,
        text: options?.plugins?.title?.text || 'Chart',
      },
    },
    ...options,
  };

  const renderChart = () => {
    switch (chartType.toLowerCase()) {
      case 'bar':
        return <Bar data={data} options={defaultOptions} />;
      case 'line':
        return <Line data={data} options={defaultOptions} />;
      case 'pie':
        return <Pie data={data} options={defaultOptions} />;
      case 'doughnut':
        return <Doughnut data={data} options={defaultOptions} />;
      default:
        return <Typography color="error">Unsupported chart type: {chartType}</Typography>;
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 2, my: 2, maxWidth: '600px' }}>
      {renderChart()}
    </Paper>
  );
};

export default ChartDisplay;

