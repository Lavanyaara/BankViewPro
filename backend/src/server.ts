import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { generateSampleData, getMetricInfo } from './utils/data-generator';
import { calculateOverallScore, getRatingLabel } from './utils/scoring-engine';
import { generateCommentary } from './utils/commentary-generator';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const bankData = generateSampleData();
const metricInfo = getMetricInfo();

app.get('/api/institutions', (req: Request, res: Response) => {
  const institutions = Object.keys(bankData).map(name => ({
    name,
    type: bankData[name].institution_type,
    assets: bankData[name].assets,
    employees: bankData[name].employees,
    branches: bankData[name].branches
  }));
  
  res.json(institutions);
});

app.get('/api/institutions/:name', (req: Request, res: Response) => {
  const name = decodeURIComponent(req.params.name);
  const institution = bankData[name];
  
  if (!institution) {
    return res.status(404).json({ error: 'Institution not found' });
  }
  
  res.json(institution);
});

app.get('/api/institutions/:name/scores', (req: Request, res: Response) => {
  const name = decodeURIComponent(req.params.name);
  const institution = bankData[name];
  
  if (!institution) {
    return res.status(404).json({ error: 'Institution not found' });
  }
  
  const scores = calculateOverallScore(institution);
  const rating = getRatingLabel(scores.overall);
  
  res.json({ ...scores, rating });
});

app.post('/api/commentary', async (req: Request, res: Response) => {
  const { institutionName, category } = req.body;
  
  if (!institutionName || !category) {
    return res.status(400).json({ error: 'institutionName and category are required' });
  }
  
  const institution = bankData[institutionName];
  
  if (!institution) {
    return res.status(404).json({ error: 'Institution not found' });
  }
  
  const scores = calculateOverallScore(institution);
  const commentary = await generateCommentary(institution, scores, category);
  
  res.json({ commentary });
});

app.get('/api/metrics', (req: Request, res: Response) => {
  res.json(metricInfo);
});

app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Credit Dashboard API server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
