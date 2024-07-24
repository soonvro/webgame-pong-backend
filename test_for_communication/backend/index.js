const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());

let port_number = 3000;
let cout = 0;

app.get('/api', (req, res) => 
{
	res.json({message: `you clicked ${cout++}`});
	console.log(`req's message is ${req.message}`);
});

app.listen(port_number, () =>
{
	console.log(`backend is running on port ${port_number}`);
});