import React, { Component } from 'react';
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
      HeadDir: "L", //head
      HeadDeg: 0,
      BodyDir: "L", //body
      BodyDeg: 0,
      Dist: 0, //distance
      MovtDir: "L", //movement
      MovtDeg: 0,
      LinkX: -1, //link pos
      LinkY: -1,
      LaserX: -1, //laser pos
      LaserY: -1,
      data: null
    }

    let self = this
    this.state.socket.on('image', curImg => { this.setState({img: curImg}) });
  }

  /* Motion Controls */
  ChangeAutoMode = () => {
    if (this.state.AutoMode == "ON")
      this.setState({AutoMode: "OFF"});
    else
      this.setState({AutoMode: "ON"});
    var dataArr = [this.state.AutoMode,this.state.HeadDir,this.state.HeadDeg,this.state.BodyDir,this.state.BodyDeg,this.state.Dist,this.state.MovtDir,this.state.MovtDeg]
    this.state.data = dataArr.join();
    this.state.socket.emit('submit', this.state.data);
  }
  /* Head */
  handleHead = (e) => { this.setState({HeadDeg: e.target.value}); }
  handleHeadDir = (e) => { this.setState({HeadDir: e.target.value}); };

  /* Body */
  handleBody = (e) =>{ this.setState({BodyDeg: e.target.value}); }
  handleBodyDir = (e) => { this.setState({BodyDir: e.target.value}); };

  /* Dist */
  handleDist = (e) =>{ this.setState({Dist: e.target.value}); }

  /* Movt */
  handleMovt = (e) =>{ this.setState({MovtDeg: e.target.value}); }
  handleMovtDir = (e) => { this.setState({MovtDir: e.target.value}); };

  /* Submit */
  onSubmit = () => {
    var dataArr = [this.state.AutoMode,this.state.HeadDir,this.state.HeadDeg,this.state.BodyDir,this.state.BodyDeg,this.state.Dist,this.state.MovtDir,this.state.MovtDeg]
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
                    <p>Link Position: {this.state.LinkX}, {this.state.LinkY}</p>
                    <p>Laser Position: {this.state.LaserX}, {this.state.LaserY}</p>
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
                        <input type="text" onChange ={this.handleHead} id="head-turn"></input><br/>
                        <p>
                          <label>
                            <input name="head" class="with-gap" type="radio" checked={this.state.HeadDir == "L"} onChange={this.handleHeadDir} value="L"/>
                            <span>Left</span>
                          </label>
                        </p>
                        <p>
                          <label>
                            <input name="head" class="with-gap" type="radio" checked={this.state.HeadDir == "R"} onChange={this.handleHeadDir} value="R"/>
                            <span>Right</span>
                          </label>
                        </p>
                      </div>
                      <div className="col m1 control-unit"><p>deg</p></div>
                    </div>

                    {/* Body */}
                    <div className="row control-category">
                      <div className="col m4 control-label">
                        <p>Body Turn: </p>
                      </div>
                      <div className="col m6 control-input">
                        <input type="text" onChange ={this.handleBody} id="head-turn"></input><br/>
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
                      <button class="waves-effect waves-light" onClick ={this.ChangeAutoMode} id="auto">Auto {this.state.AutoMode === "ON" ? "On" : "Off"}</button>
                    </div>
                  </div>
                  
          </div>
        </div>
      )
  }
}

export default Camera;
