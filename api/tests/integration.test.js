const request = require('supertest');
const hazardDefinitionService = require('../services/hazardDefinitionService');
const axios = require('axios');
const app = require('../app');

// Mock hazardDefinitionService
jest.mock('../services/hazardDefinitionService', () => ({
    getHazardDefinitions: jest.fn()
}));

describe('Integration Tests', () => {
    beforeEach(() => {
        jest.resetAllMocks();
        const mockHazardDefinitions = [
            { Hazard_Code: "001", Hazard_Description: "Sample hazard", Keywords: "hazard", Questions: "Is there a hazard?", Upstream_Hazards: "" },
            { Hazard_Code: "002", Hazard_Description: "Another hazard", Keywords: "another", Questions: "Is there another hazard?", Upstream_Hazards: "001" },
            { Hazard_Code: "003", Hazard_Description: "Third hazard", Keywords: "third", Questions: "Is there a third hazard?", Upstream_Hazards: "001" },
            { Hazard_Code: "004", Hazard_Description: "Fourth hazard", Keywords: "fourth", Questions: "Is there a fourth hazard?", Upstream_Hazards: ""}
        ];
        hazardDefinitionService.getHazardDefinitions.mockResolvedValue(mockHazardDefinitions);
    });
    afterEach(() => {
        jest.restoreAllMocks();
    });

    describe('startClassification', () => {
        test('should return a 200 and classify the report', async () => {
            const response = await request(app.classify).post('/classify/startClassification').send({report: 'Example report content containing a hazard'}) // Use the server instance to make the request
            
            expect(response.statusCode).toBe(200);
            expect(response.body).toStrictEqual([{hazardCode: "001", question: "Is there a hazard?"}])
        });

        test('should return a 500 if an error occurs', async () => {
            hazardDefinitionService.getHazardDefinitions.mockRejectedValue(new Error('Test error'));

            const response = await request(app.classify).post('/classify/startClassification').send({report: 'Example report content containing a hazard'}) // Use the server instance to make the request

            expect(response.statusCode).toBe(500);
        });

        test('should return a 400 if no report is supplied', async () => {
            const response = await request(app.classify).post('/classify/startClassification').send({})

            expect(response.statusCode).toBe(400)
        });
    });

    describe('startGPTClassification', () => {
        test('should return a 200 and classify the report', async () => {
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
            const mockAxios = jest.spyOn(axios, 'post').mockResolvedValue({data: mockGPTResponse});

            const response = await request(app.classify).post('/classify/startGPTClassification').send({report: 'Example report content containing a hazard'}) // Use the server instance to make the request
            
            expect(response.statusCode).toBe(200);
            expect(response.body).toStrictEqual([{hazardCode: "001", question: "Is there a hazard?"}])
        });

        test('should return a 500 if GPT API returns an error', async () => {
            const mockAxios = jest.spyOn(axios, 'post').mockResolvedValue({data: "Error"});

            const response = await request(app.classify).post('/classify/startGPTClassification').send({report: 'Example report content containing a hazard'}) // Use the server instance to make the request
            
            expect(response.statusCode).toBe(500);
        });

        test('should return a 400 if no report is supplied', async () => {
            const response = await request(app.classify).post('/classify/startGPTClassification').send({})

            expect(response.statusCode).toBe(400)
        })
    });

    describe('refineClassification', () => {
        test('should return a 200 and classify the report', async () => {
            const confirmed = ["001"];
            const rejected = ["002"];

            const response = await request(app.classify).post('/classify/refineClassification').send({confirmed: confirmed, rejected: rejected})

            expect(response.statusCode).toBe(200)
            expect(response.body).toStrictEqual([{hazardCode: "003", question: "Is there a third hazard?"}])
        })

        test('should return a 500 if an error occurs', async () => {
            hazardDefinitionService.getHazardDefinitions.mockRejectedValue(new Error('Test error'));

            const response = await request(app.classify).post('/classify/refineClassification').send({confirmed: ["001"], rejected: ["002"]})

            expect(response.statusCode).toBe(500)
        })

        test('Integration test refineClassification', async () => {
            const response = await request(app.classify).post('/classify/refineClassification').send({})

            expect(response.statusCode).toBe(400)
        })
    })

    describe('startCombinedClassification', () => {
        test('should return a 200 and classify the report', async () => {
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
            const mockAxios = jest.spyOn(axios, 'post').mockResolvedValue({data: mockGPTResponse});

            const response = await request(app.classify).post('/classify/startCombinedClassification').send({report: 'Example report content containing a hazard'}) // Use the server instance to make the request
            
            expect(response.statusCode).toBe(200);
            expect(response.body).toStrictEqual([{hazardCode: "001", question: "Is there a hazard?"}]) 
        })

        test('should return a 500 if an error occurs', async () => {
            hazardDefinitionService.getHazardDefinitions.mockRejectedValue(new Error('Test error'));

            const response = await request(app.classify).post('/classify/startCombinedClassification').send({report: 'Example report content containing a hazard'}) // Use the server instance to make the request

            expect(response.statusCode).toBe(500);
        })

        test('should return a 400 if no report is supplied', async () => {
            const response = await request(app.classify).post('/classify/startCombinedClassification').send({})

            expect(response.statusCode).toBe(400)
        })
    })

    describe('getHazardsByCode', () => {
        test('should return a 200 and the full hazard information', async () => {
            const response = await request(app.classify).post('/classify/getHazardsByCode').send({hazardCodes: ["001", "003"]})

            expect(response.statusCode).toBe(200)
            expect(response.body).toStrictEqual([{"Hazard_Code": "001", "Hazard_Description": "Sample hazard", "Keywords": "hazard", "Questions": "Is there a hazard?", "Upstream_Hazards": ""}, {"Hazard_Code": "003", "Hazard_Description": "Third hazard", "Keywords": "third", "Questions": "Is there a third hazard?", "Upstream_Hazards": "001"}])
        })

        test('should return a 500 if an error occurs', async () => {
            hazardDefinitionService.getHazardDefinitions.mockRejectedValue(new Error('Test error'));

            const response = await request(app.classify).post('/classify/getHazardsByCode').send({hazardCodes: ["001", "003"]})

            expect(response.statusCode).toBe(500)
        })

        test('should return a 400 if no codes are supplied', async () => {
            const response = await request(app.classify).post('/classify/getHazardsByCode').send({})

            expect(response.statusCode).toBe(400)
        })
    })
});
