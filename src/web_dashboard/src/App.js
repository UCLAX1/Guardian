import React, { Component } from 'react';
import {BrowserRouter,Switch,Route} from 'react-router-dom'
import Navbar from './components/layout/navbar'
import Dashboard from './components/dashboard/Dashboard'
import SignIn from './components/auth/SignIn'
import Camera from './components/projects/camera'
import { signOut } from './store/authActions';

//var msg = require('./client.js');

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      home: props.uid
    }
  }
  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <Navbar />
          
          <Switch>
            <Route exact path='/' component={SignIn} />
            <Route path='/signin' component={SignIn} />
            <Route path='/camera' component={Camera} />
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;