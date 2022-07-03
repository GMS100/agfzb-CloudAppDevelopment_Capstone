/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    dbname = "dealerships";
    status = 200;
    
//    if (typeof params.state !== "undefined") {
        // Return all dealers in selected state
        /*****
        * Might want to add code so state name AND abbreviation work. 
        * Right now it requires the abbreviation 
        */
//        console.log("Dealers in " + params.state);
        selector = {};
        selector = {"st":params.state};

        let resultDealer = getMatchingRecords(cloudant, dbname, selector);
        
        return resultDealer; 

//        return {"statusCode":status,"headers":{"Content-Type":"application/json"}, "result":dealerByState.result}; 
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
//                   resolve({result:result.result});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
