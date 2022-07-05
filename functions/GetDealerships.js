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

/*    try {  */
        if (params.state != undefined && params.state.length == 2) {
            console.log("Have state abbreviation parameter");
            selector = {"st":params.state.toUpperCase()};
        } else if (params.state !== undefined) {
            console.log("Have state name parameter");
            //this only works if the name starts with capital and then lowercase
            selector = {"state":params.state};
        } else if (params.dealerId != undefined) {
            console.log("Have ID parameter");
            selector = {"id":parseInt(params.dealerId)};
        }
        
//        console.log("Selector= " + JSON.stringify(selector));
        let resultDealers = await getMatchingRecords(cloudant, dbname, selector);
        
        console.log("# of results: " + Object.values(resultDealers.result).length);
        if (Object.values(resultDealers.result).length == 0) {
            status = 404
            return { "statusCode":status, "message":"No results returned"};
        }
        
        return {"statusCode":status,"headers":{"Content-Type":"application/json"}, 
            "result":resultDealers.result};         
/*    } catch (err) {
        console.error(err);
        status = 404;
        return { "statusCode":status,"error":err}; 
    } */
}

 /*
 Get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"TX"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
//         cloudant.postFind({db:dbname,selector:selector,limit:5})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
