<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <!-- <h1>Hello, world!</h1> -->
<button type="button" class="btn btn-primary" onclick="Authorize()" >Authorize</button>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

   <!-- The core Firebase JS SDK is always required and must be listed first -->
   <script src="https://www.gstatic.com/firebasejs/8.3.0/firebase-app.js"></script>

   <!-- TODO: Add SDKs for Firebase products that you want to use
      https://firebase.google.com/docs/web/setup#available-libraries -->
   <script src="https://www.gstatic.com/firebasejs/8.3.0/firebase-analytics.js"></script>

   <script>
   // Your web app's Firebase configuration
   // For Firebase JS SDK v7.20.0 and later, measurementId is optional
   var firebaseConfig = {
      apiKey: "AIzaSyDUK-eac-AEjTserNhhxf9YHNAede6-hec",
      authDomain: "aw80d-79986.firebaseapp.com",
      databaseURL: "https://aw80d-79986-default-rtdb.firebaseio.com",
      projectId: "aw80d-79986",
      storageBucket: "aw80d-79986.appspot.com",
      messagingSenderId: "479833555559",
      appId: "1:479833555559:web:d1a43ef6a4ac386c8dcac2",
      measurementId: "G-2PPLC6MK8Q"
   };
   // Initialize Firebase
   firebase.initializeApp(firebaseConfig);
   firebase.analytics();

   function Authorize() {
      $.getJSON("http://www.strava.com/oauth/authorize?client_id=62896&response_type=code&redirect_uri=https://localhost/exchange_token&approval_prompt=force&scope=read_all&callback=?", function(data) {
         console.log(data);
      });
   }
//    function saveToFirebase(email) {
//     var emailObject = {
//         email: email
//     };

//     firebase.database().ref('subscription-entries').push().set(emailObject)
//         .then(function(snapshot) {
//             success(); // some success method
//         }, function(error) {
//             console.log('error' + error);
//             error(); // some error method
//         });
// }

//    saveToFirebase(email);
   </script>


   </body>
</html>

