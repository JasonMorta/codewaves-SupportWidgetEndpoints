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



/* ===========================Port Listener============================= */
app.listen(port, () => console.log(`Listening on port ${port}!`));
