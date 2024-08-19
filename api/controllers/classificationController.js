const classificationService = require('../services/classificationService');

/**
 * Starts the rules based classification process.
 * Uses keyword matching to identify hazards in the report.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} - The questions for classification.
 */
exports.startClassification = async (req, res) => {
    try {
        const report = req.body.report;
        if (!report) {
            return res.status(400).send("Report is required");
        }

        const questions = await classificationService.startClassification(report);
        return res.status(200).send(questions);
    } catch (error) {
        console.error('Error in startClassification:', error);
        return res.status(500).send("An internal error occurred");
    }
};

/**
 * Uses the confirmed and rejected hazards to refine the classification by 
 * looking for hazards with the confirmed hazards in the upstream hazards.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} - The questions for classification.
 */
exports.refineClassification = async (req, res) => {
    try {
        const { confirmed, rejected } = req.body;
        if (!confirmed || !rejected) {
            return res.status(400).send("Both confirmed and rejected hazards are required");
        }

        const questions = await classificationService.refineClassification(confirmed, rejected);
        return res.status(200).send(questions);
    } catch (error) {
        console.error('Error in refineClassification:', error);
        return res.status(500).send("An internal error occurred");
    }
};

/**
 * Uses ChatGPT to classify the report, sending the report to the ChatGPT API
 * along with th ehazard definitions to get the classification.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} - The questions for classification.
 */
exports.startGPTClassification = async (req, res) => {
    try {
        const report = req.body.report;
        if (!report) {
            return res.status(400).send("Report is required");
        }

        const questions = await classificationService.startGPTClassification(report);
        return res.status(200).send(questions);
    } catch (error) {
        console.error('Error in startGPTClassification:', error);
        return res.status(500).send("An internal error occurred");
    }
};

/**
 * Classifies the report using both the rules based and GPT classification
 * routes, returning the combined questions.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} - The questions for classification.
 */
exports.startCombinedClassification = async (req, res) => {
    try {
        const report = req.body.report;
        if (!report) {
            return res.status(400).send("Report is required");
        }

        const questions = await classificationService.startCombinedClassification(report);
        return res.status(200).send(questions);
    } catch (error) {
        console.error('Error in startCombinedClassification:', error);
        return res.status(500).send("An internal error occurred");
    }
}

/**
 * Retrieves the full hazard information for the given hazard codes
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} - The confused hazards.
 */
exports.getHazardsByCode = async (req, res) => {
    try {
        const hazardCodes = req.body.hazardCodes;
        if (!hazardCodes) {
            return res.status(400).send("Hazard codes are required");
        }

        const confusedHazards = await classificationService.getHazardsByCode(hazardCodes);
        return res.status(200).send(confusedHazards);
    } catch (error) {
        console.error('Error in getConfusedHazards:', error);
        return res.status(500).send("An internal error occurred");
    }
};
