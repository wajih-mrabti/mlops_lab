export type SummaryCard = {
  label: string;
  value: string;
  delta: string;
  tone: 'positive' | 'neutral' | 'warning';
};

export type ActivityItem = {
  id: string;
  title: string;
  detail: string;
  time: string;
};

export type ModelRow = {
  name: string;
  version: string;
  stage: 'production' | 'staging' | 'candidate';
  owner: string;
  updated: string;
};

export const summaryCards: SummaryCard[] = [
  { label: 'Registered Models', value: '24', delta: '+3 this month', tone: 'positive' },
  { label: 'Experiments', value: '148', delta: '+18 active', tone: 'neutral' },
  { label: 'Active Deployments', value: '12', delta: '2 pending review', tone: 'positive' },
  { label: 'Alerts', value: '4', delta: '1 critical', tone: 'warning' },
];

export const recentActivity: ActivityItem[] = [
  { id: 'a1', title: 'Model promotion review', detail: 'Revenue Forecasting v2.7 was approved for production.', time: '14 min ago' },
  { id: 'a2', title: 'Experiment checkpoint', detail: 'Run #2048 completed with a 1.4% improvement in recall.', time: '42 min ago' },
  { id: 'a3', title: 'Deployment rollback', detail: 'Synthetic Risk Classifier was rolled back after a policy alert.', time: '2 hours ago' },
  { id: 'a4', title: 'Team review requested', detail: 'A new model card draft is awaiting stakeholder sign-off.', time: 'Yesterday' },
];

export const recentModels: ModelRow[] = [
  { name: 'Customer Churn Predictor', version: 'v3.1.8', stage: 'production', owner: 'ML Platform', updated: '2 hours ago' },
  { name: 'Demand Forecasting', version: 'v2.7.0', stage: 'production', owner: 'Operations', updated: '5 hours ago' },
  { name: 'Fraud Signal Model', version: 'v5.4.1', stage: 'staging', owner: 'Risk', updated: '1 day ago' },
  { name: 'Document Classifier', version: 'v1.9.2', stage: 'candidate', owner: 'AI Services', updated: '2 days ago' },
];
