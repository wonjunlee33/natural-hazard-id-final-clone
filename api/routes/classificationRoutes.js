const express = require('express');
const classificationController = require('../controllers/classificationController');
const router = express.Router();

router.post('/startClassification', classificationController.startClassification);
router.post('/refineClassification', classificationController.refineClassification);
router.post('/startGPTClassification', classificationController.startGPTClassification);
router.post('/startCombinedClassification', classificationController.startCombinedClassification);
router.post('/getHazardsByCode', classificationController.getHazardsByCode);

module.exports = router;