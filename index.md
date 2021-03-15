<!-- <!doctype html> -->
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <script src="https://code.jquery.com/jquery-3.1.1.min.js"  crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

    <!-- The core Firebase JS SDK is always required and must be listed first -->
    <script src="https://www.gstatic.com/firebasejs/8.3.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/3.1.0/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/3.1.0/firebase-database.js"></script>

    <!-- TODO: Add SDKs for Firebase products that you want to use
      https://firebase.google.com/docs/web/setup#available-libraries -->
    <script src="https://www.gstatic.com/firebasejs/8.3.0/firebase-analytics.js"></script>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <!-- <h1>Hello, world!</h1> -->
   <button type="button" class="btn btn-primary" onclick="Authorize()" >Authorize</button>
   <div id="authorized" >

   </div>


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
      location.href = "http://www.strava.com/oauth/authorize?client_id=62896&response_type=code&redirect_uri=https://rads284.github.io/AW80D/#authorized&approval_prompt=force&scope=read_all";
   }

   function saveToFirebase() {
      currentUrl = window.location.href;
      var url = new URL(currentUrl);
      var c = url.searchParams.get("code");
      console.log(c);
      $.post('https://www.strava.com/oauth/token?client_id=62896&client_secret=168e6d7e8e869d6d17abadfc9c3022f1c9bfe3da&code='+ c +'&grant_type=authorization_code',   // url
       {}, // data to be submit
       function(data, status, jqXHR) {// success callback
               //  $('p').append('status: ' + status + ', data: ' + data);
               console.log(data);
               firebase.database().ref('auth-tokens').push().set(data)
               .then(function(snapshot) {
                     success(); // some success method
               }, function(error) {
                     console.log('error' + error);
                     error(); // some error method
               });
        })
   }
   //  var emailObject = {
   //      email: email
   //  };

//    saveToFirebase(email);
   // $(document).ready(function() {
   //    console.log( "ready!" );
   //    saveToFirebase();
   // });

   window.onload = function() {
      console.log( "loading!" );
      saveToFirebase();
   };
   </script>


   </body>
</html>



