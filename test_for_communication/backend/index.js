const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

let port_number = 3000;
let count = 1;

// const oauth_id = `u-s4t2ud-7faf9f8d954018302333d61413e324fbc7c6574ea67f01f26a01f0fd43c62f8f`;
// const oauth_pw = `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`;
// const url = `https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-7faf9f8d954018302333d61413e324fbc7c6574ea67f01f26a01f0fd43c62f8f&redirect_uri=http%3A%2F%2FSPP%2Foauth&response_type=code`;
// const url2 = `http://SPP/oauth`;

app.get('/api', (req, res) => {res.json({message: count++});});
app.get('/reset', (req, res) => 
{
	count = 0;
	res.json({message: 'done'});
});

app.post('/data', (req, res) => 
{
	const data = req.body;
	if (data.no1 === undefined || data.no2 === undefined || data.no3 === undefined) {return res.status(400).json({ message: 'Missing data fields' });}
	res.json({message: `First input is ${data.no1} and it's result is ${data.no1 ** 2}
	Second input is ${data.no2} and it's result is ${data.no2 * 2}
	Third input is ${data.no3} and it's result is ${data.no3 + 2}
	I hope you well done it!!`});
});


app.listen(port_number, () => {console.log(`backend is running on port ${port_number}`);});