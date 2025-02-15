const express = require('express');
const app = express();
const fs = require('fs');
app.use(express.static("assests"));
const bodyParser=require('body-parser');
app.use(bodyParser.json());
app.use(express.urlencoded({ extended:true }));
const axios = require('axios');
var nodemailer = require('nodemailer');
const { spawn } = require('child_process');
app.use(express.static("assests"))
var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'Keerthisekharkandukuri@gmail.com',
    pass: 'rroxmtrerkbpypxs'
  }
});

app.get('/',function(req,res){
    res.sendFile(__dirname+"/home.html");
});
app.get('/contact',function(req,res){
    res.sendFile(__dirname+"/contact.html")
})
app.get("/about",function(req,res){
    res.sendFile(__dirname+"/about.html")
})
app.get("/symptom/predict",function(req,res){
    res.sendFile(__dirname+"/symptomchecker.html")
})
app.get("/checker",function(req,res){
  res.sendFile(__dirname+"/checker.html")
})
app.get('/tb',function(req,res){
  res.sendFile(__dirname+"/tb.html")
})
app.get("/tbchecker",function(req,res){
  res.sendFile(__dirname+"/tbchecker.html")
})
app.get("/outbreaks",function(req,res){
  // fs.readFile('predictions.txt', 'utf8', (err, data) => {
  //   if (err) {
  //     console.error(err);
  //     res.status(500).send('Error reading file');
  //     return;
  //   }

  //   // Split the data by line
  //   const predictions = data.trim().split('\n');
    res.sendFile(__dirname+"/covidoutbreaks.html")
    // // Generate HTML to display the predictions
    // const html = `
    //   <!DOCTYPE html>
    //   <html>
    //     <head>
    //       <title>Predictions</title>
    //       <style>
    //         /* Add your CSS styling here */
    //       </style>
    //     </head>
    //     <body>
    //       <h1>Predictions</h1>
    //       <ul>
    //         ${predictions.map((prediction, index) => `<li> ${prediction}</li>`).join('')}
    //       </ul>
    //     </body>
    //   </html>
    // `;

    // // Send the HTML response
    // res.send(html);
    

        // res.send(predictions);
  //});
  // const pythonScript = spawn('python', ['prediction.py']);
  // pythonScript.stdout.on('data', (data) => {
  //   // Process the data emitted by the Python script
  //   const predictions = data.toString().trim().split('\n');
  //   predictions.forEach((prediction, index) => {
  //     console.log(`Prediction ${index + 1}: ${prediction}`);
  //   });
  // });
  
  // pythonScript.on('close', (code) => {
  //   console.log(`Python script exited with code ${code}`);
  // });
// // Read predictions from the file
// fs.readFile('predictions.txt', 'utf8', (err, data) => {
//   if (err) {
//     console.error(err);
//     return;
//   }
  
//   // Split the predictions by line and display them
//   const predictions = data.trim().split('\n');
//   predictions.forEach((prediction, index) => {
//     console.log(`Prediction ${index + 1}: ${prediction}`);
//   });
// });

})
app.get('/sample.txt',function(req,res){
  res.sendFile(__dirname+"/sample.txt")
})
app.post('/checker', async (req, res) => {
  // const { cough, fever, sore_throat, shortness_of_breath, head_ache, age_60_and_above, gender } = req.body;

  // You can now use these variables to perform any further processing or store them as needed
  const name = req.body.name;
  const age = req.body.age;
  const cough = req.body.cough;
  const fever = req.body.fever;
  const sore_throat = req.body.sore_throat;
  const shortness_of_breath = req.body.shortness_of_breath;
  const head_ache = req.body.head_ache;
  const age_60_and_above = req.body.age_60_and_above;
  const gender = req.body.gender;
  console.log('Cough:', cough);
  console.log('Fever:', fever);
  console.log('Sore Throat:', sore_throat);
  console.log('Shortness of Breath:', shortness_of_breath);
  console.log('Headache:', head_ache);
  console.log('Age 60 and Above:', age_60_and_above);
  console.log('Gender:', gender);

  const data = [cough, fever, sore_throat, shortness_of_breath, head_ache, age_60_and_above, gender];
  let prediction = '';

  const pythonScript = spawn('python', ['prediction.py']);
  var output;
  pythonScript.stdout.on('data', (data) => {
    console.log(`Received output from Python script: ${data}`);
    output = data.toString().trim();
  
    // Check if the output includes the string "Yes"
    if (output.includes("1")) {
      console.log('Prediction: Yes');
      // Handle the 'Yes' case
      res.sendFile(__dirname + "/covidyes.html");
    } else {
      console.log('Prediction: No');
      // Handle the 'No' case
      res.sendFile(__dirname + "/covidno.html");
    }
  });
  
  // pythonScript.stdout.on('data', (data) => {
  //   console.log(`Received output from Python script: ${data}`);
  //   console.log("hello world")
  //   output= data.toString().trim(); // Assuming each output is on a separate line
  //   console.log(output+"output")
  //   // Filter and store only the prediction
  //   if (output.startsWith('Prediction:')) {
  //     console.log("hii")
  //     const predictionStr = output.replace('Prediction:', '').trim();
  //     const predictionList = JSON.parse(predictionStr);
  //     if (Array.isArray(predictionList) && predictionList.length === 1) {
  //       prediction = predictionList[0];
  //       console.log("project")
  //       console.log(prediction)
  //       console.log('Prediction:', prediction);
  //     }
  //   }
  // });

  pythonScript.stderr.on('data', (data) => {
    console.error(`Python error: ${data}`);
    res.status(500).json({ error: 'An error occurred during prediction.' });
  });
  

  // pythonScript.on('close', () => {
  //   console.log(output+"hiii");

  // Convert the output value to a string and trim any whitespace
  // const outputStr = output.toString().trim();
  // console.log(outputStr)
  //   console.log("hello world")
  //   console.log(prediction)
  //   if (output==['1']){
  //     res.sendFile(__dirname + "/covidyes.html");
  //   } else {
  //     // Handle other cases or display an error
  //     res.sendFile(__dirname + "/covidno.html");
  //   }
  // });
  

  data.forEach((message) => {
    pythonScript.stdin.write(message + '\n');
  });

  pythonScript.stdin.end();
});
app.post('/detection', async (req, res) => {
  const no = req.body.no;
  const id = req.body.id;
  const name = req.body.name;
  const gender = req.body.gender;
  const date = req.body.date;
  const time = req.body.time;
  const fever = req.body.fever;
  const coughingBlood = req.body['coughing-blood'];
  const sputumMixed = req.body['sputum-mixed'];
  const nightSweats = req.body.nightsweats;
  const chestPain = req.body['chest-pain'];
  const backPain = req.body.backpain;
  const shortnessOfBreath = req.body['shortness-of-breath'];
  const weightLoss = req.body['weight-loss'];
  const lumps = req.body.lumps;
  const coughPhlegm = req.body['cough-phlegm'];
  const swollenLymphNodes = req.body['lymph-nodes'];
  const appetite = req.body.appetite;
  const tuberculosis = req.body.tuberculosis;

  const data = [
    
    fever,
    coughingBlood,
    sputumMixed,
    nightSweats,
    chestPain,
    backPain,
    shortnessOfBreath,
    weightLoss,
    lumps,
    coughPhlegm,
    swollenLymphNodes,
    appetite,
    gender
   
  ];
   console.log(data)
  let prediction = '';

  const pythonScript = spawn('python', ['tb detection.py']);

  // pythonScript.stdout.on('data', (data) => {
  //   console.log(`Received output from Python script: ${data}`);
  //   const output = data.toString().trim(); // Assuming each output is on a separate line
  
  //   // Filter and store only the prediction
  //   if (output.startsWith('Prediction:')) {
  //     const predictionStr = output.replace('Prediction:', '').trim();
  //     const predictionList = JSON.parse(predictionStr);
  //     console.log("hello world")
  //     if (Array.isArray(predictionList) && predictionList.length === 3) {
  //       prediction = predictionList[0];
  //       console.log("hello world");
  //       console.log('Prediction:', prediction);
  //     }
  //   }
  // });
  // pythonScript.stdout.on('data', (data) => {
  //   console.log(`Received output from Python script: ${data}`);
  //   output = data.toString().trim();
  
  //   // Check if the output is equal to ['Yes']
  //   if (output === "['Yes']") {
  //     console.log('Prediction: Yes');
  //     // Handle the 'Yes' case
  //     res.sendFile(__dirname + "/tbyes.html");
  //   } else {
  //     console.log('Prediction: No');
  //     // Handle the 'No' case
  //     res.sendFile(__dirname + "/tbdno.html");
  //   }
  // });
  pythonScript.stdout.on('data', (data) => {
    console.log(`Received output from Python script: ${data}`);
    output = data.toString().trim();
  
    // Check if the output includes the string "Yes"
    if (output.includes("Yes")) {
      console.log('Prediction: Yes');
      // Handle the 'Yes' case
      res.sendFile(__dirname + "/tbyes.html");
    } else {
      console.log('Prediction: No');
      // Handle the 'No' case
      res.sendFile(__dirname + "/tbno.html");
    }
  });
  

  pythonScript.stderr.on('data', (data) => {
    console.error(`Python error: ${data}`);
    res.status(500).json({ error: 'An error occurred during prediction.' });
  });

  // pythonScript.on('close', () => {
  //   if (prediction==['Yes']) {
  //     res.sendFile(__dirname + "/tbyes.html");
  //   } else {
  //     // Handle other cases or display an error
  //     res.sendFile(__dirname + "/tbno.html");
  //   }
  // });

  data.forEach((message) => {
    pythonScript.stdin.write(message + '\n');
  });

  pythonScript.stdin.end();
});
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});


app.post('/date',function(req,res){
  var date=req.body.date;
  console.log(date)
  const pythonScript = spawn('python', ['sampleout.py']);
  pythonScript.stdin.write(date + '\n');
  pythonScript.stdout.on('data', (data) => {
    // Handle the output from the Python script
    console.log(`Received output from Python script: ${data}`);
    console.log(data.toString());
  });
  
  pythonScript.stderr.on('data', (data) => {
    // Handle any error output from the Python script
    console.error(data.toString());
  });
  pythonScript.on('close', (code) => {
    res.sendFile(__dirname+"/covidoutbreaks.html")
  });
})


app.listen(8000);
