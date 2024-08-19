/**
 * @fileoverview This file contains the implementation of the ClassificationService class,
 * which provides methods for hazard classification and question generation based on a given report.
 * It depends on the natural, axios, and hazardDefinitionService modules.
 * @module classificationService
 */

const natural = require('natural');
const axios = require("axios");
const hazardDefinitionService = require('./hazardDefinitionService');

/**
 * Represents the ClassificationService class.
 * @class
 */
class ClassificationService {
  /**
   * Constructs an instance of the ClassificationService class.
   * Initializes the tokenizer.
   * @constructor
   */
  constructor() {
    this.tokenizer = new natural.WordTokenizer();
  }

  /**
   * Starts the hazard classification process based on a given report.
   * Retrieves hazard definitions and generates report-specific questions.
   * @async
   * @param {string} report - The report to be classified.
   * @returns {Array} An array of questions to ask for hazard identification.
   * @throws {Error} If the report is not provided.
   */
  async startClassification(report) {
    if (!report) {
      throw new Error('Report is required');
    }

    const hazardDefinitions = await hazardDefinitionService.getHazardDefinitions();

    return this.getReportQuestions(report, hazardDefinitions);
  }

  /**
   * Starts the GPT-based hazard classification process based on a given report.
   * Retrieves hazard definitions and generates GPT-specific questions.
   * @async
   * @param {string} report - The report to be classified.
   * @returns {Array} An array of questions to ask for hazard identification.
   * @throws {Error} If the report is not provided.
   */
  async startGPTClassification(report) {
    if (!report) {
      throw new Error('Report is required');
    }

    const hazardDefinitions = await hazardDefinitionService.getHazardDefinitions();

    return this.getGPTQuestions(report, hazardDefinitions);
  }

  /**
   * Refines the hazard classification process based on confirmed and rejected hazards.
   * Retrieves hazard definitions and generates upstream questions.
   * @async
   * @param {Array} confirmed - An array of confirmed hazard codes.
   * @param {Array} rejected - An array of rejected hazard codes.
   * @returns {Array} An array of questions to ask for further hazard identification.
   * @throws {Error} If confirmed or rejected hazards are not provided.
   */
  async refineClassification(confirmed, rejected) {
    if (!confirmed || !rejected) {
      throw new Error('Confirmed and Rejected hazards are required');
    }

    const hazardDefinitions = await hazardDefinitionService.getHazardDefinitions();

    return this.getUpstreamQuestions(confirmed, rejected, hazardDefinitions);
  }

  /**
   * Retrieves hazard information based on hazard codes.
   * @async
   * @param {Array} hazardCodes - An array of hazard codes.
   * @returns {Array} An array of hazard definitions.
   * @throws {Error} If hazard codes are not provided.
   */  
  async getHazardsByCode(hazardCodes) {
    if (!hazardCodes) {
      throw new Error('Hazard codes are required');
    }

    const hazardDefinitions = await hazardDefinitionService.getHazardDefinitions();

    return hazardDefinitions.filter(hazard => hazardCodes.map(code => code.toLowerCase()).includes(hazard.Hazard_Code.toLowerCase()));
  }

  /**
   * Starts the combined hazard classification process based on a given report.
   * Retrieves hazard definitions and generates both GPT and report-specific questions.
   * @async
   * @param {string} report - The report to be classified.
   * @returns {Array} An array of unique questions to ask for hazard identification.
   * @throws {Error} If the report is not provided.
   */
  async startCombinedClassification(report) {
    if (!report) {
      throw new Error('Report is required');
    }

    const hazardDefinitions = await hazardDefinitionService.getHazardDefinitions();

    const gptQuestions = await this.getGPTQuestions(report, hazardDefinitions);
    const reportQuestions = this.getReportQuestions(report, hazardDefinitions);

    const both = gptQuestions.concat(reportQuestions);
    
    // Remove duplicates
    const uniqueQuestions = [];
    const seenQuestions = new Set();
    both.forEach((question) => {
      if (!seenQuestions.has(question.question)) {
        uniqueQuestions.push(question);
        seenQuestions.add(question.question);
      }
    });

    return uniqueQuestions;
  }

  /**
   * Generates report-specific questions based on a given report and hazard definitions.
   * @param {string} reportText - The report text.
   * @param {Array} hazardDefinitions - An array of hazard definitions.
   * @returns {Array} An array of questions to ask for hazard identification.
   */
  getReportQuestions(reportText, hazardDefinitions) {
    let tokenizedReport = this.tokenizer.tokenize(reportText.toLowerCase());
    let questionsToAsk = [];

    hazardDefinitions.forEach((hazard) => {
      let keywords = hazard.Keywords ? hazard.Keywords.split(", ") : [];
      keywords = keywords.map(keyword => keyword.toLowerCase());
      let keywordFound = keywords.some(keyword => tokenizedReport.includes(keyword));

      if (keywordFound) {
        questionsToAsk.push({
          question: hazard.Questions,
          hazardCode: hazard.Hazard_Code,
        });
      }
    });

    return questionsToAsk;
  }

  /**
   * Retrieves a comprehensive hazard list using GPT API based on a given report and hazard definitions.
   * @async
   * @param {Array} hazardDefinitions - An array of hazard definitions.
   * @param {string} report - The report to be classified.
   * @returns {Array} An array of possible hazards.
   * @throws {Error} If there is an error fetching the hazard list from GPT API.
   */
  async getHazardList(hazardDefinitions, report) {
    try {
      const hazardDefinitionsConcatenated = hazardDefinitions.join("\n");
      // Create the completion request
      const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
          model: "gpt-4-turbo-preview",
          messages: [
            {
              role: "system",
              content: `Here is a comprehensive list of hazard classifications, and their definitions:
              Hazard_Code, Hazard_Name Hazard_Description,
              ${hazardDefinitionsConcatenated}
              You are HazardID, an AI assistant that helps people identify hazards in a given report. It very important that you identify every hazard in the report. You should attempt to infer other hazards that may be present, even if not directly mentioned.
You MUST include all hazards that are directly mentioned in the report.`,
            },
            {
              role: "user",
              content: report,
            },
          ],
          temperature: 0,
          max_tokens: 1300,
          functions: [
            {
              name: "createHazardList",
              parameters: {
                type: "object",
                properties: {
                  possible_hazards: {
                    type: "array",
                    items: {
                      type: "object",
                      properties: {
                        hazard_code: {
                          type: "string",
                        }
                      },
                    },
                  },
                },
                required: ["hazard_code"],
              },
            },
          ],
          function_call: { name: "createHazardList" },
        },
        {
          headers: {
            Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
            "Content-Type": "application/json",
          },
        }
      );
      
      // Extracting function call information from the response
      const functionCall = response.data.choices[0].message.function_call;
      const jsonArguments = JSON.parse(functionCall.arguments);
      return jsonArguments["possible_hazards"];
    } catch (error) {
      throw new Error("Error fetching hazard list from GPT API.");
    }
  }

  /**
   * Retrieves the question for a specific hazard code from hazard definitions.
   * @param {string} hazardCode - The hazard code.
   * @param {Array} hazardDefinitions - An array of hazard definitions.
   * @returns {string|null} The question for the hazard code, or null if not found.
   */
  getHazardQuestion(hazardCode, hazardDefinitions) {
    let hazard = hazardDefinitions.find((hazard) => hazard.Hazard_Code === hazardCode);
    if (!hazard) {
      return null;
    }
    return hazard.Questions;
  }

  /**
   * Generates GPT-specific questions based on a given report and hazard definitions.
   * @async
   * @param {string} report - The report to be classified.
   * @param {Array} hazardDefinitions - An array of hazard definitions.
   * @returns {Array} An array of questions to ask for hazard identification.
   */
  async getGPTQuestions(report, hazardDefinitions) {
    let questionsToAsk = [];
  
    // Group hazard definitions by category
    let hazardDefinitionsByCategory = this.groupHazardsByCategory(hazardDefinitions);

    // Get the hazard list for the current category
    let hazardList = await this.getHazardList(hazardDefinitionsByCategory, report);
    
    // Remove duplicates
    const seenQuestions = new Set();

    // Iterate through each hazard in the hazard list
    hazardList.forEach((hazard) => {
      const hazardCode = hazard.hazard_code;
      // Get the corresponding question for the hazard code
      let question = this.getHazardQuestion(hazardCode, hazardDefinitions);

      if (!seenQuestions.has(question) && question != null) {
        seenQuestions.add(question.question);
        questionsToAsk.push({
          hazardCode: hazardCode,
          question: question,
        });
      }
    });
    return questionsToAsk;
  }

  /**
   * Groups hazards by category.
   * @param {Array} hazards - An array of hazard definitions.
   * @returns {Array} An array of grouped hazard definitions.
   */
  groupHazardsByCategory(hazards) {
    const grouped = hazards.reduce((acc, hazard) => {
      const category = hazard.Hazard_Category;
      if (!acc[category]) {
        acc[category] = [];
      }
      acc[category].push(hazard);
      return acc;
    }, {});
  
    const result = Object.keys(grouped).map((category) => {
      const hazardsInCategory = grouped[category];
      const codePrefix = grouped[category][0].Hazard_Code.slice(0, 2);
      const converted = hazardsInCategory
        .map((hazard) => {
          // const codeSuffix = hazard.Hazard_Code.slice(-2);
          const description = hazard.Hazard_Description.trim();
          return `${hazard.Hazard_Code}, ${description}`;
        })
        .join("\n");
      return `${codePrefix} - ${category}\n${converted}`;
    });
  
    return result;
  }

  /**
   * Generates upstream questions based on confirmed and rejected hazards.
   * @param {Array} confirmed - An array of confirmed hazard codes.
   * @param {Array} rejected - An array of rejected hazard codes.
   * @param {Array} hazardDefinitions - An array of hazard definitions.
   * @returns {Array} An array of questions to ask for further hazard identification.
   */
  getUpstreamQuestions(confirmed, rejected, hazardDefinitions) {
    let questionsToAsk = [];

    hazardDefinitions.forEach(hazard => {
      if (confirmed.includes(hazard.Hazard_Code.toLowerCase()) || rejected.includes(hazard.Hazard_Code.toLowerCase())) {
        return;
      }

      let upstreamHazards = hazard.Upstream_Hazards ? hazard.Upstream_Hazards.split(", ") : [];
      let upstreamHazardFound = upstreamHazards.some(upstreamHazard => confirmed.includes(upstreamHazard));
      
      if (upstreamHazardFound) {
        questionsToAsk.push({
          question: hazard.Questions,
          hazardCode: hazard.Hazard_Code,
        });
      }
    });

    return questionsToAsk;
  }
}

module.exports = new ClassificationService();
