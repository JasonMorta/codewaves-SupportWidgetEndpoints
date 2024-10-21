import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import bodyParser from 'body-parser';
import { fetchAgentConversationData } from './conversations.js';

// Configure environment variables
dotenv.config();

// Initialize express
const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: false })); // parse application/x-www-form-urlencoded
app.use(bodyParser.json()); // parse application/json

const corsOptions = { origin: "*" };
app.use(cors(corsOptions));

const port = process.env.PORT || 3001;

/* ===========================API Routes=============================== */
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// get conversation data
app.get('/conversations', async (req, res) => {

  //req.query.endDate__2024-10-14T23:59 format
  //req.query.startDate__2024-10-14T23:59 format
  //req.query.agentId__842946f3-06fa-4edd-ab0d-7f88d554efd6

  try {
   // const data = await fetchAgentConversationData(req.query.agentId, req.query.startDate, req.query.endDate);
   const data = await fetchAgentConversationData("842946f3-06fa-4edd-ab0d-7f88d554efd6", "2024-10-01T01:00", "2024-10-21T23:59");

    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});


/* ===========================Port Listener============================= */
app.listen(port, () => console.log(`Listening on port ${port}!`));
