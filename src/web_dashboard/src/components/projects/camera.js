import React, { Component } from 'react';
import {Redirect} from 'react-router-dom';
import './camera.css';
import { auth } from 'firebase';
import openSocket from 'socket.io-client';

class Camera extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: openSocket('http://localhost:1337'), //socket
      img: null, //image
      AutoMode: "ON", //auto
      HeadMode: "ON", //head
      BodyDir: "L", //body
      BodyDeg: 0,
      Dist: 0, //distance
      MovtDir: "L", //movement
      MovtDeg: 0,
      coords: ["0","0","0","0"],
      data: null
    }

    let self = this
    this.state.socket.on('image', curImg => { this.setState({img: curImg}) });
    this.state.socket.on('coord', curCoord => { 
      this.setState({coords: curCoord.split(',')});
    });
  }

  /* Motion Controls */
  ChangeAutoMode = () => {
    if (this.state.AutoMode == "ON")
      this.setState({AutoMode: "OFF"});
    else
      this.setState({AutoMode: "ON"});
    var dataArr = [this.state.BodyDir,this.state.BodyDeg,this.state.Dist,this.state.MovtDir,this.state.MovtDeg]
    this.state.data = dataArr.join();
    this.state.socket.emit('submit', this.state.data);
  }

  /* Head */
  ChangeHeadMode = () => {
    if (this.state.HeadMode == "ON")
      this.setState({HeadMode: "OFF"});
    else
      this.setState({HeadMode: "ON"});
    this.state.data = this.state.HeadMode;
    this.state.socket.emit('submit', this.state.data);
  }

  /* Body */
  HandleBody = (e) => { this.setState({BodyDeg: e.target.value}); }
  handleBodyDir = (e) => { this.setState({BodyDir: e.target.value}); };

  /* Dist */
  handleDist = (e) =>{ this.setState({Dist: e.target.value}); }

  /* Movt */
  handleMovt = (e) =>{ this.setState({MovtDeg: e.target.value}); }
  handleMovtDir = (e) => { this.setState({MovtDir: e.target.value}); };

  /* Submit */
  onSubmit = () => {
    var dataArr = [this.state.BodyDir,this.state.BodyDeg,this.state.Dist,this.state.MovtDir,this.state.MovtDeg, 'clean']
    this.state.data = dataArr.join();
    this.state.socket.emit('submit', this.state.data);
  }

  render() {
    var url = this.state.img ? ("data:image/jpg;base64," + this.state.img) : null;
      return (
        <div className="container">
          <div className="row dashboard">
                  <div className="col xs12 m6 image">
                    <img src={url} />
                    {/* All the info */}
                    <p>Link Position: {this.state.coords[0]}, {this.state.coords[1]}</p>
                    <p>Laser Position: {this.state.coords[2]}, {this.state.coords[3]}</p>
                  </div>
                  <div className="col m4 push-m1 button-container">

                    {/* Motion Controls */}
                    <div className="row header">
                      <h5>Motion Controls</h5>
                      <div class="divider"></div>
                    </div>

                    {/* Head */}
                    <div className="row control-category">
                      <div className="col m4 control-label">
                        <p>Head Turn: </p>
                      </div>
                      <div className="col m6 control-input">
                        <button class="waves-effect waves-light" onClick ={this.ChangeHeadMode} id="head">{this.state.HeadMode === "ON" ? "On" : "Off"}</button>
                      </div>
                    </div>

                    {/* Body */}
                    <div className="row control-category">
                      <div className="col m4 control-label">
                        <p>Body Turn: </p>
                      </div>
                      <div className="col m6 control-input">
                        <input type="text" onChange ={this.HandleBody} id="body-turn"></input><br/>
                        <p>
                          <label>
                            <input name="body" class="with-gap" type="radio" checked={this.state.BodyDir == "L"} onChange={this.handleBodyDir} value="L"/>
                            <span>Left</span>
                          </label>
                        </p>
                        <p>
                          <label>
                            <input name="body" class="with-gap" type="radio" checked={this.state.BodyDir == "R"} onChange={this.handleBodyDir} value="R"/>
                            <span>Right</span>
                          </label>
                        </p>
                      </div>
                      <div className="col m1 control-unit"><p>deg</p></div>
                    </div>

                    {/* Distance */}
                    <div className="row control-category">
                      <div className="col m4 control-label">
                        <p>Distance: </p>
                      </div>
                      <div className="col m6 control-input">
                        <input type="text" onChange ={this.handleDist} id="head-turn"></input><br/>
                      </div>
                      <div className="col m1 control-unit"><p>cm</p></div>
                    </div>

                    {/* Movement Angle */}
                    <div className="row control-category">
                      <div className="col m4 control-label">
                        <p>Movement Angle: </p>
                      </div>
                      <div className="col m6 control-input">
                        <input type="text" onChange ={this.handleMovt} id="head-turn"></input><br/>
                        <p>
                          <label>
                            <input name="movt" class="with-gap" type="radio" checked={this.state.MovtDir == "L"} onChange={this.handleMovtDir} value="L"/>
                            <span>Left</span>
                          </label>
                        </p>
                        <p>
                          <label>
                            <input name="movt" class="with-gap" type="radio" checked={this.state.MovtDir == "R"} onChange={this.handleMovtDir} value="R"/>
                            <span>Right</span>
                          </label>
                        </p>
                      </div>
                      <div className="col m1 control-unit"><p>deg</p></div>
                    </div>
                    <div className="row">
                      <div className="col m1"></div>
                      <button class="waves-effect waves-light" onClick ={this.onSubmit} id="auto">Submit</button>
                    </div>
                  </div>
                  
          </div>
        </div>
      )
  }
}

export default Camera;
