const { startClassification, startGPTClassification, refineClassification, getHazardsByCode, startCombinedClassification } = require('../controllers/classificationController');
const classificationService = require('../services/classificationService');

// Mock the classificationService
jest.mock('../services/classificationService');

describe('classificationController', () => {
  let mockRequest;
  let mockResponse;
  beforeEach(() => {
    mockRequest = {
      body: {}
    };
    mockResponse = {
      send: jest.fn(),
      status: jest.fn().mockReturnThis()
    };
  });

  describe('startClassification', () => {
    test('should respond with questions on valid report', async () => {
      mockRequest.body.report = 'Example report content';
      classificationService.startClassification.mockResolvedValue(['Question 1?', 'Question 2?']);

      await startClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(200);
      expect(mockResponse.send).toHaveBeenCalledWith(['Question 1?', 'Question 2?']);
    });

    test('should respond with 400 if report is missing', async () => {
      await startClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.send).toHaveBeenCalledWith("Report is required");
    });

    test('should respond with 500 if an error occurs', async () => {
      mockRequest.body.report = 'Example report content';
      classificationService.startClassification.mockRejectedValue('Error message');

      await startClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.send).toHaveBeenCalledWith("An internal error occurred");
    });
  });

  describe('startGPTClassification', () => {
    test('should respond with questions on valid report', async () => {
      mockRequest.body.report = 'Example report content';
      classificationService.startGPTClassification.mockResolvedValue(['Question 1?', 'Question 2?']);

      await startGPTClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(200);
      expect(mockResponse.send).toHaveBeenCalledWith(['Question 1?', 'Question 2?']);
    });

    test('should respond with 400 if report is missing', async () => {
      await startGPTClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.send).toHaveBeenCalledWith("Report is required");
    });

    test('should respond with 500 if an error occurs', async () => {
      mockRequest.body.report = 'Example report content';
      classificationService.startGPTClassification.mockRejectedValue('Error message');

      await startGPTClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.send).toHaveBeenCalledWith("An internal error occurred");
    });
  });

  describe('refineClassification', () => {
    test('should refine classification successfully', async () => {
      mockRequest.body = {
        confirmed: ['Hazard1'],
        rejected: ['Hazard2']
      };
      classificationService.refineClassification.mockResolvedValue(['Refined question?']);

      await refineClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(200);
      expect(mockResponse.send).toHaveBeenCalledWith(['Refined question?']);
    });

    test('should respond with 400 if confirmed or rejected lists are missing', async () => {
      await refineClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.send).toHaveBeenCalledWith("Both confirmed and rejected hazards are required");
    });

    test('should respond with 500 if an error occurs', async () => {
      mockRequest.body = {
        confirmed: ['Hazard1'],
        rejected: ['Hazard2']
      };
      classificationService.refineClassification.mockRejectedValue('Error message');

      await refineClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.send).toHaveBeenCalledWith("An internal error occurred");
    });
  });

  describe('getHazardsByCode', () => {
    test('should retrieve hazards successfully', async () => {
      mockRequest.body.hazardCodes = ['001', '002'];
      classificationService.getHazardsByCode.mockResolvedValue(['Hazard details']);

      await getHazardsByCode(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(200);
      expect(mockResponse.send).toHaveBeenCalledWith(['Hazard details']);
    });

    test('should respond with 400 if hazard codes are missing', async () => {
      await getHazardsByCode(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.send).toHaveBeenCalledWith("Hazard codes are required");
    });

    test('should respond with 500 if an error occurs', async () => {
      mockRequest.body.hazardCodes = ['001', '002'];
      classificationService.getHazardsByCode.mockRejectedValue('Error message');

      await getHazardsByCode(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.send).toHaveBeenCalledWith("An internal error occurred");
    });
  });

  describe('startCombinedClassification', () => {
    test('should respond with questions on valid report', async () => {
      mockRequest.body.report = 'Example report content';
      classificationService.startCombinedClassification.mockResolvedValue(['Question 1?', 'Question 2?']);

      await startCombinedClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(200);
      expect(mockResponse.send).toHaveBeenCalledWith(['Question 1?', 'Question 2?']);
    });

    test('should respond with 400 if report is missing', async () => {
      await startCombinedClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.send).toHaveBeenCalledWith("Report is required");
    });

    test('should respond with 500 if an error occurs', async () => {
      mockRequest.body.report = 'Example report content';
      classificationService.startCombinedClassification.mockRejectedValue('Error message');

      await startCombinedClassification(mockRequest, mockResponse);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.send).toHaveBeenCalledWith("An internal error occurred");
    });
  });
});
