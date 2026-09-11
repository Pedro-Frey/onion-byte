import React from 'react';
import { Badge } from './ui/Badge';
import { ScoreData } from '@/types';

export function ScoreDisplay({ data }: { data: ScoreData }) {
  if (!data) return <Badge variant="default">N/A</Badge>;

  return (
    <div className="flex items-center gap-2">
      <Badge variant={data.grade}>{data.grade}</Badge>
      <span className="text-sm font-medium">{data.score}/100</span>
    </div>
  );
}

export function ScoreDetailedDisplay({ data }: { data: ScoreData }) {
  if (!data) return <div>Sem dados de score</div>;

  const getBarColor = (val: number) => {
    if (val >= 80) return 'bg-green-500';
    if (val >= 60) return 'bg-blue-500';
    if (val >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const breakdowns = [
    { label: 'Fit da Empresa', value: data.breakdown.company_fit },
    { label: 'Saúde Financeira', value: data.breakdown.financial_health },
    { label: 'Presença Online', value: data.breakdown.online_presence },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between border-b pb-4">
        <div>
          <h4 className="text-sm font-medium text-gray-500">Score Geral</h4>
          <div className="flex items-center mt-1">
            <span className="text-3xl font-bold mr-2">{data.score}</span>
            <Badge variant={data.grade} className="text-sm px-3">{data.grade}</Badge>
          </div>
        </div>
      </div>
      
      <div className="space-y-3">
        {breakdowns.map((item, idx) => (
          <div key={idx}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-700">{item.label}</span>
              <span className="font-medium">{item.value}/100</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getBarColor(item.value)}`} 
                style={{ width: `${item.value}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-100">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Recomendação IA</h4>
        <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded">{data.recommendation}</p>
      </div>
    </div>
  );
}
