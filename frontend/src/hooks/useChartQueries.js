import { useMutation } from '@tanstack/react-query';
import chartService from '../services/chartService';

// Hook to generate chart data
export const useGenerateChart = () => {
  return useMutation({
    mutationFn: chartService.generateChart,
  });
};

