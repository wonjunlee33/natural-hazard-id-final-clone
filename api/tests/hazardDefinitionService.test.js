const hazardDefinitionService = require('../services/hazardDefinitionService');
const {Storage} = require('@google-cloud/storage');

// Mock the @google-cloud/storage module
jest.mock('@google-cloud/storage', () => {
    return {
        Storage: jest.fn().mockImplementation(() => {
            return {
                bucket: jest.fn().mockReturnValue({
                    file: jest.fn().mockReturnValue({
                        download: jest.fn().mockResolvedValue(JSON.stringify([{Hazard_Code: '1', Hazard_Description: 'Hazard 1'}]))
                    })
                })
            };
        })
    };
});


describe('hazardDefinitionService', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('getHazardDefinitions', () => {
        it('should return hazard definitions from cache if available', async () => {
            const hazardDefinitions = [{Hazard_Code: '1', Hazard_Description: 'Hazard 1'}];
            hazardDefinitionService.hazardDefinitionsCache = hazardDefinitions;

            const result = await hazardDefinitionService.getHazardDefinitions();

            expect(result).toEqual(hazardDefinitions);
        });

        it('should return hazard definitions from storage if not available in cache', async () => {
            const hazardDefinitions = [{Hazard_Code: '1', Hazard_Description: 'Hazard 1'}];
            const file = {
                download: jest.fn().mockResolvedValue(JSON.stringify(hazardDefinitions))
            };
            const bucket = {
                file: jest.fn().mockReturnValue(file)
            };
            const storage = {
                bucket: jest.fn().mockReturnValue(bucket)
            };
            Storage.mockImplementation(() => storage);

            const result = await hazardDefinitionService.getHazardDefinitions();

            expect(result).toEqual(hazardDefinitions);
        });
    });
});