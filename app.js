const fetch = require('node-fetch');

const url = 'https://api.clever.com/v3.0/sections';
const options = {
  method: 'GET',
  headers: {Accept: 'application/json', Authorization: 'Bearer DEMO_TOKEN'}
};

function findNames(json){
    let districtID = "4fd43cc56d11340000000005";
    let apidata = json.data;
    let totalcount = 0;
    let numOfSections = 0;
    for (let i = 0; i < apidata.length; i++){
        if (apidata[i].data.district == districtID){
            numOfSections += 1;
            totalcount += apidata[i].data.students.length;
        }
    }
    console.log(totalcount / numOfSections);
}

fetch(url, options)
  .then(res => res.json())
  .then(json => findNames(json))
  .catch(err => console.error('error:' + err));
