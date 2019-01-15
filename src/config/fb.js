
import firebase from 'firebase/app'
import 'firebase/firestore'
import 'firebase/auth'
  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyBFZsl6grqK_U2kiF5FVQQ762io575y1Tg",
    authDomain: "x1-robotics.firebaseapp.com",
    databaseURL: "https://x1-robotics.firebaseio.com",
    projectId: "x1-robotics",
    storageBucket: "x1-robotics.appspot.com",
    messagingSenderId: "1093228487481"
  };

  firebase.initializeApp(config);
  firebase.firestore().settings({timestampsInSnapshots: true});

  export default firebase;
