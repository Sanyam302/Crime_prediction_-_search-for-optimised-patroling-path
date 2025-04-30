const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

// Enable CORS
app.use(cors({
    origin: 'http://127.0.0.1:5500'  // Adjust this to match your frontend's URL if different
}));

// Parse JSON bodies
app.use(bodyParser.json());

// POST route for prediction
app.post('/predict', (req, res) => {
    const { latitude, longitude, hour, dayOfWeek, month, blockCode, locationCode } = req.body;

    // Ensure you provide the correct path to Python executable if necessary
    const python = spawn('C:/Users/Admin/Crime prediction/ml model/venv/Scripts/python.exe', ['ml model/predict.py', latitude, longitude, hour, dayOfWeek, month, blockCode, locationCode]);

    python.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        const prediction = data.toString().trim();
        res.json({ prediction });
    });

    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        if (!res.headersSent) {   // 🛡️ Check if response is already sent
            res.status(500).send('Internal server error: ' + data.toString());
        }
    });
    

    python.on('error', (err) => {
        console.error('Failed to start Python process:', err);
        res.status(500).json({ error: 'Failed to start Python process' });
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
