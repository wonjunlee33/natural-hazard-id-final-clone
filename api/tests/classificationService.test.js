const ClassificationService = require('../services/classificationService');
const hazardDefinitionService = require('../services/hazardDefinitionService');
const axios = require('axios');

// Mock hazardDefinitionService
jest.mock('../services/hazardDefinitionService', () => ({
  getHazardDefinitions: jest.fn()
}));

describe('ClassificationService', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });
  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('startClassification', () => {
    test('should classify a report successfully', async () => {
      const report = "Sample report containing hazard";
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard", Keywords: "hazard, keywords", Questions: "Is there a hazard?"},
        { Hazard_Code: "002", Description: "Another hazard", Keywords: "", Questions: "Is there another hazard?"}
      ];
      hazardDefinitionService.getHazardDefinitions.mockResolvedValue(mockHazardDefinitions);

      const expectedResponse = [{hazardCode: "001", question: "Is there a hazard?"}];
      const questions = await ClassificationService.startClassification(report);

      expect(questions).toEqual(expectedResponse);
      expect(hazardDefinitionService.getHazardDefinitions).toHaveBeenCalled();
    });

    test('should throw an error if report is not provided', async () => {
      await expect(ClassificationService.startClassification(null))
        .rejects
        .toThrow("Report is required");
    });
  });

  describe('startGPTClassification', () => {
    test('check if the report is passed to getHazardList correctly', async () => {
      const report = "Sample report with GPT-related content";
  
      const mockHazardDefinitions = [
        { Hazard_Code: "002", Hazard_Description: "Complex GPT hazard", Keywords: "complex, gpt", Questions: "Is the complex condition present?"}
      ];
      const mockGroupedHazards = ["00 - Category 1\n001, Sample hazard\n002, Another hazard"];

      // Use jest.spyOn for mocking
      const mockHazardDefinitionService = jest.spyOn(hazardDefinitionService, 'getHazardDefinitions').mockImplementation(() => mockHazardDefinitions);
      const mockGetHazardList = jest.spyOn(ClassificationService, 'getHazardList').mockImplementation(() => [{hazard_code: '002'}]);
      const mockGroupHazardsByCategory = jest.spyOn(ClassificationService, 'groupHazardsByCategory').mockImplementation(() => mockGroupedHazards);
      const mockGetHazardQuestions = jest.spyOn(ClassificationService, 'getHazardQuestion').mockImplementation(() => "Is the complex condition present?");
  
      const expectedQuestions = [{hazardCode: "002", question: "Is the complex condition present?"}];
      const questions = await ClassificationService.startGPTClassification(report);
  
      expect(questions).toEqual(expectedQuestions);
      expect(hazardDefinitionService.getHazardDefinitions).toHaveBeenCalled();
      expect(mockGetHazardList).toHaveBeenCalledWith(mockGroupedHazards, report);
      expect(mockGetHazardQuestions).toHaveBeenCalledWith("002", mockHazardDefinitions);
    });

    test('Should return no hazards if GPT hallucinates fake hazards', async () => {
      const report = "Sample report with GPT-related content";
  
      const mockHazardDefinitions = [
        { Hazard_Code: "002", Hazard_Description: "Complex GPT hazard", Keywords: "complex, gpt", Questions: "Is the complex condition present?"}
      ];
      const mockGroupedHazards = ["00 - Category 1\n001, Sample hazard\n002, Another hazard"];

      // Use jest.spyOn for mocking
      const mockHazardDefinitionService = jest.spyOn(hazardDefinitionService, 'getHazardDefinitions').mockImplementation(() => mockHazardDefinitions);
      const mockGetHazardList = jest.spyOn(ClassificationService, 'getHazardList').mockImplementation(() => [{hazard_code: '728'}]);
      const mockGroupHazardsByCategory = jest.spyOn(ClassificationService, 'groupHazardsByCategory').mockImplementation(() => mockGroupedHazards);
      const mockGetHazardQuestions = jest.spyOn(ClassificationService, 'getHazardQuestion').mockImplementation(() => null);
  
      const expectedQuestions = [];
      const questions = await ClassificationService.startGPTClassification(report);
  
      expect(questions).toEqual(expectedQuestions);
      expect(hazardDefinitionService.getHazardDefinitions).toHaveBeenCalled();
      expect(mockGetHazardList).toHaveBeenCalledWith(mockGroupedHazards, report);
      expect(mockGetHazardQuestions).toHaveBeenCalledWith("728", mockHazardDefinitions);
    });

    test('should throw an error if report is not provided', async () => {
      await expect(ClassificationService.startGPTClassification(null))
        .rejects
        .toThrow("Report is required");
    });
  });

  describe('groupHazardsByCategory', () => {
    test('should return the hazard definitions grouped by category', () => {
      const mockHazardDefinitions = [

        { Hazard_Code: "001", Hazard_Category: "Category 1", Hazard_Description: "Sample hazard" },
        { Hazard_Code: "002", Hazard_Category: "Category 1", Hazard_Description: "Another hazard" },
        { Hazard_Code: "003", Hazard_Category: "Category 2", Hazard_Description: "Another hazard" },
        { Hazard_Code: "004", Hazard_Category: "Category 2", Hazard_Description: "Another hazard" }
      ];
      const expectedGroupedHazards = [
        "00 - Category 1\n001, Sample hazard\n002, Another hazard",
        "00 - Category 2\n003, Another hazard\n004, Another hazard"
      ];

      const groupedHazards = ClassificationService.groupHazardsByCategory(mockHazardDefinitions);

      expect(groupedHazards).toEqual(expectedGroupedHazards);
    });
  
    test('should return an empty array if no hazard definitions are provided', () => {
      const groupedHazards = ClassificationService.groupHazardsByCategory([]);
      expect(groupedHazards).toEqual([]);
    });
  });2

  describe('getHazardList', () => {
    test('should return a list of hazards based on the report', async () => {
      const mockGroupedHazards = ["00 - Category 1\n001, Sample hazard\n002, Another hazard"];
      const report = "Sample report containing hazard";
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard", Keywords: "hazard, keywords", Questions: "Is there a hazard?"},
        { Hazard_Code: "002", Description: "Another hazard", Keywords: "not, in, text", Questions: "Is there another hazard?"}
      ];
      const mockGPTResponse = {
        choices: [
        {
          message: {
            function_call: {
              arguments:
                '{"possible_hazards": [{"hazard_code": "001"}]}'
            }
          }
        }
      ]};
      const mockHazardDefinitionService = jest.spyOn(hazardDefinitionService, 'getHazardDefinitions').mockImplementation(() => mockHazardDefinitions);
      const mockAxios = jest.spyOn(axios, 'post').mockResolvedValue({data: mockGPTResponse});

      const hazardList = await ClassificationService.getHazardList(mockGroupedHazards, report);

      expect(hazardList).toEqual([{"hazard_code": "001"}]);
      expect(axios.post).toHaveBeenCalled();
    });

    test('Should throw an error if the api call fails', async () => {
      const mockGroupedHazards = ["00 - Category 1\n001, Sample hazard\n002, Another hazard"];
      const report = "Sample report containing hazard";
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard", Keywords: "hazard, keywords", Questions: "Is there a hazard?"},
        { Hazard_Code: "002", Description: "Another hazard", Keywords: "not, in, text", Questions: "Is there another hazard?"}
      ];
      const mockHazardDefinitionService = jest.spyOn(hazardDefinitionService, 'getHazardDefinitions').mockImplementation(() => mockHazardDefinitions);
      const mockAxios = jest.spyOn(axios, 'post').mockRejectedValue(new Error("API call failed"));

      await expect(ClassificationService.getHazardList(mockGroupedHazards, report))
        .rejects
        .toThrow("Error fetching hazard list from GPT API.");
    });
  });

  describe('refineClassification', () => {
    test('should refine classification based on confirmed and rejected hazards', async () => {
      const confirmed = ["001"];
      const rejected = ["002"];
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Hazard_Description: "Sample hazard", Keywords: "hazard", Questions: "Is there a hazard?", Upstream_Hazards: "" },
        { Hazard_Code: "002", Hazard_Description: "Another hazard", Keywords: "another", Questions: "Is there another hazard?", Upstream_Hazards: "001" },
        { Hazard_Code: "003", Hazard_Description: "Third hazard", Keywords: "third", Questions: "Is there a third hazard?", Upstream_Hazards: "001" },
        { Hazard_Code: "004", Hazard_Description: "Fourth hazard", Keywords: "fourth", Questions: "Is there a fourth hazard?", Upstream_Hazards: ""}
      ];
      hazardDefinitionService.getHazardDefinitions.mockResolvedValue(mockHazardDefinitions);

      const expectedQuestions = [{hazardCode: "003", question: "Is there a third hazard?"}];
      const questions = await ClassificationService.refineClassification(confirmed, rejected);

      expect(questions).toEqual(expectedQuestions);
      expect(hazardDefinitionService.getHazardDefinitions).toHaveBeenCalled();
    });

    test('should throw an error if confirmed or rejected hazards are not provided', async () => {
      await expect(ClassificationService.refineClassification(null, null))
        .rejects
        .toThrow("Confirmed and Rejected hazards are required");
    });
  });

  describe('getHazardsByCode', () => {
    test('should retrieve hazards by code successfully', async () => {
      const hazardCodes = ["001"];
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard" }
      ];
      hazardDefinitionService.getHazardDefinitions.mockResolvedValue(mockHazardDefinitions);

      const hazards = await ClassificationService.getHazardsByCode(hazardCodes);

      expect(hazards).toEqual(mockHazardDefinitions);
      expect(hazardDefinitionService.getHazardDefinitions).toHaveBeenCalled();
    });

    test('should throw an error if hazard codes are not provided', async () => {
      await expect(ClassificationService.getHazardsByCode(null))
        .rejects
        .toThrow("Hazard codes are required");
    });
  });

  describe('getHazardQuestion', () => {
    test('should retrieve the question for a hazard code', () => {
      const hazardCode = "001";
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard", Keywords: "hazard, keywords", Questions: "Is there a hazard?"}
      ];

      const question = ClassificationService.getHazardQuestion(hazardCode, mockHazardDefinitions);

      expect(question).toEqual("Is there a hazard?");
    });

    test('should return null if the hazard code is not found', () => {
      const hazardCode = "002";
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard", Keywords: "hazard, keywords", Questions: "Is there a hazard?"}
      ];

      const question = ClassificationService.getHazardQuestion(hazardCode, mockHazardDefinitions);

      expect(question).toBeNull();
    });
  });

  describe('combinedClassification', () => {
    test('should combine GPT and report classification successfully', async () => {
      const report = "Sample report containing hazard";
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard", Keywords: "hazard, keywords", Questions: "Is there a hazard?"},
        { Hazard_Code: "002", Description: "Another hazard", Keywords: "not, in, text", Questions: "Is there another hazard?"}
      ];

      const mockHazardDefinitionService = jest.spyOn(hazardDefinitionService, 'getHazardDefinitions').mockImplementation(() => mockHazardDefinitions);
      const mockGPTQuestions = jest.spyOn(ClassificationService, 'getGPTQuestions').mockImplementation(() => [{hazardCode: "001", question: "Is there a hazard?"}]);
      const mockReportQuestions = jest.spyOn(ClassificationService, 'getReportQuestions').mockImplementation(() => [{hazardCode: "002", question: "Is there another hazard?"}]);

      const expectedResponse = [
        {hazardCode: "001", question: "Is there a hazard?"},
        {hazardCode: "002", question: "Is there another hazard?"}
      ];
      const questions = await ClassificationService.startCombinedClassification(report);

      expect(questions).toEqual(expectedResponse);
      expect(hazardDefinitionService.getHazardDefinitions).toHaveBeenCalled();
    });

    test('should remove duplicate classification questions', async () => {
      const report = "Sample report containing hazard";
      const mockHazardDefinitions = [
        { Hazard_Code: "001", Description: "Sample hazard", Keywords: "hazard, keywords", Questions: "Is there a hazard?"},
        { Hazard_Code: "002", Description: "Another hazard", Keywords: "not, in, text", Questions: "Is there another hazard?"}
      ];

      const mockHazardDefinitionService = jest.spyOn(hazardDefinitionService, 'getHazardDefinitions').mockImplementation(() => mockHazardDefinitions);
      const mockGPTQuestions = jest.spyOn(ClassificationService, 'getGPTQuestions').mockImplementation(() => [{hazardCode: "001", question: "Is there a hazard?"}, {hazardCode: "002", question: "Is there another hazard?"}]);
      const mockReportQuestions = jest.spyOn(ClassificationService, 'getReportQuestions').mockImplementation(() => [{hazardCode: "001", question: "Is there a hazard?"}, {hazardCode: "002", question: "Is there another hazard?"}]);

      const expectedResponse = [
        {hazardCode: "001", question: "Is there a hazard?"},
        {hazardCode: "002", question: "Is there another hazard?"}
      ];
      const questions = await ClassificationService.startCombinedClassification(report);

      expect(questions).toEqual(expectedResponse);
      expect(hazardDefinitionService.getHazardDefinitions).toHaveBeenCalled();
    });

    test('should throw an error if report is not provided', async () => {
      await expect(ClassificationService.startCombinedClassification(null))
        .rejects
        .toThrow("Report is required");
    });
  }
)});
