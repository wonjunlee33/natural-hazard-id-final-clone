const express = require('express');
const classificationRoutes = require('./routes/classificationRoutes');
const app = express();

app.use(express.json());

app.use('/classify', classificationRoutes);

// const PORT = process.env.PORT || 3000;
// app.listen(PORT, () => {
//   console.log(`Server is running on port ${PORT}`);
// });

exports.classify = app;