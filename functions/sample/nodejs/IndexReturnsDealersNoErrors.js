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
/*
    let dbListPromise = getDbs(cloudant);
    return dbListPromise; 
*/
    dbname = "dealerships";

    if (typeof params.state !== "undefined") {
        // Return all dealers in selected state
        /*****
        * Might want to add code so state name AND abbreviation work. 
        * Right now it requires the abbreviation 
        */
        console.log("Dealers in " + params.state);
        selector = {"st":params.state};

        let dealerByState = getMatchingRecords(cloudant, dbname, selector);
        return dealerByState; 
    } else if (typeof params.id !== "undefined") {
        // Return dealer with selected id
        console.log("Dealer with ID " + params.id);

        selector = {"id":params.id};
        let dealerById = getMatchingRecords(cloudant, dbname, selector);
        
        return dealerById;
    } else {
        console.log("All Dealers");
        
        selector = {};
        let allDealers = getMatchingRecords(cloudant, dbname, selector);
        
        return allDealers;
    }
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
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
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }
