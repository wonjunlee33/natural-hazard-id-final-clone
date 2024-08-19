const {Storage} = require('@google-cloud/storage');
const storage = new Storage();
const bucketName = 'hazard_definitions_bucket';
const fileName = 'hazard_definitions.json';

let hazardDefinitionsCache = null;

exports.getHazardDefinitions = async () => {
  if (hazardDefinitionsCache) {
    return hazardDefinitionsCache;
  }
  const file = storage.bucket(bucketName).file(fileName);
  const data = await file.download();
  hazardDefinitionsCache = JSON.parse(data.toString());
  return hazardDefinitionsCache;
};
