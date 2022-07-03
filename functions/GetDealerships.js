/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    dbname = "dealerships";
    status = 200;
    
    selector = {};
    selector = {"st":params.state};

    try {
        let resultDealers = await getMatchingRecords(cloudant, dbname, selector);
        
        console.log("# of results: " + Object.values(resultDealers.result).length);
        if (Object.values(resultDealers.result).length == 0) {
            status=404;
        }
        
        return {"statusCode":status,"headers":{"Content-Type":"application/json"}, 
            "result":resultDealers.result};         
    } catch (error) {
        console.log("Caught error");
        status = 404;
        return { statusCode:status,error:error.description };
    }
   
}

 /*
 Get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"TX"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
