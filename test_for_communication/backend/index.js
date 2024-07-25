const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());

let port_number = 3000;
let count = 1;

app.get('/api', (req, res) => {res.json({message: `you clicked ${count++} times`});});

app.get('/', (req, res) => {res.json({message: `you requested basic url`});});

app.listen(port_number, () => {console.log(`backend is running on port ${port_number}`);});