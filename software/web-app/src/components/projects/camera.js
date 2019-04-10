import React, { Component } from 'react';
import './camera.css';
import { auth } from 'firebase';
import openSocket from 'socket.io-client';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: openSocket('http://localhost:1337'),
      img: null
    }

    let self = this
    this.state.socket.on('event', curImg => {
      this.setState({img: curImg})
    });
  }

  render() {
    var url = this.state.img ? ("data:image/jpg;base64," + this.state.img) : null;
      return (
        <div className="container">
          <div className="row button-container">
                  <div className="row"><img src={url} /></div>
                  <div className="row">{url}</div>
                  <button className="col s8 offset-s2 m2 offset-m9">Tracking</button>
                  <div className="row"></div>
                  <button className="col s8 offset-s2 m2 offset-m9">Follow Link</button>
                  <div className="row"></div>
                  <button className="col s8 offset-s2 m2 offset-m9">Up</button>
                  <div className="row"></div>
                  <button className="col s8 offset-s2 m2 offset-m9">Left</button>
                  <div className="row"></div>
                  <button className="col s8 offset-s2 m2 offset-m9">Right</button>
                  <div className="row"></div>
                  <button  className="col s8 offset-s2 m2 offset-m9">Down</button>
                  <div className="row"></div>
                  <button className="col s8 offset-s2 m2 offset-m9">Auto Mode</button>
          </div>
        </div>
      )
  }
}

export default App;
